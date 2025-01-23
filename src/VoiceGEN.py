from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os
import datetime
from AudioSave import upload_to_tmpfiles

# Load environment variables
load_dotenv()

def list_available_voices():
    """
    Retrieve and list all available voices from IBM Watson Text to Speech service.

    Returns:
    - list: A list of dictionaries containing voice names and their descriptions.
    """
    # Initialize IBM Watson Text to Speech
    authenticator = IAMAuthenticator(os.getenv('voiceAuth'))
    text_to_speech = TextToSpeechV1(authenticator=authenticator)
    text_to_speech.set_service_url(os.getenv('voice_URL'))

    # Get the list of available voices
    voices = text_to_speech.list_voices().get_result()

    # Format the voice data into a readable list
    voice_list = []
    for voice in voices['voices']:
        voice_list.append({
            'name': voice['name'],
            'language': voice['language'],
            'description': voice['description']
        })
    
    return voice_list

def text_to_speech_conversion(text, customerName,voice):
    """
    Convert text to speech using IBM Watson Text to Speech service and save the audio file.

    Parameters:
    - text (str): The text to be converted to speech.
    - output_folder (str): The folder where the audio file will be saved. Default is 'static/audio/'.

    Returns:
    - str: Path of the saved audio file.
    """
    # Initialize IBM Watson Text to Speech
    authenticator = IAMAuthenticator(os.getenv('voiceAuth'))
    text_to_speech = TextToSpeechV1(authenticator=authenticator)
    text_to_speech.set_service_url(os.getenv('voice_URL'))

    # Get current date and time to include in the filename
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Define the temporary file path
    temp_audio_path = f"{current_datetime}_{customerName}.mp3"

    # Synthesize the speech and save to a temporary audio file
    with open(temp_audio_path, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                voice=voice,
                accept='audio/mp3'
            ).get_result().content
        )

    # Upload to tmpfiles.org
    try:
        direct_url = upload_to_tmpfiles(temp_audio_path)
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

    return direct_url

# # Example Usage
# if __name__ == "__main__":
#     # List available voices
#     voices = list_available_voices()
#     for voice in voices:
#         print(f"Name: {voice['name']}, Language: {voice['language']}, Description: {voice['description']}")

#     # Convert text to speech (example)
#     example_text = "Hello, welcome to IBM Watson Text to Speech service!"
#     customer_name = "JohnDoe"
#     audio_file_path = text_to_speech_conversion(example_text, customer_name)
#     print(f"Audio file saved at: {audio_file_path}")
