import os
import math
from flask import (
    Flask, 
    request, 
    redirect, 
    render_template)
from vect import to_vector
from scipy.spatial.distance import cosine

UPLOAD_FOLDER_ENTER = './static/images/image_enter'
IMAGE_FOLDER_REFERENCE = './static/images/image_reference'

entry_dict = {} # アップロードする画像 key=path, value=ベクトル
reference_dict = {} # 比較する画像 key=path, value=ベクトル
num_image_dict = { 'ONEPIECE.jpg':490000000,'ゴルゴ13.jpg':300000000, 'ドラゴンボール.jpg':260000000, 
'NARUTO.jpg':250000000, '名探偵コナン.jpg':250000000,
'鬼滅の刃.jpg':150000000, '美味しんぼ.jpg':135000000, 'スラムダンク.jpg':120290000,
'BLEACH.jpg':120000000, 'ドラえもん.jpg':100000000, '鉄腕アトム.jpg':100000000,
'ジョジョの奇妙な冒険.jpg':100000000, 'タッチ.jpg':100000000,
'進撃の巨人.jpg':100000000, 'はじめの一歩.jpg':96000000,
'サザエさん.jpg':86000000, 'バキ.jpg':85000000, 'キングダム.jpg':83000000,
'キャプテン翼.jpg':80000000, 'キン肉マン.jpg':75000000,
'るろうに剣心.jpg':72000000, 'FAIRYTAIL フェアリーテイル.jpg':72000000
} # 部数と画像ファイルのパス

def start_up(): # アプリ起動前から完成(実行)しておきたい所...
    reference_dict.clear()
    for references_file in os.listdir(IMAGE_FOLDER_REFERENCE):
        reference_img_path = os.path.join(IMAGE_FOLDER_REFERENCE, references_file)
        to_vector(references_file, reference_dict, reference_img_path)


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

start_up()

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
                    if get_similarity(entry_dict[uploads_file], r_vector) > max_similarity:
                        max_similarity = get_similarity(entry_dict[uploads_file], r_vector)
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
                return redirect('/')



#スクリプトからAPIを叩けるようにします。
if __name__ == "__main__":
    app.run(debug=True)