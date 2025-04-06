import os
import logging
import cv2
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import requests
import json

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to log messages both to console and logging service
def log(category, content):
    print(f'{category}: {content}')
    logging.info(f'{category}: {content}')
    send_log_to_logging_service(category, content)

# Function to send logs to an external logging service
def send_log_to_logging_service(category, content):
    try:
        logging_service_url = 'http://localhost:25580/log'  # Update with logging service URL
        log_message = {'category': category, 'content': content}
        response = requests.post(logging_service_url, json=log_message)
        if response.status_code != 200:
            print(f'Failed to send log to logging service: {response.text}')
    except Exception as e:
        print(f'Error sending log to logging service: {e}')

# Function to load an image from file path
def load_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or the file format is not supported")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        log('App', f'Error loading image {image_path}: {e}')
        raise

# Function to apply KMeans clustering to the image and return dominant colors
def apply_kmeans(image, k=5):
    try:
        reshaped_image = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=k, random_state=0).fit(reshaped_image)
        return kmeans.cluster_centers_
    except Exception as e:
        log('App', f'Error applying KMeans: {e}')
        raise

# Function to enhance colors by increasing saturation and value
def enhance_colors(colors):
    enhanced_colors = []
    for color in colors:
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        hsv_color[1] = min(hsv_color[1] * 1.25, 255)  # Increase saturation
        hsv_color[2] = min(hsv_color[2] * 1.10, 255)  # Increase brightness
        rgb_color = cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2RGB)[0][0]
        enhanced_colors.append(rgb_color)
    return enhanced_colors

# Function to filter out unwanted colors based on HSV ranges and darkness threshold
def filter_colors(colors, ranges_to_ignore, darkness_threshold):
    filtered_colors = []
    for color in colors:
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        if hsv_color[2] < darkness_threshold:  # Skip dark colors
            continue
        ignore = any(all(r[0] <= ch <= r[1] for ch, r in zip(hsv_color, range_to_ignore)) for range_to_ignore in ranges_to_ignore)
        if not ignore:
            filtered_colors.append(color)
    return filtered_colors

# Function to convert RGB to HEX format
def rgb_to_hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

# Route to check if the API is healthy
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Route to handle image processing requests
@app.route('/api/process-image', methods=['POST'])
def handle_image_processing():
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['imageFile']
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400

    try:
        # Save the image temporarily
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        
        log('Processing', f'Processing image: {filename}')
        
        # Process the image and extract top colors
        color_codes = process_image(image_path, k=3)  # Adjust k value as needed

        # Extract user info from the request
        user_info = json.loads(request.form.get('userInfo'))  # Parse JSON string to dictionary
        print('User info received:', user_info)
        print('Color codes received:', color_codes)
        
        # Delete the temporary image file
        os.remove(image_path)
        
        log('ImageProcess', f'Successfully processed image: {filename}')
        
        # Prepare the response data
        response_data = {"message": "Image processed successfully", "colorCodes": color_codes, "imageName": filename}
        
        # Send user info and image data to the database service
        send_to_database(json.dumps(user_info), response_data)
        
        print('Response data:', response_data)
        
        return jsonify(response_data), 200

    except Exception as e:
        log('App', f'Error processing image: {e}')
        return jsonify({"error": "Failed to process image"}), 500

# Function to process the image and extract dominant color codes
def process_image(image_path, k=5, ranges_to_ignore=None, darkness_threshold=30):
    try:
        # Default ranges to ignore specific color ranges (e.g., too dark/light)
        if ranges_to_ignore is None:
            ranges_to_ignore = [((90, 140), (10, 255), (50, 255)), ((0, 180), (0, 50), (50, 80))]
        
        image = load_image(image_path)
        dominant_colors = apply_kmeans(image, k)
        enhanced_colors = enhance_colors(dominant_colors)
        preferred_colors = filter_colors(enhanced_colors, ranges_to_ignore, darkness_threshold)
        
        # Sort colors by their brightness (HSV value)
        preferred_colors_sorted = sorted(preferred_colors, key=lambda c: cv2.cvtColor(np.uint8([[c]]), cv2.COLOR_RGB2HSV)[0][0][2], reverse=True)
        
        # Extract the top 3 color codes in HEX format
        top_3_colors_hex = [rgb_to_hex(color) for color in preferred_colors_sorted[:3]]
        
        log('App', f'Processed image {image_path} and extracted top 3 color codes.')
        return top_3_colors_hex
    except Exception as e:
        log('App', f'Error processing image {image_path}: {e}')
        raise

# Function to send user info and image data to the database service
def send_to_database(user_info, image_data):
    try:
        print('User info:', user_info)
        print('Image data:', image_data)
        
        # Send user info and image data to the database service
        database_url = 'http://localhost:25576/api/save-image'  # Update with database service URL
        payload = {'userInfo': user_info, 'imageData': image_data}
        response = requests.post(database_url, json=payload)
        if response.status_code != 200:
            log('App', f'Failed to send data to database: {response.text}')
    except Exception as e:
        log('App', f'Error sending data to database: {e}')

# Run the Flask app
if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Start the Flask server
    app.run(host='localhost', port=25577, debug=True)