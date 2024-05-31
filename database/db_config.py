import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    DB_CONFIG = {
        'sqlite': os.getenv('SQLITE_DB_NAME', 'supply_chain.db'),
        'postgres': {
            'dbname': os.getenv('POSTGRES_DB', 'supply_chain'),
            'user': os.getenv('POSTGRES_USER', 'your_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'your_password'),
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432')
        },
        'mysql': {
            'dbname': os.getenv('MYSQL_DB', 'supply_chain'),
            'user': os.getenv('MYSQL_USER', 'your_user'),
            'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': os.getenv('MYSQL_PORT', '3306')
        },
        'mongodb': {
            'dbname': os.getenv('MONGODB_DB', 'supply_chain'),
            'user': os.getenv('MONGODB_USER', 'your_user'),
            'password': os.getenv('MONGODB_PASSWORD', 'your_password'),
            'host': os.getenv('MONGODB_HOST', 'localhost'),
            'port': os.getenv('MONGODB_PORT', '27017')
        },
        'oracle': {
            'dbname': os.getenv('ORACLE_DB', 'supply_chain'),
            'user': os.getenv('ORACLE_USER', 'your_user'),
            'password': os.getenv('ORACLE_PASSWORD', 'your_password'),
            'host': os.getenv('ORACLE_HOST', 'localhost'),
            'port': os.getenv('ORACLE_PORT', '1521')
        }
    }
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
