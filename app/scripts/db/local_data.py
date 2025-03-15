import os
import sqlite3

from ..config import DATA_DIR, bot_settings
from ..api import Mock
from ..logs import ExceptionLogger, logging
from ..schemas import KokomiUser

class UserLocalDB:
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, 'local.db')
        self.__check_db()

    def __check_db(self):
        if os.path.exists(self.db_path) is False:
            self.__create_db()

    def __create_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        table_create_query = f'''
        CREATE TABLE users (
            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            -- 用户基本信息
            platform    TEXT        NOT NULL,
            user_id     TEXT        NOT NULL,
            query_count INTEGER     DEFAULT 0,
            -- 用户数据
            language    VARCHAR(10) NOT NULL,
            algorithm   VARCHAR(10) NOT NULL,    -- 注意，如果设置为不使用算法，则内容为空字符串！
            background  VARCHAR(10) NOT NULL,
            content     VARCHAR(10) NOT NULL,
            theme       VARCHAR(10) NOT NULL,
            -- 相关时间
            created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at  IMESTAMP,

            UNIQUE(platform, user_id) -- 联合唯一索引
        );
        '''
        cursor.execute(table_create_query)
        conn.commit()
        cursor.close()
        conn.close()

    @ExceptionLogger.handle_database_exception_sync
    def get_user_local(self, kokomi_user: KokomiUser):
        if bot_settings.USE_MOCK:
            result = Mock.read_data('local.json')
            logging.debug('Using MOCK, skip network requests')
            return result
        user_id = kokomi_user.basic.id
        platform_type = kokomi_user.platform.name
        if os.path.exists(self.db_path) is False:
            self.__create_db()
        conn = sqlite3.connect(database=self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT language, algorithm, background, content, theme
            FROM users 
            WHERE platform = '{platform_type}' AND user_id = '{user_id}';
        ''')
        user = cursor.fetchone()
        if user is None:
            data = {
                'language': kokomi_user.local.language,
                'algorithm': kokomi_user.local.algorithm,
                'background': kokomi_user.local.background,
                'content': kokomi_user.local.content,
                'theme': kokomi_user.local.theme
            }
            cursor.execute('''
                INSERT INTO users (platform, user_id, language, algorithm, background, content, theme)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            [
                platform_type, user_id, data['language'], data['algorithm'], 
                data['background'], data['content'], data['theme']
            ]
            )
        else:
            data = {
                'language': user[0],
                'algorithm': None if user[1] == '' else user[1],
                'background': user[2],
                'content': user[3],
                'theme': user[4]
            }
            cursor.execute(f'''
                UPDATE users
                SET query_count = query_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE platform = '{platform_type}' AND user_id = '{user_id}';
            ''')
        conn.commit()
        cursor.close()
        conn.close()
        return {'status': 'ok','code': 1000,'message': 'Success','data': data}

    @ExceptionLogger.handle_database_exception_sync
    def update_language(self, user: KokomiUser, language: str):
        user_id = user.basic.id
        platform_type = user.platform.name
        if os.path.exists(self.db_path) is False:
            self.__create_db()
        conn = sqlite3.connect(database=self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE users SET language = '{language}'
            WHERE platform = '{platform_type}' AND user_id = '{user_id}';
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        return {'status': 'ok','code': 1000,'message': 'Success','data': None}

    @ExceptionLogger.handle_database_exception_sync
    def update_algorithm(self, user: KokomiUser, algorithm: str):
        user_id = user.basic.id
        platform_type = user.platform.name
        if os.path.exists(self.db_path) is False:
            self.__create_db()
        conn = sqlite3.connect(database=self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE users SET algorithm = '{algorithm}'
            WHERE platform = '{platform_type}' AND user_id = '{user_id}';
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        return {'status': 'ok','code': 1000,'message': 'Success','data': None}
