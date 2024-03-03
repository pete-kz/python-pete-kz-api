from flask import Flask, request, jsonify
import boto3
import uuid

app = Flask(__name__)

# Configure these with your AWS access key, secret key, and bucket name
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_KEY'
S3_BUCKET_NAME = 'YOUR_BUCKET_NAME'

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = str(uuid.uuid4()) + '-' + file.filename
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

if __name__ == '__main__':
    app.run(debug=True)
