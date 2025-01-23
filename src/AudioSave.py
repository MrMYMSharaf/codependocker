import requests
import os
# import streamlit as st


# # Streamlit file uploader
# uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

# if uploaded_file:
#     # Upload the file to tmpfiles.org
#     response = requests.post(
#         "https://tmpfiles.org/api/v1/upload",
#         files={"file": (uploaded_file.name, uploaded_file.read())},
#     )

#     if response.status_code == 200:
#         # Get the download link from the response
#         file_url = response.json()["data"]["url"]
#         st.success(f"File uploaded successfully: [Download here]({file_url})")

#         # Extract the direct playback URL
#         if "/dl/" not in file_url:
#             file_id = file_url.split('/')[-2]
#             file_name = file_url.split('/')[-1]
#             direct_url = f"https://tmpfiles.org/dl/{file_id}/{file_name}"
#         else:
#             direct_url = file_url

#         # Play the audio file directly from the URL
#         st.title("Streamlit Audio Player")
#         st.write("Playing your uploaded audio file:")
#         st.audio(direct_url, format="audio/mp3")
#         st.write(f"Direct Playback URL: {direct_url}")

#     else:
#         st.error("Failed to upload the file. Please try again.")


def upload_to_tmpfiles(file_path):
    with open(file_path, 'rb') as file_data:
        response = requests.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": (os.path.basename(file_path), file_data)},
        )
    if response.status_code == 200:
        file_url = response.json()["data"]["url"]
        if "/dl/" not in file_url:
            file_id = file_url.split('/')[-2]
            file_name = file_url.split('/')[-1]
            return f"https://tmpfiles.org/dl/{file_id}/{file_name}"
        return file_url
    else:
        raise Exception("Failed to upload the file to tmpfiles.org.")
