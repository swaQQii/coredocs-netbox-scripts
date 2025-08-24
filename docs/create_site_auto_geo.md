### **Create Site OSM Script (`02_create_site_auto_geo.py`)**

A NetBox Custom Script that creates new **Sites** with automatically enriched metadata:

- Uses **OpenStreetMap (OSM) geocoding** to normalize street, city, and postal code  
- Automatically fetches **latitude/longitude**  
- Infers the correct **time zone** from coordinates  
- Validates input (street, house number, postal code) against OSM data  
- Supports optional fields: **Region, Site Group, ASNs, Facility, Shipping address**  

[View Script](../scripts/02_create_site_auto_geo.py)
