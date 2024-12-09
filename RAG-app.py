import requests
from typing import Dict

# Dify APIの認証キー
API_KEY = 'app-ZC4DH7fHMtGwK3q3L1y4MmaT'  # 取得したAPIキーに置き換えてください
# Dify APIのベースURL
BASE_URL = 'https://api.dify.ai/v1/chat-messages'

def get_dify_response(query: str, user: str) -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数

    :param query: ユーザーの質問
    :param user: ユーザー識別子
    :return: APIからの応答テキスト
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data: Dict[str, any] = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": user,
    }
    
    response = requests.post(BASE_URL, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()['answer']

if __name__ == "__main__":
    MAX_CHATS = 3  # 最大チャット回数
    chat_count = 0  # チャット回数の初期値
    user = "abc-123"
    
    while chat_count < MAX_CHATS:
        query = input("質問を入力してください（終了するには 'exit' と入力）: ")
        if query.lower() == 'exit':
            print("チャットを終了します。")
            break

        try:
            answer = get_dify_response(query, user)
            print(f"回答: {answer}")
            chat_count += 1
        except requests.RequestException as e:
            print(f"エラーが発生しました: {e}")
    
    if chat_count >= MAX_CHATS:
        print("1回のセッションでのご質問は3回までです。有償プランにアップグレードしていただくと、より多くのやり取りができるようになります。")
