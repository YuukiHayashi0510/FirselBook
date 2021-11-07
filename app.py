import os
import sys 
import tensorflow.compat.v1 as tf

from flask import (
    Flask, 
    request, 
    redirect, 
    url_for, 
    make_response, 
    jsonify, 
    render_template, 
    send_from_directory)
from keras.applications.vgg16 import VGG16, decode_predictions

from vect import to_vector

UPLOAD_FOLDER_ENTER = './image_enter'
IMAGE_FOLDER_REFERENCE = './image_reference'

entry_dict = {} # アップロードする画像 key=path, value=ベクトル
reference_dict = {} # 比較する画像 key=path, value=ベクトル

for references_file in os.listdir(IMAGE_FOLDER_REFERENCE):
    reference_img_path = os.path.join(IMAGE_FOLDER_REFERENCE, references_file)
    to_vector(references_file, reference_dict, reference_img_path)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        enter_images=os.listdir(UPLOAD_FOLDER_ENTER)[::-1],
        reference_images=os.listdir(IMAGE_FOLDER_REFERENCE)[::-1])

@app.route('/upload', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'upload_files' not in request.files:
            print("ファイルなし")
            return redirect(request.url)

        if request.files.getlist('upload_files')[0].filename:
            #画像オブジェクトを受け取る。
            uploads_files = request.files.getlist('upload_files')
            for uploads_file in uploads_files:
                #それぞれの画像に対してimage_enterまでのパスを定義作成してsaveメソッドを用いて保存する。
                img_path = os.path.join(UPLOAD_FOLDER_ENTER, uploads_file.filename)
                uploads_file.save(img_path)
                to_vector(uploads_file, entry_dict, img_path)
        return redirect('/')

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(UPLOAD_FOLDER_ENTER, path)

#スクリプトからAPIを叩けるようにします。
if __name__ == "__main__":
    app.run(debug=True)