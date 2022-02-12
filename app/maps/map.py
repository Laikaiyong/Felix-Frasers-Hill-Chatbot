import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
LOCATIONS = {
    "Shahzan Inn": "Shahzan Inn Fraser's Hill",
    "Puncak Inn": "Puncak Inn Bukit Fraser",
    "The Pines": "The Pines Fraser's Hill",
    "Silverpark Resort": "Silverpark Resort Fraser's Hill",
    "Green Acres": "Green Acres Fraser's Hill",
    "The Hill": "The Hill at Fraser Hill",
    "80 Colonie": "Colonie Fraser's Hill",
    "The Smokehouse": "The Smokehouse Fraser's Hill"
}

def location_url(location_keyname):
    location_query = LOCATIONS[location_keyname].split(" ")
    processed_query = "+".join(location_query)
    url = "https://www.google.com/maps/embed/v1/place?key=" + GOOGLE_MAP_API_KEY + "&q=" + processed_query
    return url


