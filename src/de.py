import random
from discovery import get_crwlinformation

def random_selected_title(card_type, category):
    """Fetches offers and selects a random title from the first 20 results."""
    
    # Fetch all titles and offer details
    offers = get_crwlinformation(card_type, category)
    
    # Debugging: Print retrieved offers
    # print(f"🔍 Retrieved {len(offers)} offers for {card_type} - {category}")

    # Check if offers are available
    if not offers:
        # print("⚠️ No offers found.")
        return {"title": "No offers available", "offer_details": "N/A"}

    # Select a random offer from the first 20 results (if available)
    selected_offer = random.choice(offers[:20]) if len(offers) >= 20 else random.choice(offers)

    # Debugging: Print selected offer
    # print(f"✅ Selected Offer:\nTitle: {selected_offer.get('title', 'N/A')}\nDetails: {selected_offer.get('offer_details', 'N/A')}")

    # Return selected offer as a dictionary
    return {
        "title": selected_offer.get("title", "N/A"),
        "offer_details": selected_offer.get("offer_details", "N/A")
    }


