import sqlite3


class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_answers(self):
        sql = """
            CREATE TABLE TEST_ANSWERS (
                book_number int NOT NULL,
                answers varchar(255) NOT NULL ,
                PRIMARY KEY (id)
                );
            """
        self.execute(sql, commit=True)



    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_answer(self, book_number: int, answers: str):
        sql = """
        INSERT INTO TEST_ANSWERS(book_number, answers) VALUES (?, ?)  
        """
        self.execute(sql, parameters=(book_number, answers), commit=True)

    def select_all_answers(self):
        sql = """
        SELECT * FROM TEST_ANSWERS            
        """
        return self.execute(sql, fetchall=True)

    def select_answer(self, **kwargs):
        sql = """SELECT * FROM TEST_ANSWERS WHERE """
        sql, parameters = self.format_args(kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

def logger(statement):
    print(f"""
    Executing:
    {statement}
    """)
