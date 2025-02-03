from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_marketing_message_mistral(customer_name, residence, employment, selected_voice, card_type, category, link, title, details):
    # Set up credentials
    credentials = Credentials(
        url=os.getenv('Pay_url_Watsonx'),  # Replace with your IBM Cloud URL
        api_key=os.getenv('Pay_API_KEY_Watsonx')  # Replace with your API key
    )

    model_id = "mistralai/mistral-large"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 900,
        "min_new_tokens": 0,
        "repetition_penalty": 1
    }

    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=os.getenv('Pay_PROJECT_ID_Watsonx'),  # Replace with your Project ID
        space_id=os.getenv('space_id')  # Replace with your Space ID
    )

    # Construct the prompt
    prompt_input = f"""
    You are a marketing specialist tasked with creating engaging and professional promotional content. Please generate a concise and compelling marketing message for the following scenario. Adhere strictly to the given format and include all specified sections without any deviation. Use persuasive and positive language suitable for a premium audience.

### Details:
- **Customer Name:** {customer_name}
- **Card Type:** {card_type}
- **Category:** {category}
- **Title:** {title}
- **Details:** {details}
- **Link:** {link}
- **residence** {residence}
- **employment** {employment}
- **selected_voice** {selected_voice}

### Required Format:
**Headline:** Capture the reader's attention with an engaging headline related to luxury and exclusivity.

**Body:** Address the customer by name ,residence,employment and describe the exclusive offer. Clearly mention the card type, category, and offer details. Emphasize the exclusivity and the luxurious experience awaiting them. Ensure the tone shoude be selected_voice, and inviting.

**Call to Action:** Conclude with a compelling call to action, encouraging the customer to apply for their BOC Premium Card. Include the provided link for further action.

### Strict Instructions:
- **Only generate ONE marketing message.**  
- **Do not include "Marketing Message:", notes, explanations, or extra text.**
- **Output must be strictly in the format below. No variations.** 
- **Only one output not a more only one.** 

### Expected Output:

**Headline:** "Unlock Exclusive Rewards with Your {card_type}!" 

**Body:** (max 80 words) "Dear {customer_name}, as a {employment} resident of {residence}, your {card_type} unlocks premium {category} privileges. Enjoy {details} designed to enhance your experience. This exclusive offer, tailored to your {selected_voice} preferences, is available for a limited time—don’t miss out!"  

**Call to Action:** "Claim your exclusive benefits today: {link}"

Important: Stick to the required format, using professional language and focusing only on the given details. Do not include additional text or unrelated content.
"""

    try:
        # Generate the response
        print(prompt_input)
        generated_response = model.generate_text(prompt=prompt_input, guardrails=True)

        # if not generated_response:
        #     # print("API response is empty.")
        #     print(f"Generated response: {generated_response}")  # Add this line to check the content of the response

        return generated_response
    
    except Exception as e:
        # print(f"Error generating marketing message: {e}")
        return "Error: Watsonx.ai API request failed."

