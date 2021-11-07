import os
import numpy as np
import tensorflow.compat.v1 as tf
from keras import backend as K
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, VGG16

UPLOAD_FOLDER_ENTER = './image_enter' # 入力の画像フォルダ
IMAGE_FOLDER_REFERENCE = './image_reference' # 比べる画像のフォルダ

reference_dict = {} # 比較する画像 key=path, value=ベクトル

def preprocess_input(x, data_format=None, version=1):
    K.clear_session()
    x_temp = np.copy(x)
    if data_format is None:
        data_format = K.image_data_format()
    assert data_format in {'channels_last', 'channels_first'}

    if version == 1:
        if data_format == 'channels_first':
            x_temp = x_temp[:, ::-1, ...]
            x_temp[:, 0, :, :] -= 93.5940
            x_temp[:, 1, :, :] -= 104.7624
            x_temp[:, 2, :, :] -= 129.1863
        else:
            x_temp = x_temp[..., ::-1]
            x_temp[..., 0] -= 93.5940
            x_temp[..., 1] -= 104.7624
            x_temp[..., 2] -= 129.1863

    elif version == 2:
        if data_format == 'channels_first':
            x_temp = x_temp[:, ::-1, ...]
            x_temp[:, 0, :, :] -= 91.4953
            x_temp[:, 1, :, :] -= 103.8827
            x_temp[:, 2, :, :] -= 131.0912
        else:
            x_temp = x_temp[..., ::-1]
            x_temp[..., 0] -= 91.4953
            x_temp[..., 1] -= 103.8827
            x_temp[..., 2] -= 131.0912
    else:
        raise NotImplementedError
    K.clear_session()
    return x_temp


def to_vector():
    for references_file in os.listdir(IMAGE_FOLDER_REFERENCE):
        img_path = os.path.join(IMAGE_FOLDER_REFERENCE,references_file)
        book_img = image.load_img(img_path, target_size=(224,224))
        x = image.img_to_array(book_img) #モデルが認識できる形式に画像を変換する
        x = x[np.newaxis, ...] # 複数の画像が読み込めるよう、n * height * width * channelの入力をとるようになっているため、軸を一つ加えている
        x = preprocess_input(x) # 画像の前処理を行い、前処理済みの画像をxという変数に格納する
        book_img_arrays = image.img_to_array(book_img) # 画像を行列にする
        reference_book_array = preprocess_input(book_img_arrays, version=2) # 前処理
        reference_dict[references_file] = reference_book_array # 辞書に登録