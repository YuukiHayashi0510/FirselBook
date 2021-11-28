# vect2.py title_to_vector

import pandas as pd

df_title = pd.read_excel('NovelComics.xlsx', index_col=0, usecols=['Title'])

for i in range(60):
    print(df_title.iloc[i])
