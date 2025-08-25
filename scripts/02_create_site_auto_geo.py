import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

import requests
from dcim.choices import SiteStatusChoices
from dcim.models import Region, Site, SiteGroup
from django.utils.text import slugify
from extras.scripts import MultiObjectVar, ObjectVar, Script, StringVar
from ipam.models import ASN


class CreateSiteOSM(Script):
    class Meta:
        name = "Create Site OSM"
        description = "Structured address via OSM geocoding with auto time zone."

    site_name = StringVar(label="Site name")
    street = StringVar(label="Street")
    house_number = StringVar(label="House number")
    addition = StringVar(label="Addition", required=False)
    postal_code = StringVar(label="Postal code", required=False)
    city = StringVar(label="City")
    shipping_address = StringVar(label="Shipping address", required=False)
    facility = StringVar(label="Facility", required=False)
    region = ObjectVar(model=Region, required=False, label="Region")
    group = ObjectVar(model=SiteGroup, required=False, label="Site group")
    asns = MultiObjectVar(model=ASN, required=False, label="ASNs")

    def _round6(self, v):
        try:
            return Decimal(str(v)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, TypeError, ValueError):
            return None

    def _tok(self, s: str):
        return re.findall(r"\w+", (s or "").lower())

    def _eq_simple(self, a: str, b: str) -> bool:
        ta, tb = self._tok(a), self._tok(b)
        return ta == tb or (len(ta) > 0 and all(t in tb for t in ta))

    def _norm_hn(self, s: str) -> str:
        return re.sub(r"[^0-9a-z]", "", (s or "").lower())

    def _pick_city(self, a: dict) -> str:
        return (
            a.get("city")
            or a.get("town")
            or a.get("village")
            or a.get("municipality")
            or a.get("hamlet")
            or ""
        )

    def _format_address(self, a: dict, house_full: str) -> str:
        street = (
            a.get("road")
            or a.get("pedestrian")
            or a.get("residential")
            or a.get("footway")
            or ""
        )
        postcode = a.get("postcode") or ""
        city = self._pick_city(a)
        state = a.get("state") or ""
        country = a.get("country") or ""
        line1 = " ".join([p for p in [street, house_full] if p])
        parts = [line1, " ".join([p for p in [postcode, city] if p])]
        if state:
            parts.append(state)
        if country:
            parts.append(country)
        return ", ".join([p for p in parts if p])

    def _geocode_structured(self, street, house_full, postal_code, city):
        params = {
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
            "street": f"{street} {house_full}",
            "city": city,
        }
        if postal_code:
            params["postalcode"] = postal_code
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent": "netbox-script/1.0"},
            timeout=8,
        )
        r.raise_for_status()
        data = r.json()
        return data[0] if data else None

    def _geocode_fallback(self, street, house_full, postal_code, city):
        q = ", ".join([p for p in [f"{street} {house_full}", postal_code, city] if p])
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "limit": 1, "addressdetails": 1, "q": q},
            headers={"User-Agent": "netbox-script/1.0"},
            timeout=8,
        )
        r.raise_for_status()
        data = r.json()
        return data[0] if data else None

    def _infer_timezone(self, lat: float, lon: float) -> str:
        try:
            r = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "current": "temperature_2m",
                    "timezone": "auto",
                },
                headers={"User-Agent": "netbox-script/1.0"},
                timeout=8,
            )
            r.raise_for_status()
            tz = (r.json().get("timezone") or "").strip()
            return tz if "/" in tz else ""
        except Exception:
            return ""

    def run(self, data, commit):
        name = (data["site_name"] or "").strip()
        street = (data["street"] or "").strip()
        hn = (data["house_number"] or "").strip()
        add = (data.get("addition") or "").strip()
        house_full = f"{hn}{add}" if add else hn
        postal_code = (data.get("postal_code") or "").strip()
        city = (data["city"] or "").strip()
        shipping = (data.get("shipping_address") or "").strip() or ""
        facility = (data.get("facility") or "").strip() or ""
        region = data.get("region")
        group = data.get("group")
        asns = data.get("asns") or []

        try:
            item = self._geocode_structured(street, house_full, postal_code, city)
            if not item:
                item = self._geocode_fallback(street, house_full, postal_code, city)
        except Exception as e:
            self.log_failure(f"Geocoding error: {e}")
            return f"Aborted: {e}"
        if not item:
            self.log_failure("No result from OSM.")
            return "Aborted: no match."

        addr = item.get("address", {})
        lat = self._round6(item.get("lat"))
        lon = self._round6(item.get("lon"))
        if lat is None or lon is None:
            self.log_failure("Invalid coordinates from OSM.")
            return "Aborted: invalid coordinates."

        osm_street = (
            addr.get("road")
            or addr.get("pedestrian")
            or addr.get("residential")
            or addr.get("footway")
            or ""
        ).strip()
        osm_hn = (addr.get("house_number") or "").strip()
        osm_post = (addr.get("postcode") or "").strip()
        if not self._eq_simple(street, osm_street):
            self.log_failure(f"Street mismatch: '{street}' vs '{osm_street}'")
            return "Aborted: street mismatch."
        if house_full and osm_hn and self._norm_hn(house_full) != self._norm_hn(osm_hn):
            self.log_failure(f"House number mismatch: '{house_full}' vs '{osm_hn}'")
            return "Aborted: house number mismatch."
        if postal_code and osm_post and self._tok(postal_code) != self._tok(osm_post):
            self.log_failure(f"Postal code mismatch: '{postal_code}' vs '{osm_post}'")
            return "Aborted: postal code mismatch."

        final_addr = self._format_address(addr, house_full)
        tz = self._infer_timezone(float(lat), float(lon)) or None

        self.log_success(f"Geocoding OK: {lat},{lon}")
        self.log_info(f"Normalized address: {final_addr}")
        if tz:
            self.log_info(f"Time zone: {tz}")

        site = Site(
            name=name,
            slug=slugify(name),
            status=SiteStatusChoices.STATUS_ACTIVE,
            region=region,
            group=group,
            facility=facility,
            physical_address=final_addr,
            shipping_address=shipping,
            latitude=lat,
            longitude=lon,
            time_zone=tz,
        )
        site.full_clean()
        if commit:
            site.save()
            if asns:
                site.asns.set(asns)
            self.log_success(f"Site '{site.name}' created.")
        return (
            f"{site.name} | addr='{final_addr}' | lat={lat} lon={lon} | tz={tz or ''}"
        )
