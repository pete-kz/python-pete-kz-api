from flask import Flask, request, jsonify
import boto3, uuid, os
from os.path import join, dirname
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)

ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_ENDPOINT = os.environ.get('S3_ENDPOINT') 
S3_BUCKET_DOMAIN = os.environ.get('S3_BUCKET_DOMAIN') 

s3_client = boto3.client('s3', 
                          endpoint_url=S3_ENDPOINT,
                          aws_access_key_id=ACCESS_KEY_ID, 
                          aws_secret_access_key=SECRET_ACCESS_KEY,
                        )

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    uploaded_files_urls = []
    for file in files:
        if file:
            filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.split(".")[-1])
            s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})
            file_url = f'{S3_BUCKET_DOMAIN}/{filename}'
            uploaded_files_urls.append(file_url)

    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files_urls}), 200

if __name__ == '__main__':
    app.run(debug=True)
