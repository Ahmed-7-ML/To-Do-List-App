# ✅ To-Do List App  

## 📌 Overview  
The **To-Do List App** is a web-based application built with **Streamlit** and **SQLite** to help users manage their tasks efficiently.  

It provides a simple, intuitive interface with **tab-based navigation** to:  
👉 **Add, View, Update, Delete, and Filter tasks**.  

Developed by **👨‍💻 Eng. Ahmed Akram Amer**, the app ensures persistent storage of tasks in a local SQLite database.  

---

## 🚀 Features  
- ✍️ **Add Tasks**: Create tasks with a name, optional due date (defaults to today), and status (`Pending`, `In Progress`, `Finished`).  
- 🗑️ **Delete Tasks**: Remove tasks by their unique ID.  
- 👀 **View Tasks**: Display all tasks in a table with a **CSV download** option.  
- 🛠️ **Update Tasks**: Modify a task’s **name, date, or status**.  
- 🔍 **Filter Tasks**: Search tasks by **name (partial match), date, or status**.  
- 📱 **Responsive UI**: Tab-based layout for seamless navigation.  
- ⚠️ **Error Handling**: Validates inputs with clear success/error messages.  
- 🗄️ **Database**: Persistent task storage using SQLite (`ToDo.db`).  

---

## 📸 Screenshots  
<img src = 'backgorind-photo.png'/>
---

## 🛠️ Prerequisites  
- 🐍 Python **3.7+**  
- Required Python packages (listed in `requirements.txt`):  
  - `streamlit`  
  - `pandas`  
  - `colorama` *(optional, for console-based colored output)*  
  - `sqlite3` *(comes with Python standard library)*  

---

## ⚙️ Installation  

1. **Clone the repository**  
   ```bash
   git clone <repository-url>
   cd to-do-list-app
   ```

2. **Create & activate a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the following files exist**  
   ```
   app.py          # Streamlit frontend
   ToDoList.py     # Backend logic for database operations
   requirements.txt
   ```

---

## ▶️ Usage  

Run the app:  
```bash
streamlit run app.py
```

Navigate through the tabs:  
- ➕ **Add Tasks** → Enter task name, optional date & status.  
- ❌ **Delete Tasks** → Enter task ID to remove it.  
- 📋 **View Tasks** → See all tasks in a table, refresh, or download as CSV.  
- ✏️ **Update Tasks** → Enter task ID and update name, date, or status.  
- 🔎 **Filter Tasks** → Search tasks by name, date, or status.  

---

## 🗄️ Database  

- The app automatically creates a local SQLite database file `ToDo.db`.  
- Make sure the project directory has **write permissions** for database operations.  

---

## ☁️ Deployment on Streamlit Cloud  

1. Push your project to GitHub:  
   ```bash
   git init
   git add app.py ToDoList.py requirements.txt
   git commit -m "Initial commit"
   git remote add origin <repository-url>
   git push -u origin main
   ```

2. Deploy on **Streamlit Cloud**:  
   - Log in to Streamlit Cloud.  
   - Create a new app, link your GitHub repo, and set `app.py` as the main file.  
   - Streamlit Cloud will auto-install dependencies from `requirements.txt`.  

🔧 **Troubleshooting**: Check logs via *Manage App* in Streamlit Cloud if errors occur.  

---

## 📂 File Structure  
```
to-do-list-app/
├── app.py            # Streamlit frontend with tab-based UI
├── ToDoList.py       # Backend logic for SQLite operations
├── requirements.txt  # Dependencies
├── ToDo.db           # SQLite database (auto-created)
└── README.md         # Documentation
```

---

## 🔖 Notes  
- ⚡ Requires **streamlit >= 1.0.0** (for `st.rerun()`).  
- 🎨 `colorama`: Optional, only affects console debugging.  
- 🔄 Dynamic UI: Update tab dynamically changes labels (e.g., “Enter new Name/Date/Status”).  

---

## 👨‍💻 Developer  
**Eng. Ahmed Akram Amer**  

---

## 📜 License  
This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.  

---

## 🙏 Acknowledgments  
- 🌐 **Streamlit** → Web framework for Python.  
- 🗄️ **SQLite** → Lightweight database storage.  
- 🎨 **Colorama** → Optional console styling.  
