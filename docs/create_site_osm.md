### **Create Site OSM Script (`03_create_site_osm.py`)**

A NetBox Custom Script that creates new **Sites** with automatically enriched metadata:

- Uses **OpenStreetMap (OSM) geocoding** to normalize street, city, and postal code
- Automatically fetches **latitude/longitude**
- Infers the correct **time zone** from coordinates
- Validates input (street, house number, postal code) against OSM data
- Supports optional fields: **Region, Site Group, ASNs, Facility, Shipping address**

#### Example Screenshots

1. **Input Form in NetBox**  
   ![Input Form](../images/create_site_osm_1.png)

2. **Geocoding Results**  
   ![Geocoding Results](../images/create_site_osm_2.png)

3. **Created Site in NetBox**  
   ![Created Site](../images/create_site_osm_3.png)

[View Script](../scripts/03_create_site_osm.py)
