import random
import spacy
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Load environment variables
load_dotenv()

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("⚠️ spaCy model 'en_core_web_lg' not found. Running without NLP features.")
    nlp = None

# Try importing the web crawling function
try:
    from discovery import get_crwlinformation
except ImportError:
    print("❌ Error: 'discovery' module not found. Ensure it is available.")
    get_crwlinformation = None


def get_coordinates(place_name):
    """Returns the latitude and longitude of a place."""
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(place_name)
    
    if location:
        return (location.latitude, location.longitude)
    return None


def extract_place_and_address(text, country="LK"):
    """Extracts places from the given text."""
    if not text.strip():
        return {"Places": []}

    places = []
    hotel_keywords = ["hotel", "resort", "villa", "inn", "lodge", "spa"]
    
    for line in text.split("\n"):
        if any(keyword.lower() in line.lower() for keyword in hotel_keywords):
            places.append(line.strip())
    
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["GPE", "FACILITY", "ORG"]:
                places.append(ent.text.strip())
    
    return {"Places": list(set(places))}  # Remove duplicates


def find_closest_offer(card_type, category, reference_location):
    """Finds the closest offer location to the reference location."""
    if get_crwlinformation is None:
        return {"title": "No valid offers found", "offer_details": "N/A", "distance": None}

    offers = get_crwlinformation(card_type, category)
    
    if not offers:
        return {"title": "No valid offers found", "offer_details": "N/A", "distance": None}
    
    random_5_offers = random.sample(offers, min(len(offers), 5))
    places_list = []
    
    for offer in random_5_offers:
        result = extract_place_and_address(offer["offer_details"])
        print(f"📍 Extracted Places for {offer['title']}: {result['Places']}")
        places_list.extend(result["Places"])
    
    if not places_list:
        return {"title": "No valid offers found", "offer_details": "N/A", "distance": None}
    
    reference_coords = get_coordinates(reference_location)
    if not reference_coords:
        return {"title": "Reference location not found", "offer_details": "N/A", "distance": None}
    
    closest_place = None
    min_distance = float("inf")
    closest_offer = None
    
    for offer in random_5_offers:
        result = extract_place_and_address(offer["offer_details"])
        for place in result["Places"]:
            place_coords = get_coordinates(place)
            print(f"📍 {place} Coordinates: {place_coords}")
            if place_coords:
                distance = geodesic(reference_coords, place_coords).kilometers
                if distance < min_distance:
                    min_distance = distance
                    closest_place = place
                    closest_offer = offer
    
    if closest_offer:
        return {
            "title": closest_offer["title"],
            "offer_details": closest_offer["offer_details"],
            "distance": round(min_distance, 2)
        }
    else:
        return {"title": "No valid offers found", "offer_details": "N/A", "distance": None}

# Example usage
# card_type = "Credit Card"
# category = "Hotels"
# reference_location = "Dehiwala"
# result = find_closest_offer(card_type, category, reference_location)
# print(result)
