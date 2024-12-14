import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from sqlalchemy import create_engine
import json
from db_control import crud, mymodels
from sentence_transformers import SentenceTransformer

## レコメンドエンジン
model = mymodels.Customers
results = crud.myselectAll(mymodels.Customers)
print(results)

# データを読み込み
json_results = json.loads(results)
df = pd.json_normalize(json_results)
print(df)

# データの整形
df_input = df.drop(columns=["user_name", "company_name", "email", "password", "company_url"])
# df_review = df_input.fillna(0)
print(df_input[['entry_title', 'entry_description', 'entry_achievement', 'strength', 'tags']])

# モデルをロード
model = SentenceTransformer('all-MiniLM-L6-v2')

# 複数のカラムを一文につなげてリスト化
texts = df_input[['entry_title', 'entry_description', 'entry_achievement', 'strength', 'tags']].apply(
    lambda row: ' '.join(row.values.astype(str)), axis=1
).tolist()

# company_category カラムのリスト化
company_categories = df_input['company_category'].tolist()

# company_category の埋め込みを作成
company_category_embeddings = model.encode(company_categories)

# 埋め込みを作成
embeddings = model.encode(texts)

# 最後の文章とそれ以外の類似度を計算
target_embedding = embeddings[-1]  # 最後の埋め込みベクトル
similarities = []  # 類似度を保存するリスト

for i in range(len(embeddings) -1):  # 本人を除いてループ
    similarity = cosine_similarity([target_embedding], [embeddings[i]])[0][0]
    category_similarity = cosine_similarity([company_category_embeddings[-1]], [company_category_embeddings[i]])[0][0]
    if category_similarity < 0.95:  # 業種の類似度が 0.95 未満の場合のみ保存
        similarities.append((i, similarity))  # (インデックス, 類似度)のタプルを保存
        print(f"本人と会員番号 {i + 1} の類似度: {similarity:.4f}")

# 類似度の高い企業をソート
user_list = sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
index_sim2 = [index for index, _ in sorted_similarities[:2]]  # 上位2社のindexを選択

# 選択されたインデックスに紐づくデータを出力
selected_data = df.iloc[index_sim2]  # 上位2社のインデックスに対応するデータを取得
print(selected_data)


# データを読み込み
#df = pd.read_csv("https://files.grouplens.org/datasets/movielens/ml-100k/u.data", 
                 #names=["user_id", "item_id", "review", "timestamp"], sep="\t")

# データの整形
#df = pd.pivot_table(df.drop("timestamp", axis=1), index="user_id", columns="item_id", values="review")
#df = df.fillna(0)

#print(df)

# cos類似度をnumpyを使って計算
# dot =  np.dot(df.iloc[0], df.iloc[1])
# norm_a = np.linalg.norm(df.iloc[0])
# norm_b = np.linalg.norm(df.iloc[1])
# dot / (norm_a*norm_b)

## cos類似度をcosine_similarityを使って計算
# cosine_similarity([df.iloc[0], df.iloc[1]])

#cos_list = []
#for user_id in df.index:
    #cos_list.append(cosine_similarity([df.loc[943, 1:]], [df.loc[user_id, 1:]]))

# sorted([ソートの対象], [ソートキー], reverse=True)
#user_list = sorted(range(len(cos_list)), key=lambda i: cos_list[i], reverse=True)

#user_sim10 = user_list[1:][:10]
#print(user_sim10)
