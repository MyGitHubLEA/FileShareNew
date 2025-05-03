from flask import Flask, jsonify, request, send_file, render_template, send_from_directory, redirect, url_for, flash 

import os 
import psutil 
import requests 
from minio import Minio
from dotenv import load_dotenv 
from urllib.request import urlopen 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from sqlalchemy import Column, Integer, String
from _init_ import app, db, login
from werkzeug.utils import secure_filename
from flask_login import UserMixin
from routes import register, login, logout
from urllib.parse import quote

LOCAL_FILE_PATH = os.environ.get('LOCAL_FILE_PATH') 
ACCESS_KEY = os.environ.get('ACCESS_KEY') 
SECRET_KEY = os.environ.get('SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000" 
MINIO_CLIENT = Minio("localhost:9000", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False) 
 

############################################################


@app.route("/", methods=["HEAD"]) 
def head():
  return (  jsonify({"message": "Hello, world"}),  200,  {"Content-Type": "application/json"},  ) 


@app.route("/", methods=["GET"]) 
@login_required
def index():  
  filenames = os.listdir(app.config['UPLOAD_FOLDER']) 
  user_prefix = f"{current_user.login}/"
  objects = MINIO_CLIENT.list_objects('mybucket', prefix=user_prefix, recursive=True)  
  filenames = [object.object_name.split('/')[-1] for object in objects if object.object_name.endswith('/') == False]  
  get_bucket_files()  
  return render_template('index.html', filenames=filenames, login = current_user.login), 200, {"Content-Type": "text/html"}



@app.route("/upload", methods=["POST"])
@login_required
def load_file():  
    if 'file' not in request.files: 
       return "Incorrect name"  
    file = request.files['file']
    if file.filename == '':  
       return "File was not chosen"  
    if file: 
        filename = secure_filename(file.filename)
        
        user_prefix = f"{current_user.login}/" 
        bucket_path = user_prefix + filename
        
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(local_path) 
        MINIO_CLIENT.fput_object("mybucket", bucket_path, local_path, file.mimetype)  
        os.remove(local_path) 
        
    return redirect('/')   



def get_bucket_files():  
   objects = MINIO_CLIENT.list_objects('mybucket', prefix=None, recursive = True)
   for obj in objects: print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,  obj.etag, obj.size, obj.content_type)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename): 
      user_prefix = f"{current_user.login}/" 
      bucket_path = user_prefix + filename
      res = MINIO_CLIENT.fget_object("mybucket", bucket_path, filename) 
      url = MINIO_CLIENT.get_presigned_url("GET",  "mybucket",  bucket_path,  )
      print('your url:', url)
      opened_url = urlopen(url) 
      return send_file(opened_url, mimetype=res.content_type) 



@app.route('/delete/<filename>', methods=['POST', 'GET'])
@login_required
def delete_file(filename):  
      user_prefix = f"{current_user.login}/" 
      bucket_path = user_prefix + filename
      MINIO_CLIENT.remove_object('mybucket', bucket_path)  
      print('Object removed successfully')  
      return redirect(url_for('index'))  #except ResponseError as err:  # print(err) ''' 


@app.route('/share/<filename>')
@login_required
def share_file(filename):
        user_prefix = f"{current_user.login}/"
        bucket_path = user_prefix + filename

        try:
            # Generate a presigned URL for the file.  This is the key to sharing.
            url = MINIO_CLIENT.get_presigned_url(
                "GET",
                "mybucket",
                bucket_path,
            )
            #  Present the pre-signed URL to the user - display the link directly, properly encoded
            quoted_url = quote(url, safe=':/')
            flash(f"Shareable link for {filename}: <a href='{quoted_url}'>{filename}</a>", "info") # Provide the link
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error generating shareable link: {str(e)}", "error")
            return redirect(url_for('index'))


if __name__ == "__main__":
      app.run(host='0.0.0.0')

      #os.makedirs(UPLOAD_FOLDER, exist_ok = True)  
