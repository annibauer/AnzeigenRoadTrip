from functions.anzeigen import make_location_code_reference
from functions.maps import  get_postcodes_in_radius

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'}

# postcode=10967

# make_location_code_reference(headers, postcode)

center_postcode = "SW1A 1AA"  # Replace with the center postcode
radius_km = 5  # Replace with the desired radius in kilometers

result = get_postcodes_in_radius(center_postcode, radius_km)

