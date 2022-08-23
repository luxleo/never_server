db = {
    'user': 'root',
    'password':'password!',
    'host':'localhost',
    'port':3306,
    'database':'never'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

test_db = {
    'user': 'root',
    'password':'password',
    'host':'localhost',
    'port':3306,
    'database':'never_test'
}

test_config = {
    "DB_URL": f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8"
}