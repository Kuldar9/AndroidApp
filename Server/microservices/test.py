import requests
import json

# Set the URL of the Flask server
url = 'http://localhost:25577/api/process-image'

# Set the path to the image file you want to process
image_path = 'image.jpg'

# User information
user_info = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "$2b$10$ETOpWoqnx/v51qxEzmnJL.7tH7oWoi.tdc2dNtO3fWzzqlT9MeZgu",
    "images": []
}

# Open the image file
with open(image_path, 'rb') as file:
    # Create a dictionary containing the file and user info to be sent
    files = {'imageFile': file}
    data = {'userInfo': json.dumps(user_info)}  # Convert user_info to JSON string

    # Print out user_info and image_data before sending
    print('User info sent:', user_info)
    print('Image data sent:', image_path)

    # Send the POST request to the server
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("Image processed successfully.")
            print(response.json())
        else:
            print("Failed to process image.")
            print("Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)