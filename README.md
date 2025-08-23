# coredocs-netbox-scripts

Collection of reusable **NetBox Custom Scripts** – automation examples for:

- Creating and updating Virtual Machines  
- Assigning IPv4 addresses automatically  
- Enforcing naming conventions  
- Streamlining repetitive workflows in NetBox  

---

## Getting Started

### Requirements
- [NetBox](https://github.com/netbox-community/netbox) (v3.6+ recommended)  
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

## Repository Structure

.
├── 00_hello_script.py # Minimal example: inputs, logging, dry-run
├── 01_reserve_ipv4.py # Reserve next free IPv4 with optional DNS name
└── (more coming soon) # VM creation, interface automation, etc.

---

## License
This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute these scripts with attribution.

---

## Related
These scripts are part of the **[CoreDocs](https://coredocs.eu)** knowledge base project,  
which provides open IT guides, tools, and documentation resources.
