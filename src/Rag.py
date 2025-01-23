from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_marketing_message_mistral(customer_name, discount, hotel_name, start_date, end_date, link):
    # Set up credentials
    credentials = Credentials(
        url=os.getenv('IBM_CLOUD_URL'),  # Replace with your IBM Cloud URL
        api_key=os.getenv('API_KEY'),   # Replace with your API key
    )

    # Specify model_id for inferencing
    model_id = "mistralai/mistral-large"

    # Define model parameters
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 900,
        "min_new_tokens": 0,
        "repetition_penalty": 1
    }

    # Initialize ModelInference
    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=os.getenv('PROJECT_ID'),  # Replace with your Project ID
        space_id=os.getenv('space_id')      # Replace with your Space ID
    )

    # Prepare the prompt for the model
    prompt_input = f"""Using the directions below, generate only one marketing message in a clear and structured manner.

    # Task Description:
    # Write a marketing message with the following structure:
    # - Headline: A short, catchy phrase that highlights the offer.
    # - Body: A detailed message explaining the offer, including the discount, product/service details, and validity period.
    # - Call to Action: A clear instruction encouraging the customer to act, such as applying for a card or visiting a link.

    # Input Details:
    # customer_name: {customer_name}
    # discount: {discount}%
    # hotel_name: {hotel_name}
    # start_date: {start_date}
    # end_date: {end_date}
    # link: {link}

    # Example Output (single response):
    # Headline: Unlock Exclusive Rewards with Your BOC Premium Card!
    # Body: Dear {customer_name}, we’re excited to offer you an exclusive {discount}% discount at {hotel_name}, 
    #       available for full board, half board, and bed & breakfast options. 
    #       This limited-time offer is exclusively for BOC Credit & Debit Cardholders and is valid 
    #       from {start_date} to {end_date}. Don’t miss this chance to enjoy a luxurious getaway at a special rate.
    # Call to Action: Apply for your BOC Premium Card now and start enjoying amazing benefits! 
    #                 Visit {link} to apply today.

    # Do not generate multiple versions, only produce a single, formatted marketing message.
"""
    # Generate the response
    generated_response = model.generate_text(prompt=prompt_input, guardrails=True)
    return generated_response


    
