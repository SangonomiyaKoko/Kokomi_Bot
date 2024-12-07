import os
import sqlite3

from scripts.config import DATA_DIR
from scripts.logs import ExceptionLogger

class UserLocal:
    def __create_db():
        db_path = os.path.join(DATA_DIR, 'user_pic.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        table_create_query = f'''
        CREATE TABLE users (
            id          INTEGER    PRIMARY KEY AUTOINCREMENT,
            platform    TEXT       NOT NULL,
            user_id     TEXT       NOT NULL,
            picture     INTEGER    NOT NULL,
            query_count INTEGER    DEFAULT 0,
            created_at  TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at T IMESTAMP,
            UNIQUE(platform, user_id) -- 联合唯一索引
        );
        '''
        cursor.execute(table_create_query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    @ExceptionLogger.handle_database_exception_sync
    def get_user_local(cls, platform: str, user: str):
        db_path = os.path.join(DATA_DIR, 'local.db')
        if os.path.exists(db_path) is False:
            cls.__create_db()
        conn = sqlite3.connect(database=db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT picture 
            FROM users 
            WHERE platform = '{platform}' AND user_id = '{user}';
        ''')
        data = cursor.fetchone()
        if data is None:
            picture = 1
        else:
            picture = data[0]
            cursor.execute(f'''
                UPDATE users
                SET query_count = query_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE platform = '{platform}' AND user_id = '{user}';
            ''')
        cursor.close()
        conn.close()
        return {'status': 'ok','code': 1000,'message': 'Success','data': {'picture': picture}}

    @classmethod
    @ExceptionLogger.handle_database_exception_sync
    def put_user_local(cls, platform: str, user: str, picture: int):
        db_path = os.path.join(DATA_DIR, 'local.db')
        if os.path.exists(db_path) is False:
            cls.__create_db()
        conn = sqlite3.connect(database=db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT picture 
            FROM users 
            WHERE platform = '{platform}' AND user_id = '{user}';
        ''')
        data = cursor.fetchone()
        if data is None:
            cursor.execute(f'''
                INSERT INTO pic ( platform, user_id, picture )
                VALUES ({platform},{user},{picture});
            ''')
            conn.commit()
        else:
            cursor.execute(f'''
                UPDATE users
                SET picture = {picture}, updated_at = CURRENT_TIMESTAMP
                WHERE platform = '{platform}' AND user_id = '{user}';
            ''')
            conn.commit()
        cursor.close()
        conn.close()
        return {'status': 'ok','code': 1000,'message': 'Success','data': None}