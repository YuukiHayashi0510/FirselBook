# vect2.py title_to_vector

import numpy as np
import pandas as pd
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


def wakachi(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    docs=[]
    for token in tokens:
        docs.append(token.surface)
    return docs

def vecs_array(documents):
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()


def title_to_vector():
    df_title = pd.read_excel('NovelComics.xlsx', index_col=0, usecols=['Title'])
    vector = [0] * 10
    for i in range(10):
        vector[i] = vecs_array(wakachi(df_title.index.values[i]))
    return vector

df = pd.read_excel('NovelComics.xlsx')

vector = title_to_vector()

for i,j in enumerate(vector):
    df.at[i, 'Vector'] = j
print(df)