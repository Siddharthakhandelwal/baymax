import requests
import json

def mri():
    api_url="http://localhost:5000/mri"

    try:
        # Send POST request to the API endpoint
        response = requests.post(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            print(f"Response: {response.text}")
            
            # Try to parse JSON response if available
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=4)}")
                return json_response
            except json.JSONDecodeError:
                print("Response is not in JSON format")
                return response.text
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

