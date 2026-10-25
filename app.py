import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

items_db = [
    {
        "id": 1,
        "title": "Sample Item with Image",
        "description": "This item has an image",
        "imageUrl": ""
    }
]

@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify({"status": "success", "data": items_db}), 200

@app.route("/api/items", methods=["POST"])
def create_item_with_image():

    title = request.form.get("title", "Untitled")
    description = request.form.get("description", "")
    
    image_url = ""
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)
            
            image_url = f"http://127.0.0.1:5000/api/uploads/{filename}"

    new_item = {
        "id": len(items_db) + 1,
        "title": title,
        "description": description,
        "imageUrl": image_url
    }
    
    items_db.append(new_item)
    
    return jsonify({
        "status": "success",
        "message": "Item and image uploaded successfully",
        "data": new_item
    }), 201

@app.route("/api/uploads/<filename>", methods=["GET"])
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)