from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_marketing_message_llama(customer_name, discount, hotel_name, start_date, end_date, link):
    # Set up credentials
    credentials = Credentials(
        url=os.getenv('IBM_CLOUD_URL'),  # Replace with your IBM Cloud URL
        api_key=os.getenv('API_KEY'),   # Replace with your API key
    )

    # Specify model_id for inferencing
    model_id = "meta-llama/llama-3-1-70b-instruct"
    # model_id = "meta-llama/llama-3-2-90b-vision-instruct"

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
    prompt_input = f"""
You are a marketing specialist tasked with creating engaging and professional promotional content. Please generate a concise and compelling marketing message for the following scenario. Adhere strictly to the given format and include all specified sections without any deviation. Use persuasive and positive language suitable for a premium audience.

### Details:
- **Customer Name:** {customer_name}
- **Discount:** {discount}%
- **Hotel Name:** {hotel_name}
- **Start Date:** {start_date}
- **End Date:** {end_date}
- **Link:** {link}

### Required Format:
**Headline:** Capture the reader's attention with an engaging headline related to luxury and exclusivity.

**Body:** Address the customer by name and describe the exclusive offer. Clearly mention the discount, hotel name, and the duration of the offer. Emphasize the exclusivity and the luxurious experience awaiting them. Ensure the tone is positive, professional, and inviting.

**Call to Action:** Conclude with a compelling call to action, encouraging the customer to apply for their BOC Premium Card. Include the provided link for further action.

Important: Stick to the required format, using professional language and focusing only on the given details. Do not include additional text or unrelated content.
"""

    # Generate the response
    generated_response = model.generate_text(prompt=prompt_input, guardrails=True)
    return generated_response


    
