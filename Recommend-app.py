import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from sqlalchemy import create_engine

# データを読み込み
df = pd.read_csv("https://files.grouplens.org/datasets/movielens/ml-100k/u.data", 
                 names=["user_id", "item_id", "review", "timestamp"], sep="\t")

# データの整形
df = pd.pivot_table(df.drop("timestamp", axis=1), index="user_id", columns="item_id", values="review")
df = df.fillna(0)

print(df)

# cos類似度をnumpyを使って計算
# dot =  np.dot(df.iloc[0], df.iloc[1])
# norm_a = np.linalg.norm(df.iloc[0])
# norm_b = np.linalg.norm(df.iloc[1])
# dot / (norm_a*norm_b)

## cos類似度をcosine_similarityを使って計算
# cosine_similarity([df.iloc[0], df.iloc[1]])

cos_list = []
for user_id in df.index:
    cos_list.append(cosine_similarity([df.loc[943, 1:]], [df.loc[user_id, 1:]]))

# sorted([ソートの対象], [ソートキー], reverse=True)
user_list = sorted(range(len(cos_list)), key=lambda i: cos_list[i], reverse=True)

user_sim10 = user_list[1:][:10]
print(user_sim10)
