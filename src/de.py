from discovery import get_crwlinformation
import random




def random_selected_title(card_type, category):
    """Fetches offers and selects a random title from the first 20 results."""
    if get_crwlinformation is None:
        return {"title": "No offers available", "offer_details": "N/A"}

    offers = get_crwlinformation(card_type, category)
    
    if not offers:
        return {"title": "No offers available", "offer_details": "N/A"}

    selected_offer = random.choice(offers[:20]) if len(offers) >= 20 else random.choice(offers)

    return {
        "title": selected_offer.get("title", "N/A"),
        "offer_details": selected_offer.get("offer_details", "N/A") or "No details available"
    }


