import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

DB_NAME = "tasks.db"


# ---------------- DATABASE ----------------
class DB:
    """
    Handles SQLite database operations for tasks.
    Creates the tasks table if it doesn't exist.
    """
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()


# ---------------- SCREENS ----------------
class Intro1(Screen): pass  # Splash screen
class Intro2(Screen): pass  # Onboarding 1
class Intro3(Screen): pass  # Onboarding 2
class Intro4(Screen): pass  # Onboarding 3
class Todo(Screen): pass    # Main to-do screen


# ---------------- APP ----------------
class UpTodoApp(App):
    """
    Main application class for UpTodo.
    Manages screen navigation, database, and task operations.
    """

    def build(self):
        """
        Builds the app UI with ScreenManager and loads KV files.
        Schedules task loading after UI initialization.
        """
        self.db = DB()
        Builder.load_file("intro.kv")
        Builder.load_file("todo.kv")
        sm = ScreenManager()
        sm.add_widget(Intro1(name="intro1"))
        sm.add_widget(Intro2(name="intro2"))
        sm.add_widget(Intro3(name="intro3"))
        sm.add_widget(Intro4(name="intro4"))
        sm.add_widget(Todo(name="todo"))
        self.sm = sm
        Clock.schedule_once(lambda dt: self.load_tasks())
        return sm

    # ---------- TASK LOGIC ----------
    def add_task(self, text):
        """
        Adds a new task to the database if text is not empty.
        Clears the input field and reloads tasks.
        """
        if not text.strip():
            return
        self.db.cur.execute(
            "INSERT INTO tasks(title, completed) VALUES (?,0)",
            (text,)
        )
        self.db.conn.commit()
        self.sm.get_screen("todo").ids.task_input.text = ""
        self.load_tasks()

    def load_tasks(self):
        """
        Loads all tasks from database, ordered by creation time descending.
        Clears and repopulates the task list UI.
        """
        todo = self.sm.get_screen("todo")
        todo.ids.task_list.clear_widgets()
        self.db.cur.execute("SELECT id, title, completed FROM tasks ORDER BY created_at DESC")
        for tid, title, completed in self.db.cur.fetchall():
            todo.ids.task_list.add_widget(
                Builder.load_string(f'''
BoxLayout:
    size_hint_y: None
    height: "60dp"
    padding: "10dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: (0.15,0.15,0.18,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [16]

    CheckBox:
        active: {bool(completed)}
        on_active: app.toggle_task({tid}, self.active)

    Label:
        text: "[s]{title}[/s]" if {bool(completed)} else "{title}"
        markup: True
        color: (.6,.6,.6,1) if {bool(completed)} else (1,1,1,1)

    Button:
        text: "✕"
        size_hint_x: None
        width: "40dp"
        background_color: (1,0.3,0.3,1)
        on_press: app.delete_task({tid})
''')
            )

    def toggle_task(self, tid, value):
        """
        Toggles the completion status of a task.
        Updates database and reloads tasks.
        """
        self.db.cur.execute(
            "UPDATE tasks SET completed=? WHERE id=?",
            (1 if value else 0, tid)
        )
        self.db.conn.commit()
        self.load_tasks()

    def delete_task(self, tid):
        """
        Deletes a task from the database permanently.
        Reloads tasks after deletion.
        """
        self.db.cur.execute("DELETE FROM tasks WHERE id=?", (tid,))
        self.db.conn.commit()
        self.load_tasks()


if __name__ == "__main__":
    UpTodoApp().run()
