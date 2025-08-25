import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

import requests
from dcim.choices import SiteStatusChoices
from dcim.models import Region, Site, SiteGroup
from django.utils.text import slugify
from extras.scripts import MultiObjectVar, ObjectVar, Script, StringVar
from ipam.models import ASN


class CreateSiteOSMScript(Script):
    class Meta:
        name = "Create Site OSM Script"
        description = "Structured address via OSM geocoding with auto time zone."

    site_name = StringVar(label="Site Name")
    street = StringVar(label="Street")
    house_number = StringVar(label="House Number")
    addition = StringVar(label="Addition", required=False)
    postal_code = StringVar(label="Postal Code", required=False)
    city = StringVar(label="City")
    shipping_address = StringVar(label="Shipping Address", required=False)
    facility = StringVar(label="Facility", required=False)
    region = ObjectVar(model=Region, required=False, label="Region")
    group = ObjectVar(model=SiteGroup, required=False, label="Site Group")
    asns = MultiObjectVar(model=ASN, required=False, label="ASNs")

    def _round_to_six(self, value):
        try:
            return Decimal(str(value)).quantize(
                Decimal("0.000001"), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, TypeError, ValueError):
            return None

    def _normalize_string(self, string: str) -> str:
        return re.sub(r"[^0-9a-z]", "", (string or "").lower())

    def _geocode_address(self, street, house_full, postal_code, city):
        params = {
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
            "street": f"{street} {house_full}",
            "city": city,
        }
        if postal_code:
            params["postalcode"] = postal_code
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent": "netbox-script/1.0"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def run(self, inputs, commit):
        site_name = (inputs["site_name"] or "").strip()
        street = (inputs["street"] or "").strip()
        house_number = (inputs["house_number"] or "").strip()
        addition = (inputs.get("addition") or "").strip()
        house_full = f"{house_number}{addition}" if addition else house_number
        postal_code = (inputs.get("postal_code") or "").strip()
        city = (inputs["city"] or "").strip()

        try:
            geocode_result = self._geocode_address(
                street, house_full, postal_code, city
            )
        except Exception as e:
            self.log_failure(f"Geocoding error: {e}")
            return f"Aborted: {e}"

        if not geocode_result:
            self.log_failure("No result from OSM.")
            return "Aborted: no match."

        lat = self._round_to_six(geocode_result.get("lat"))
        lon = self._round_to_six(geocode_result.get("lon"))
        if lat is None or lon is None:
            self.log_failure("Invalid coordinates from OSM.")
            return "Aborted: invalid coordinates."

        self.log_success(f"Geocoding OK: {lat},{lon}")

        site = Site(
            name=site_name,
            slug=slugify(site_name),
            status=SiteStatusChoices.STATUS_ACTIVE,
            latitude=lat,
            longitude=lon,
        )
        site.full_clean()
        if commit:
            site.save()
            self.log_success(f"Site '{site.name}' created.")
        return f"Site: {site.name}, Lat: {lat}, Lon: {lon}, Commit={commit}"
