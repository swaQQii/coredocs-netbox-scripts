[![Website](https://img.shields.io/badge/Website-coredocs.eu-9146FF?style=for-the-badge&logo=google-chrome&logoColor=white)](https://coredocs.eu)

[![Lint](https://img.shields.io/github/actions/workflow/status/swaQQii/coredocs-netbox-scripts/lint.yml?style=for-the-badge&label=Lint%20CI&logo=github)](https://github.com/swaQQii/coredocs-netbox-scripts/actions/workflows/lint.yml)
[![Style](https://img.shields.io/github/actions/workflow/status/swaQQii/coredocs-netbox-scripts/style.yml?style=for-the-badge&label=Style%20CI&logo=github)](https://github.com/swaQQii/coredocs-netbox-scripts/actions/workflows/style.yml)
[![Link Check](https://img.shields.io/github/actions/workflow/status/swaQQii/coredocs-netbox-scripts/link-check.yml?style=for-the-badge&label=Link%20Check&logo=github)](https://github.com/swaQQii/coredocs-netbox-scripts/actions/workflows/link-check.yml)

[![Last Commit](https://img.shields.io/github/last-commit/swaQQii/coredocs-netbox-scripts?style=for-the-badge)](https://github.com/swaQQii/coredocs-netbox-scripts/commits/main)

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

# coredocs-netbox-scripts

Collection of reusable **NetBox Custom Scripts** – automation examples for:

- Creating and updating Virtual Machines
- Assigning IPv4 addresses automatically
- Enforcing naming conventions
- Streamlining repetitive workflows in NetBox

---

## Table of Contents

- [Getting Started](#getting-started)
- [Available Scripts](#available-scripts)
  - [Hello Script](docs/hello_script.md) → [Code](scripts/01_hello_script.py)
  - [Reserve IPv4 Script](docs/reserve_ipv4.md) → [Code](scripts/02_reserve_ipv4.py)
  - [Create Site (Auto Geo)](docs/create_site_auto_geo.md) → [Code](scripts/03_create_site_osm.py)
- [License](#license)
- [Related](#related)

---

## Getting Started

### Requirements

- [NetBox](https://github.com/netbox-community/netbox) (v4.3+ recommended)
- Python 3.x environment (ships with NetBox)

### Usage

1. Clone this repository or copy the desired script(s).
2. Upload them directly via the NetBox UI:  
   **Extras / (Customization) → Scripts → Upload Script**
3. Alternatively, place them under your NetBox installation:
4. Run scripts via the NetBox web interface.

- Toggle **Commit** off → dry run (no database changes)
- Toggle **Commit** on → changes are saved

---

## Available Scripts

- **[Hello Script](docs/hello_script.md)** – Minimal example to demonstrate inputs, logging, and commit.
- **[Reserve IPv4](docs/reserve_ipv4.md)** – Finds the first free IPv4 in a prefix and assigns it.
- **[Create Site (Auto-Geo)](docs/create_site_osm.md)** – Creates a Site using OSM geocoding, coordinates, and timezone auto-detection.

---

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute these scripts with attribution.

---

## Related

These scripts are part of the **[CoreDocs](https://coredocs.eu)** knowledge base project,  
which provides open IT guides, tools, and documentation resources.
