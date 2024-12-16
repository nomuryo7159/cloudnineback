# uname() error回避
import platform
print("platform", platform.uname())
 

from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
import numpy as np
from db_control.connect import engine
from db_control.mymodels import Customers
from db_control import crud, mymodels
from sqlalchemy import text


from sklearn.metrics.pairwise import cosine_similarity
# import mysql.connector
from sentence_transformers import SentenceTransformer
 

def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
 
    # セッションを閉じる
    session.close()
    return "inserted"
 
def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json

def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    customer_id = values.pop("customer_id")
 
    query = query = update(mymodel).where(mymodel.customer_id == customer_id).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"

def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id==customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
 
    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"

def myselect2():
    # セッション構築
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(
                text("SELECT * FROM master ORDER BY customer_id DESC")
            ).fetchall()
            print(result)
            arr_master_list = []
            for val in result:
                ml = {
                        "user_name": val[1],
                        "company_name": val[2],
                        "email": val[3],
                        "password": val[4],
                        "company_url": val[5],
                        "company_size": val[6],
                        "company_category": val[7],
                        "entity_title": val[8],
                        "entry_image": val[9],
                        "entry_description": val[10],
                        "entry_achievement": val[11],
                        "strength": val[12],
                        "tags": val[13]
                }
                arr_master_list.append(ml)
            result_json = arr_master_list
            result = session.execute(
                text("DESC master")
            ).fetchall()
            print(result)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、取得に失敗しました")
        result_json = json.dumps([])
    # セッションを閉じる
    session.close()
    return result_json

def myinsert2(value):
    # セッション構築
    Session = sessionmaker(bind=engine)
    session = Session()
    # SQL作成
    query = f"""
INSERT INTO master(
    user_name,
    company_name,
    email,
    password,
    company_url,
    company_size,
    company_category,
    entity_title,
    entry_image,
    entry_description,
    entry_achievement,
    strength,
    tags
)
VALUE(
    '{value['user_name']}',
    '{value['company_name']}',
    '{value['email']}',
    '{value['password']}',
    '{value['company_url']}',
    '{value['company_size']}',
    '{value['company_category']}',
    '{value['entity_title']}',
    '{value['entry_image']}',
    '{value['entry_description']}',
    '{value['entry_achievement']}',
    '{value['strength']}',
    '{value['tags']}'
)"""
    print(query)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(
                text(query)
            )
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "inserted"


def recommendselect(value):
    # セッション構築
    Session = sessionmaker(bind=engine)
    session = Session()
    result_json = ""
    try:
        # トランザクションを開始
        with session.begin():
            ## レコメンドエンジン
            results = session.execute(
                text("SELECT * FROM master")
            ).fetchall()
            arr_master_list = []
            for val in results:
                ml = {
                        "user_name": val[1],
                        "company_name": val[2],
                        "email": val[3],
                        "password": val[4],
                        "company_url": val[5],
                        "company_size": val[6],
                        "company_category": val[7],
                        "entity_title": val[8],
                        "entry_image": val[9],
                        "entry_description": val[10],
                        "entry_achievement": val[11],
                        "strength": val[12],
                        "tags": val[13]
                }
                arr_master_list.append(ml)
            # データを読み込み
            # json_results = json.loads(arr_master_list)
            json_results = arr_master_list
            df = pd.json_normalize(json_results)
            print(df)
            # データの整形
            df_input = df.drop(columns=["user_name", "company_name", "email", "password", "company_url"])
            # df_review = df_input.fillna(0)
            print(df_input[['entity_title', 'entry_description', 'entry_achievement', 'strength', 'tags']])
            # モデルをロード
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # 複数のカラムを一文につなげてリスト化
            texts = df_input[['entity_title', 'entry_description', 'entry_achievement', 'strength', 'tags']].apply(
                lambda row: ' '.join(row.values.astype(str)), axis=1
            ).tolist()

            # company_category カラムのリスト化
            company_categories = df_input['company_category'].tolist()

            # company_category の埋め込みを作成
            company_category_embeddings = model.encode(company_categories)

            # 埋め込みを作成
            embeddings = model.encode(texts)
            print(embeddings)

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
            result_json = selected_data.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、取得に失敗しました")
        result_json = json.dumps([])
    # セッションを閉じる
    session.close()
    return result_json