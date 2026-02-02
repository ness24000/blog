from app.DBHandler import DBHandler

class PostsHandler:
    def __init__(self, db_handler: DBHandler) -> None:
        self.dbHandler = db_handler