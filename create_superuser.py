from api.db.db_models import init_database_tables
from api.db.init_data import init_superuser
from api import settings

if __name__ == '__main__':
    # 初始化设置
    settings.init_settings()
    # 初始化数据库表
    init_database_tables()
    # 创建超级用户
    init_superuser()
