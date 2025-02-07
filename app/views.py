from flask import request, render_template, session, send_from_directory, redirect, url_for
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image
import os
from app import app

api = Api(app)

# Configurations
app.config['SECRET_KEY'] = "yldZ-Jzfj7DAqfnRmsub8Q"
UPLOAD_FOLDER = "./app/static/img/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# YOLO Models
model_4_points = YOLO('./app/static/models/model-4-points.pt')
model_6_points = YOLO('./app/static/models/model-6-points.pt')

@app.route("/")
@app.route("/Home")
def home():
    return render_template("Home.html")

@app.route("/About")
def About():
    return render_template("About.html")

@app.route("/ContactUs")
def Contact_Us():
    return render_template("ContactUs.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

class UploadImage(Resource):
    def post(self):
        file = request.files['file']

        if file.filename == '':
            return {'success': False, 'message': 'No selected file'}, 400

        if file:
            filename = secure_filename(file.filename)
            if filename.lower().endswith(('.png', '.jpeg', '.bmp', '.tiff', '.webp')):
                new_filename = os.path.splitext(filename)[0] + ".jpg"
                filename=new_filename
            try:
                # Open the file and check its metadata using Pillow
                with Image.open(file) as img:
                    # Ensure the image format is valid
                    if img.format not in ('JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP'):
                        return {'success': False, 'message': 'Invalid image format'}, 400
                    # If the image has an alpha channel (RGBA), convert it to RGB
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    # Save the file in the desired folder
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    img.save(file_path)
                    
                    # Save the filename in the session
                    session['uploaded_file'] = filename
                    return {'success': True, "message": "File is a valid image", "file_path": filename}, 201

            except Exception as e:
                # Handle cases where the file cannot be opened or is not an image
                return {'success': False, "message": f"File validation failed: {str(e)}"}, 400

        return {'success': False, "message": "File upload failed"}, 400


@app.route('/results')
def results():
    image_name = session.get('uploaded_file', None)
    if not image_name:
        return redirect(url_for('upload'))  # Redirect to upload page if no file uploaded

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    # Split the path into components
    path_parts = app.config['UPLOAD_FOLDER'].split("/")
    
    # Remove the first two components
    updated_path = "/".join(path_parts[:-1])
    # Define custom directory for predictions
    prediction_dir_4 = os.path.join(updated_path, 'prediction_4points')
    os.makedirs(prediction_dir_4, exist_ok=True)
    prediction_dir_6 = os.path.join(updated_path, 'prediction_6points')
    os.makedirs(prediction_dir_6, exist_ok=True)

    # Run YOLOv8 inference
    results = model_4_points.predict(source=file_path, save=True, project=prediction_dir_4, name='predict')
    results1 = model_6_points.predict(source=file_path, save=True, project=prediction_dir_6, name='predict')

    str_path = results[0].save_dir
    # Convert backslashes to forward slashes
    str_path = str_path.replace("\\", "/")
    
    # Split the path into components
    path_parts = str_path.split("/")
    
    # Remove the first two components
    updated_path = "/".join(path_parts[2:])

    str_path1 = results1[0].save_dir
    # Convert backslashes to forward slashes
    str_path1 = str_path1.replace("\\", "/")
    
    # Split the path into components
    path_parts1 = str_path1.split("/")
    
    # Remove the first two components
    updated_path2 = "/".join(path_parts1[2:])

    return render_template('results.html', prediction_path=updated_path, image_name=image_name, prediction_path2=updated_path2)


class ServeUploads(Resource):
    def get(self, filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Add Resources to API
api.add_resource(UploadImage, '/upload_img')
api.add_resource(ServeUploads, '/uploads/<filename>')
