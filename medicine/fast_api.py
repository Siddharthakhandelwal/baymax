import requests
prompt="hi"
def get_response(prompt):
    api_url = "http://192.168.29.146:5000"
    payload = {'prompt': prompt}

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raises an error for HTTP error responses
        print(response.json().get('response'))
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the server. Make sure the server is running.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Try increasing the timeout or checking the server.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

get_response(prompt)
