from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

async def generate_marketing_message_llama(customer_name, residence, employment, selected_voice, card_type, category, link, title, details):
    await asyncio.sleep(2)

    # Set up credentials
    credentials = Credentials(
        url=os.getenv('Pay_url_Watsonx'),  # Replace with your IBM Cloud URL
        api_key=os.getenv('Pay_API_KEY_Watsonx')  # Replace with your API key
    )

    # Specify model_id for inferencing
    #model_id = "meta-llama/llama-3-3-70b-instruct"
    model_id = "meta-llama/llama-3-2-11b-vision-instruct"

    # Define model parameters
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 0,
        "repetition_penalty": 1
    }

    # Initialize ModelInference
    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=os.getenv('Pay_PROJECT_ID_Watsonx'),  # Replace with your Project ID
        space_id=os.getenv('space_id')  # Replace with your Space ID   
    )

    # Prepare the prompt for the model
    prompt_input = f"""
You are a marketing specialist tasked with creating engaging and professional promotional content. Generate a concise and compelling marketing message for the following scenario. Adhere strictly to the given format and include all specified sections without any deviation. Use persuasive and positive language suitable for a premium audience while ensuring the tone matches the selected voice.

### Details:
- Customer Name: {customer_name}
- Residence: {residence}
- Employment: {employment}
- Selected Voice (Tone): {selected_voice}
- Card Type: {card_type}
- Category: {category}
- Title: {title}
- Details: {details}
- Link: {link}

### Required Format:
No code is required for this task. The final answer is:  

**Headline:** A short, engaging headline (max 10 words) that highlights the offer.  

**Body:** (max 80 words) Address the customer by name and describe the exclusive offer. Clearly mention the card type, category, and offer details while naturally incorporating their residence and employment status, ensuring the tone matches the selected voice to create a tailored experience that resonates with the customer; emphasize exclusivity, luxury, and the premium benefits awaiting them, maintaining a persuasive and professional tone throughout in a **single continuous sentence** without unnecessary spaces or separators.  

**Call to Action:** Conclude with a compelling call to action, encouraging the customer to apply for their BOC Premium Card. Include the provided link for further action.  

### Sample Output:
No code is required for this task.  

**Headline:** Exclusive Travel Offers with World Master Card  

**Body:** Dear AHANGANGODA, enjoy the luxury of your World Master Card from the Travelling category, offering you an exclusive 20% off on full board, half board, and bed & breakfast basis at Joe’s Resort Bentota, a premium experience tailored to enhance your travel and leisure activities with BOC credit card offers, valid from 04th September 2024 to 30th April 2025.  

**Call to Action:** Apply now for your BOC Premium Card here: https://www.boc.lk/personal-banking/cards/credit-cards/world-master-card  

### STRICT INSTRUCTIONS (DO NOT VIOLATE):
1. No code is required for this task. Ensure the output does **not** appear as code.  
2. Generate **only ONE marketing message**. Do not repeat it again and again.  
3. Do **NOT add any extra text** such as "Marketing Message:", "Output:", or any explanatory content.  
4. Maintain the **exact structured format** below. Do not add formatting changes.  
5. No bullet points, no additional labels, and no extra words.  
6. The "Body" must be a **single continuous sentence** without unnecessary spaces or separators.  
7. End with the call to action, including the provided link.
8. Do **NOT** Print Again And Again Body,Call to Action Headline only Print one Time  
9. Only one output not a more only one.
10.Do **NOT** print **The final answer is:**

### Important:
The final output must strictly follow the same structured format as the sample. Do not include additional text or unrelated content. Focus only on the given details.
"""







    # Generate the response
    generated_response = model.generate_text(prompt=prompt_input, guardrails=True)
    return generated_response

    


