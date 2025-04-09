import os
import json
import sqlite3

from ..config import DATA_DIR
from ..api import Mock
from ..logs import ExceptionLogger
from ..schemas import KokomiUser

class UserLocalDB:
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, 'local.db')
        self.__check_db()

    def __check_db(self):
        """检查数据库是否存在，不存在则创建"""
        if not os.path.exists(self.db_path):
            self.__create_db()

    def __create_db(self):
        """创建数据库和表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            table_create_query = '''
            CREATE TABLE users (
                id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                platform    TEXT        NOT NULL,
                user_id     TEXT        NOT NULL,
                query_count INTEGER     DEFAULT 0,
                language    VARCHAR(10) NOT NULL,
                algorithm   VARCHAR(10) NOT NULL,
                background  VARCHAR(10) NOT NULL,
                content     VARCHAR(10) NOT NULL,
                theme       VARCHAR(10) NOT NULL,
                created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at  IMESTAMP,
                UNIQUE(platform, user_id)
            );
            '''
            cursor.execute(table_create_query)
            table_create_query = '''
            CREATE TABLE alias (
                id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                platform    TEXT        NOT NULL,
                user_id     TEXT        NOT NULL,
                alias_list  TEXT        DEFAULT NULL,
                created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at  IMESTAMP,
                UNIQUE(platform, user_id)
            );
            '''
            cursor.execute(table_create_query)
            conn.commit()

    @ExceptionLogger.handle_database_exception_sync
    def get_user_local(self, kokomi_user: KokomiUser):
        """获取用户本地设置或初始化用户数据"""
        # if bot_settings.USE_MOCK:
        #     result = Mock.read_data('local.json')
        #     logging.debug('Using MOCK, skip network requests')
        #     return result

        user_id = kokomi_user.basic.id
        platform_type = kokomi_user.platform.name

        # 检查并创建数据库
        if not os.path.exists(self.db_path):
            self.__create_db()

        # 使用with语句管理数据库连接和游标
        with sqlite3.connect(self.db_path) as conn:
            result = {
                'config': None,
                'alias': None
            }
            cursor = conn.cursor()
            cursor.execute('''
                SELECT alias_list FROM alias 
                WHERE platform = ? AND user_id = ?;
            ''', (platform_type, user_id))
            alias = cursor.fetchone()
            if alias:
                result['alias'] = json.loads(alias)

            cursor.execute('''
                SELECT language, algorithm, background, content, theme
                FROM users 
                WHERE platform = ? AND user_id = ?;
            ''', (platform_type, user_id))
            user = cursor.fetchone()

            if user is None:
                # 插入新的用户数据
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
                ''', (
                    platform_type, user_id, data['language'], data['algorithm'], 
                    data['background'], data['content'], data['theme']
                ))
                result['config'] = data
            else:
                # 更新查询次数
                data = {
                    'language': user[0],
                    'algorithm': None if user[1] == '' else user[1],
                    'background': user[2],
                    'content': user[3],
                    'theme': user[4]
                }
                cursor.execute('''
                    UPDATE users
                    SET query_count = query_count + 1, updated_at = CURRENT_TIMESTAMP
                    WHERE platform = ? AND user_id = ?;
                ''', (platform_type, user_id))
                result['config'] = data
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': result}

    @ExceptionLogger.handle_database_exception_sync
    def update_language(self, user: KokomiUser, language: str):
        """更新用户语言设置"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET language = ?
                WHERE platform = ? AND user_id = ?;
            ''', (language, platform_type, user_id))
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}

    @ExceptionLogger.handle_database_exception_sync
    def update_algorithm(self, user: KokomiUser, algorithm: str):
        """更新用户算法设置"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET algorithm = ?
                WHERE platform = ? AND user_id = ?;
            ''', (algorithm, platform_type, user_id))
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}

    @ExceptionLogger.handle_database_exception_sync
    def update_content(self, user: KokomiUser, content: str):
        """更新用户content主题设置"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        background = {
            'dark': '#313131',
            'light': '#F8F9FB'
        }

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET background = ?, content = ?
                WHERE platform = ? AND user_id = ?;
            ''', (background.get(content), content, platform_type, user_id))
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}
    
    @ExceptionLogger.handle_database_exception_sync
    def update_theme(self, user: KokomiUser, theme: str):
        """更新用户theme主题设置"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        background = {
            'default': ['light', '#F8F9FB'],
            'mavuika': ['dark', '#313131'],
            'furina': ['light', '#F8F9FB'],
            'mygo': ['dark', '#313131'],
            'xnn': ['light', '#F8F9FB']
        }
        content = background.get(theme, None)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if theme != 'defualt':
                cursor.execute('''
                    UPDATE users SET background = ?, content = ?, theme = ?
                    WHERE platform = ? AND user_id = ?;
                ''', (content[1], content[0], theme, platform_type, user_id))
            else:
                cursor.execute('''
                    UPDATE users SET theme = ?
                    WHERE platform = ? AND user_id = ?;
                ''', (theme, platform_type, user_id))
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}

    @ExceptionLogger.handle_database_exception_sync
    def add_alias(self, user: KokomiUser, alias_data: dict):
        """更新用户alias表"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT alias_list FROM alias 
                WHERE platform = ? AND user_id = ?;
            ''', (platform_type, user_id))
            alias = cursor.fetchone()
            if alias:
                alias_list: list = json.loads(alias)
                alias_list.append(alias_data)
            else:
                alias_list = [alias_data]
            cursor.execute('''
                INSERT OR REPLACE INTO alias (platform, user_id, alias_list)
                VALUES (?, ?, ?);
            ''', (platform_type, user_id, json.dumps(alias_list)))
            conn.commit()

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}

    @ExceptionLogger.handle_database_exception_sync
    def del_alias(self, user: KokomiUser, alias_index: int):
        """更新用户alias表"""
        user_id = user.basic.id
        platform_type = user.platform.name

        if not os.path.exists(self.db_path):
            self.__create_db()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT alias_list FROM alias 
                WHERE platform = ? AND user_id = ?;
            ''', (platform_type, user_id))
            alias = cursor.fetchone()
            if alias:
                alias_list: list = json.loads(alias)
                if 0 <= alias_index < len(alias_index):
                    alias_list.pop(alias_index)
                    cursor.execute('''
                        UPDATE alias SET alias_list = ?
                        WHERE platform = ? AND user_id = ?;
                    ''', (json.dumps(alias_list), platform_type, user_id))
                    conn.commit()
                else:
                    pass
            else:
                pass

        return {'status': 'ok', 'code': 1000, 'message': 'Success', 'data': None}
