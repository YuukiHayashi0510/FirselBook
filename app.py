import os
import math
from flask import (
    Flask,
    request,
    redirect,
    render_template)
from vect import to_vector
from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np

UPLOAD_FOLDER_ENTER = './static/images/image_enter'
IMAGE_FOLDER_REFERENCE = './static/images/image_reference'

entry_dict = {} # アップロードする画像 key=path, value=ベクトル
reference_dict = {} # 比較する画像 key=path, value=ベクトル
num_image_dict = {}

df = pd.read_csv('./static/csv/enter_book.csv')
df_dict = df.to_dict(orient='dict')
title = df_dict['title']
num = df_dict['circulation']

for i in range(len(num)):
    num_image_dict[title[i]] = num[i]

df_ref = pd.read_csv('./static/csv/reference_book.csv')
for i in range(len(df_ref)-1):
    reference_dict[df.loc[i,:].values[0]] = df.loc[i,:].values[1:].tolist()


def get_similarity(entry_vector, reference_vector):
    """
    cos類似度を求める関数

    Parameters
    ----------
    entry_vector : vector
        アップロードした本のベクトル
    reference_vector : vector
        比較元の本のベクトル
    """
    return 1 - cosine(entry_vector, reference_vector)


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
                #最も似ている画像へのパスと類似度を保存するための変数
                most_similar_img = ''
                max_similarity = 0
                for r_path, r_vector in reference_dict.items():
                    tmp = np.array(r_vector)
                    if get_similarity(entry_dict[uploads_file], tmp) > max_similarity:
                        max_similarity = get_similarity(entry_dict[uploads_file], tmp)
                        most_similar_img = r_path
                        num_circ = num_image_dict[most_similar_img]
                filename = most_similar_img.split('//')[-1] #windowsは//, macは\\
                result = num_circ * max_similarity
                return render_template(
                    'result.html',
                    filename=filename,
                    score=math.floor(max_similarity*100),
                    num_circ=num_circ,
                    result=math.floor(result)
                )



#スクリプトからAPIを叩けるようにします。
if __name__ == "__main__":
    app.run(debug=True,port=8000)