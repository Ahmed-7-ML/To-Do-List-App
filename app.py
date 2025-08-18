import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
from ToDoList import Tasks

# --------------------
# DB Connection (Safe with Session State)
# --------------------
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect("ToDo.db", check_same_thread=False)

task = Tasks(st.session_state.conn)

# --------------------
# Streamlit UI
# --------------------

# st.write("Current directory:", os.getcwd())
st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

st.title("📝 To Do List")
st.markdown("### Welcome to my App!\n**Developed by Eng/Ahmed Akram Amer**")

st.image("background-photo.png", use_container_width=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Add Tasks", "Delete Tasks", "View Tasks", "Update Tasks", "Filter Tasks"]
)

# ---- Add Task ----
with tab1:
    st.subheader("➕ Add a New Task")
    with st.form("add_task_form", clear_on_submit=True):
        name = st.text_input("Task Name")
        task_date = st.date_input("Task Date", value=date.today())
        status = st.selectbox("Status", ["Pending", "In Progress", "Finished"])
        submitted = st.form_submit_button("Add Task")
        if submitted:
            if not name.strip():
                st.error("Task name cannot be empty!")
            else:
                success, msg = task.Add_Task(name, str(task_date), status)
                st.success(msg) if success else st.error(msg)

# ---- Delete Task ----
with tab2:
    st.subheader("🗑️ Delete Task")
    del_id = st.number_input("Enter Task ID", min_value=1, step=1)
    if st.button("Delete Task"):
        success, msg = task.Delete_Task(del_id)
        st.success(msg) if success else st.error(msg)

# ---- View Tasks ----
with tab3:
    st.subheader("📋 View All Tasks")
    success, result = task.View_Tasks()
    if success:
        df = pd.DataFrame(result, columns=["ID", "Name", "Date", "Status"])
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "tasks.csv", "text/csv")
    else:
        st.info(result)

# ---- Update Task ----
with tab4:
    st.subheader("✏️ Update Task")
    with st.form("update_task_form"):
        uid = st.number_input("Enter Task ID", min_value=1, step=1)
        choice = st.selectbox("Field to Update", ["name", "date", "status"])
        new_value = st.text_input(f"Enter new {choice}")
        update_submit = st.form_submit_button("Update")
        if update_submit:
            if not new_value.strip():
                st.error("Value cannot be empty!")
            else:
                success, msg = task.Update_Task(uid, choice, new_value)
                st.success(msg) if success else st.error(msg)

# ---- Filter Task ----
with tab5:
    st.subheader("🔍 Filter Tasks")
    with st.form("filter_task_form"):
        filter_choice = st.selectbox("Filter By", ["name", "date", "status"])
        filter_value = st.text_input(f"Enter {filter_choice}")
        filter_submit = st.form_submit_button("Apply Filter")
        if filter_submit:
            success, result = task.Filter_Tasks(filter_choice, filter_value)
            if success:
                df = pd.DataFrame(
                    result, columns=["ID", "Name", "Date", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info(result)
