

DATA_STORE_SRC = './data-store/'

class DataLocator:


    def get_db_connection(time:str):
        return DATA_STORE_SRC + 'event.sqlite'

