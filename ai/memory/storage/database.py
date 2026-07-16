import sqlite3


class MemoryDatabase:

    def __init__(self):
        self.conn = sqlite3.connect(
            "memory.db"
        )

        self.create_table()


    def create_table(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            action TEXT,
            input TEXT,
            response TEXT
        )
        """)

        self.conn.commit()


    def save(
        self,
        task_id,
        action,
        input_text,
        response
    ):

        self.conn.execute(
            """
            INSERT OR REPLACE INTO memories
            VALUES (?, ?, ?, ?)
            """,
            (
                task_id,
                action,
                input_text,
                str(response)
            )
        )

        self.conn.commit()


    def get(self, task_id):

        cursor = self.conn.execute(
            """
            SELECT * FROM memories
            WHERE id=?
            """,
            (task_id,)
        )

        return cursor.fetchone()
