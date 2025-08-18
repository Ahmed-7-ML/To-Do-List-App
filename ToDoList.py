from datetime import datetime, date
import sqlite3

# Try to import colorama, but provide a fallback if it's not installed
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Fallback for color_status if colorama is not available


def color_status(status):
    if COLORAMA_AVAILABLE:
        if status.lower() == "in progress":
            return Fore.YELLOW + status + Style.RESET_ALL
        elif status.lower() == "finished":
            return Fore.GREEN + status + Style.RESET_ALL
        elif status.lower() == "pending":
            return Fore.CYAN + status + Style.RESET_ALL
        else:
            return Fore.WHITE + status + Style.RESET_ALL
    else:
        return status  # Return plain status if colorama is not available


class Tasks:
    def __init__(self):
        # Initialize database connection
        self.conn = sqlite3.connect("ToDo.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create Tasks table if it doesn't exist
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks(
            tid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date DATE,
            status TEXT NOT NULL DEFAULT 'In Progress'
        )
        """)
        self.conn.commit()
        print("Successful Access to the Tasks Table in ToDo DB")

    def Add_Task(self, name, task_date='', status='In Progress'):
        try:
            if not task_date:
                task_date = date.today()
            self.cursor.execute(
                """INSERT INTO Tasks(name, date, status) VALUES (?, ?, ?)""",
                (name.lower(), task_date, status.title())
            )
            self.conn.commit()
            return True, f"Task '{name}' is successfully added"
        except sqlite3.Error as e:
            return False, f"Error adding task: {str(e)}"

    def Delete_Task(self, id):
        try:
            # Check if the Task ID exists
            self.cursor.execute("SELECT * FROM Tasks WHERE tid = ?", (id,))
            if self.cursor.fetchone():
                self.cursor.execute(
                    """DELETE FROM Tasks WHERE tid = ?""", (id,))
                self.conn.commit()
                return True, f"Task {id} is successfully deleted"
            else:
                return False, "Task ID not found!"
        except sqlite3.Error as e:
            return False, f"Error deleting task: {str(e)}"

    def View_Tasks(self):
        try:
            self.cursor.execute("SELECT * FROM Tasks ORDER BY tid")
            result_set = self.cursor.fetchall()
            if result_set:
                return True, result_set
            else:
                return False, "No tasks found"
        except sqlite3.Error as e:
            return False, f"Error retrieving tasks: {str(e)}"

    def Update_Task(self, id, choice, new_value):
        try:
            if choice == 'name':
                self.cursor.execute(
                    """UPDATE Tasks SET name = ? WHERE tid = ?""",
                    (new_value.lower(), id)
                )
            elif choice == 'date':
                self.cursor.execute(
                    """UPDATE Tasks SET date = ? WHERE tid = ?""",
                    (new_value, id)
                )
            elif choice == 'status':
                self.cursor.execute(
                    """UPDATE Tasks SET status = ? WHERE tid = ?""",
                    (new_value.title(), id)
                )
            else:
                return False, "Invalid update choice"

            if self.cursor.rowcount == 0:
                return False, "Task ID not found!"
            self.conn.commit()
            return True, "Task successfully updated"
        except sqlite3.Error as e:
            return False, f"Error updating task: {str(e)}"

    def Filter_Tasks(self, choice, filter_value):
        try:
            if choice == 'status':
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE status = ?", (filter_value.title(),))
            elif choice == 'name':
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE name LIKE ?", (f"%{filter_value.lower()}%",))
            elif choice == 'date':
                self.cursor.execute(
                    "SELECT * FROM Tasks WHERE date = ?", (filter_value,))
            else:
                return False, "Invalid filter choice"

            result_set = self.cursor.fetchall()
            if result_set:
                return True, result_set
            else:
                return False, "No tasks match the filter"
        except sqlite3.Error as e:
            return False, f"Error filtering tasks: {str(e)}"

    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()
