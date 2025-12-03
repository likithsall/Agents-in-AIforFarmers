!pip install requests opencv-python
import requests

def upload_image_from_device(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return image_file.read()
    except FileNotFoundError:
        print(f"File '{image_path}' not found.")
        return None

def detect_crop_disease(image_data, api_key):
    api_url = 'https://api.gemini15pro.com/predict'  # Ensure this URL is correct
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'image/jpeg'
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=image_data)
        if response.status_code == 200:
            api_response = response.json()
            disease = api_response.get('disease')
            actions = api_response.get('actions')
            result = {
                'disease': disease,
                'actions': actions
            }
            return result
        else:
            error_msg = f"Failed to predict: {response.status_code} - {response.text}"
            return {'error': error_msg}
    except requests.exceptions.RequestException as e:
        return {'error': f"Error with API request: {e}"}

def handle_detection_result(result):
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Detected Disease/Pest: {result['disease']}")
        print("Recommended Actions:")
        for action in result['actions']:
            print(f"- {action}")

def handle_image_upload(api_key, image_path):
    image_data = upload_image_from_device(image_path)
    if image_data:
        result = detect_crop_disease(image_data, api_key)
        handle_detection_result(result)
    else:
        print("Failed to upload image.")

import ast
import os
import google.generativeai as genai

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
genai.configure(api_key="AIzaSyAwTrLqf_Kpq4jvXDOtls9EqpkjKzCGlu0")
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def detect_crop_disease2(image_fpath):
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 5,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    files = [upload_to_gemini(image_fpath),]

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [files[0],],
        },
    ]
    )

    input_prompt = """
    You're provided with an image of leaf. You're supposed to analyse the image and return a json response in the below format
    {
    'disease': <Type of disease identified>,
    'actions': <Steps to be taken to cure the disease identified>
    }

    Instructions:
    - If the leaf is healthy, then return the below response
    {
    'disease': "Healthy",
    'actions': "No Action Needed"
    }
    
    - If you can't identify the disease, then return the below response
    {
    'disease': "Unidentifiable",
    'actions': "NA"
    }
    """
    try:
        response = chat_session.send_message(input_prompt)
    except:
        return {'error': f"Error with API request: {e}"}
    
    response_dict = ast.literal_eval(response.text)
    return response, response_dict
_, disease_info = detect_crop_disease2(r"C:\Users\ushac\Downloads\disease.jpg")
disease_info
