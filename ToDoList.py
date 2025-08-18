import sqlite3
from datetime import date


class Tasks:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks(
            tid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date DATE,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
        """)
        self.conn.commit()

    def Add_Task(self, name, task_date='', status='Pending'):
        try:
            if not task_date:
                task_date = date.today()
            self.cursor.execute(
                "INSERT INTO Tasks(name, date, status) VALUES (?, ?, ?)",
                (name.strip().lower(), str(task_date), status.title())
            )
            self.conn.commit()
            return True, f"Task '{name}' added successfully ✅"
        except sqlite3.Error as e:
            return False, f"Error adding task: {str(e)}"

    def Delete_Task(self, task_id):
        try:
            self.cursor.execute("DELETE FROM Tasks WHERE tid = ?", (task_id,))
            if self.cursor.rowcount == 0:
                return False, "Task ID not found!"
            self.conn.commit()
            return True, f"Task {task_id} deleted successfully 🗑️"
        except sqlite3.Error as e:
            return False, f"Error deleting task: {str(e)}"

    def View_Tasks(self):
        try:
            self.cursor.execute("SELECT * FROM Tasks ORDER BY tid")
            result_set = self.cursor.fetchall()
            if result_set:
                return True, result_set
            return False, "No tasks found."
        except sqlite3.Error as e:
            return False, f"Error retrieving tasks: {str(e)}"

    def Update_Task(self, task_id, choice, new_value):
        try:
            query = f"UPDATE Tasks SET {choice} = ? WHERE tid = ?"
            self.cursor.execute(
                query, (new_value.title() if choice == "status" else new_value, task_id))
            if self.cursor.rowcount == 0:
                return False, "Task ID not found!"
            self.conn.commit()
            return True, "Task updated successfully ✏️"
        except sqlite3.Error as e:
            return False, f"Error updating task: {str(e)}"

    def Filter_Tasks(self, choice, filter_value):
        try:
            if choice == "status":
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE status = ?", (filter_value.title(),))
            elif choice == "name":
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE name LIKE ?", (f"%{filter_value.lower()}%",))
            elif choice == "date":
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE date = ?", (filter_value,))
            else:
                return False, "Invalid filter choice"

            result_set = self.cursor.fetchall()
            if result_set:
                return True, result_set
            return False, "No matching tasks."
        except sqlite3.Error as e:
            return False, f"Error filtering tasks: {str(e)}"
