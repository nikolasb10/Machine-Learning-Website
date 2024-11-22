import requests
import toml

# Load the TOML file
config = toml.load("./.streamlit/secrets.toml")

# Access the API key
huggingface_api_key = config["api_keys"]["HUGGINGFACE_API_KEY"]
headers = {"Authorization": f"Bearer {huggingface_api_key}"}

# Function to make requests to hugging face api
def make_hf_requests(model, payload):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
