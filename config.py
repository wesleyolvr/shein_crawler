import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return dict(config['database'])


database_config = get_config()

DATABASE_URL = database_config['database_url']
