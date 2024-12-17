# # uname() error回避
# import platform
# print(platform.uname())

# from sqlalchemy import create_engine
# import sqlalchemy

# import os
# main_path = os.path.dirname(os.path.abspath(__file__))
# path = os.chdir(main_path)
# print(path)
# engine = create_engine("sqlite:///CRM.db", echo=True)
import os
from sqlalchemy import create_engine
import tempfile
import logging
import atexit

logging.basicConfig(level=logging.INFO)
logger = logging.getlogger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
ca_path = os.path.join(script_dir, "DigiCertGlobalRootG2.crt.pem")
print(ca_path)

# 接続情報
username = "tech0gen8student"  # @以降はサーバ名と一致させる必要がある場合あり
password = "5iTbVNuqQu8z8"
hostname = "tech0-gen-8-step3-rdb-8.mysql.database.azure.com"  # Azure MySQLのホスト名
port = 3306  # 通常MySQLのデフォルトポート
database_name = "cloudninedb"

pem_content = os.getenv("DB_SSL_CA")
if pem_content:
    pem_content = pem_content.replace("\\n", "\n")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, sufix=".pem") as temp_pem:
        temp_pem.write(pem_content)
        temp_pem_path = temp_pem.name
    
    atexit.register(lambda: os.unlink(temp_pem_path))
else:
    logger.error("SSL証明書の環境変数が設定されていません")
    raise ValueError("SSL証明書の環境変数が設定されていません")

# 接続オプション（SSL接続必須の場合などに設定）
# Azure Database for MySQLではSSLをrequireにすることが推奨される場合があります。
# connection_url = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}"
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}",
    connect_args={
        "ssl": {
             "ca": ca_path
        }
    },
    echo=True
)
# エンジン作成
# engine = create_engine(connection_url, echo=True)
print(engine)