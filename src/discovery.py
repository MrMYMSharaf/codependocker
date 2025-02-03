from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

def get_crwlinformation(card_type, category):
    """Fetch and extract offer or reservation details based on credit card and category."""
    # Retrieve API credentials
    discovery_apikey = os.getenv('Discovery_API_KEY')
    url_discovery = os.getenv('discovery_URl')

    # Initialize Watson Discovery
    authenticator = IAMAuthenticator(discovery_apikey)
    watson_discovery = DiscoveryV2(version="2023-03-31", authenticator=authenticator)
    watson_discovery.set_service_url(url_discovery)

    # Define project ID
    project_id = os.getenv('Discovery_ProjectId')

    # List all collections
    collection_list = watson_discovery.list_collections(project_id=project_id).get_result()["collections"]

    if not collection_list:
        print("Error: No collections found.")
        return []

    # Function to run a query
    def discovery_query(query, collection_id, counter=200):  
        """Run a query in IBM Watson Discovery."""
        query_results = watson_discovery.query(
            project_id=project_id,
            collection_ids=[collection_id],
            natural_language_query=query,
            count=counter
        ).get_result()
        return query_results

    # Function to remove HTML tags
    def remove_html_tags(text):
        """Remove HTML tags from a given text."""
        if isinstance(text, str):
            return re.sub(r'<[^>]*>', '', text)
        return text

    # Function to extract offer or reservation details
    def extract_offer_or_reservation_details(query_response):
        """Extract title and offer/reservation details."""
        extracted_offers = []
        
        for result in query_response.get("results", []):
            title = remove_html_tags(result.get("title", "No title available"))
            content = result.get("text", "No information available")

            if isinstance(content, list):
                content = " ".join(content)

            content = remove_html_tags(content)

            offer_match = re.search(r"(\d+% OFF.*?\d{2}th \w+ \d{4})", content, re.DOTALL)
            reservation_match = re.search(r"(Reservations\s*[:\-]\s*[\d\s\|]+)", content)

            extracted_text = ""
            if offer_match:
                start = max(0, offer_match.start() - 300)
                end = min(len(content), offer_match.end() + 300)
                extracted_text = content[start:end]
            elif reservation_match:
                start = max(0, reservation_match.start() - 300)
                end = min(len(content), reservation_match.end() + 300)
                extracted_text = content[start:end]
            
            if extracted_text:
                extracted_offers.append({
                    "title": title,
                    "offer_details": extracted_text
                })
        
        return extracted_offers

    # Fetch data from all collections
    all_offers = []
    for collection in collection_list:
        collection_id = collection['collection_id']
        query = f"{card_type} + {category}"

        # Run the query
        query_results_discovery = discovery_query(query, collection_id)

        # Extract offer details
        offer_details = extract_offer_or_reservation_details(query_results_discovery)

        all_offers.extend(offer_details)

    return all_offers
