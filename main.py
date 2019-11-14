import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'xlsx', 'xls'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	print(request.cookies)
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File {} successfully uploaded to {}'.format(filename, os.path.dirname(os.path.abspath(__file__)))})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, csv, xlsx, xls'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0')