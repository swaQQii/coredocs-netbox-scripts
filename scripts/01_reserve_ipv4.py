from extras.scripts import ObjectVar, Script, StringVar
from ipam.models import IPAddress, Prefix


class ReserveIPv4(Script):
    class Meta:
        name = "Reserve IPv4"
        description = (
            "Find the first free IPv4 in the selected prefix and create an IPAddress"
        )

    prefix = ObjectVar(
        model=Prefix,
        required=True,
        label="IPv4 Prefix",
        description="Select the prefix to reserve the next free address from.",
    )
    dns_name = StringVar(
        required=False,
        label="DNS name (optional)",
        description="Stored as DNS name, e.g., 'web01'.",
    )

    def _pick_free_ip(self, prefix):
        for host in prefix.prefix.iter_hosts():
            ip_str = str(host)
            if IPAddress.objects.filter(address__startswith=f"{ip_str}/").exists():
                self.log_info(f"{ip_str} -> in use (NetBox)")
                continue
            self.log_success(f"{ip_str} -> free, will be used")
            return ip_str
        return None

    def run(self, data, commit):
        prefix = data["prefix"]
        dns_name = (data.get("dns_name") or "").strip()

        if prefix.prefix.version != 4:
            self.log_failure(f"{prefix.prefix} is not an IPv4 prefix.")
            return "Aborted."

        ip_plain = self._pick_free_ip(prefix)
        if not ip_plain:
            self.log_failure(f"No free IP found in {prefix.prefix}.")
            return "Aborted."

        ip_with_mask = f"{ip_plain}/{prefix.prefix.prefixlen}"

        ip_obj = IPAddress(address=ip_with_mask, dns_name=dns_name or "")
        if commit:
            ip_obj.save()
            self.log_success(
                f"IPAddress created: {ip_obj.address} (dns_name='{ip_obj.dns_name}')"
            )
        else:
            self.log_info(
                f"[Dry-Run] would create: {ip_with_mask} (dns_name='{dns_name}')"
            )

        return f"Prefix: {prefix.prefix}, IP: {ip_with_mask}, Commit={commit}"
