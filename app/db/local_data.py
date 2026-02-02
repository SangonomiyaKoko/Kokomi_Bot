import sqlite3

from ..core import STORAGE_DIR
from ..loggers import ExceptionLogger
from ..models.schemas import KokomiUser
from ..response import JSONResponse

class LocalDB:
    @staticmethod
    def init_local_db():
        """检查数据库是否存在，不存在则创建"""
        db_path = STORAGE_DIR / 'db/local.db'
        if not db_path.exists():
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                table_create_query = '''
                CREATE TABLE users (
                    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                    platform    TEXT        NOT NULL,
                    user_id     TEXT        NOT NULL,
                    theme       VARCHAR(10) NOT NULL,
                    language    VARCHAR(10) NOT NULL,
                    show_rating INTEGER     NOT NULL,
                    valid_data  INTEGER     NOT NULL,
                    query_count INTEGER     DEFAULT 0,
                    query_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    created_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at  IMESTAMP,
                    UNIQUE(platform, user_id)
                );
                '''
                cursor.execute(table_create_query)
                conn.commit()
        else:
            # TODO: Table结构修改的数据迁移代码
            pass

    @staticmethod
    @ExceptionLogger.handle_program_exception_sync
    def get_user_local(kokomi_user: KokomiUser):
        """获取用户本地设置或初始化用户数据"""
        user_id = kokomi_user.basic.id
        platform_type = kokomi_user.platform.name
        db_path = STORAGE_DIR / 'db/local.db'
        with sqlite3.connect(db_path) as conn:
            data = {}
            cursor = conn.cursor()
            sql = '''
                SELECT 
                    language, 
                    theme, 
                    show_rating, 
                    valid_data
                FROM users 
                WHERE platform = ? 
                  AND user_id = ?;
            '''
            cursor.execute(sql, (platform_type, user_id))
            user = cursor.fetchone()
            if user is None:
                # 插入新的用户数据
                sql = '''
                    INSERT INTO users (
                        platform, 
                        user_id,
                        theme, 
                        language,
                        show_rating,
                        valid_data
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?
                    );
                '''
                cursor.execute(sql, (
                    platform_type, 
                    user_id, 
                    kokomi_user.local.theme,
                    kokomi_user.local.language,
                    kokomi_user.local.show_rating,
                    kokomi_user.local.filter_valid_data
                ))
                data = {
                    'theme': kokomi_user.local.theme,
                    'language': kokomi_user.local.language,
                    'show_rating': kokomi_user.local.show_rating,
                    'filter_valid_data': kokomi_user.local.filter_valid_data
                }
            else:
                # 更新查询次数
                sql = '''
                    UPDATE users
                    SET 
                        query_count = query_count + 1, 
                        query_at = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE platform = ? 
                      AND user_id = ?;
                '''
                cursor.execute(sql, (platform_type, user_id))
                data = {
                    'theme': user[0],
                    'language': user[1],
                    'show_rating': user[2],
                    'filter_valid_data': user[3]
                }
            conn.commit()

        return JSONResponse.get_success_response(data)

    @staticmethod
    @ExceptionLogger.handle_program_exception_sync
    def update_language(user: KokomiUser, language: str):
        """更新用户语言设置"""
        user_id = user.basic.id
        platform_type = user.platform.name
        db_path = STORAGE_DIR / 'db/local.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                UPDATE users 
                SET 
                    language = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE platform = ? 
                  AND user_id = ?;
            '''
            cursor.execute(sql, (language, platform_type, user_id))
            conn.commit()

        return JSONResponse.API_1000_Success
    
    @staticmethod
    @ExceptionLogger.handle_program_exception_sync
    def update_theme(user: KokomiUser, theme: str):
        """更新用户theme主题设置"""
        user_id = user.basic.id
        platform_type = user.platform.name
        db_path = STORAGE_DIR / 'db/local.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                UPDATE users 
                SET 
                    theme = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE platform = ? 
                  AND user_id = ?;
            '''
            cursor.execute(sql, (theme, platform_type, user_id))
            conn.commit()

        return JSONResponse.API_1000_Success

    @staticmethod
    @ExceptionLogger.handle_program_exception_sync
    def update_show_rating(user: KokomiUser, show_rating: bool):
        """更新用户设置"""
        user_id = user.basic.id
        platform_type = user.platform.name
        db_path = STORAGE_DIR / 'db/local.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                UPDATE users 
                SET 
                    show_rating = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE platform = ? 
                  AND user_id = ?;
            '''
            cursor.execute(sql, (show_rating, platform_type, user_id))
            conn.commit()

        return JSONResponse.API_1000_Success

    @staticmethod
    @ExceptionLogger.handle_program_exception_sync
    def update_filter_valid_data(user: KokomiUser, filter_valid_data: bool):
        """更新用户设置"""
        user_id = user.basic.id
        platform_type = user.platform.name
        db_path = STORAGE_DIR / 'db/local.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                UPDATE users 
                SET 
                    valid_data = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE platform = ? 
                  AND user_id = ?;
            '''
            cursor.execute(sql, (filter_valid_data, platform_type, user_id))
            conn.commit()

        return JSONResponse.API_1000_Success
