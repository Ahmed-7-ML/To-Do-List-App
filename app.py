import streamlit as st
import pandas as pd
from datetime import date
from ToDoList import Tasks

# Initialize Tasks object
task = Tasks()
st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("background-photo.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* إضافة طبقة شبه شفافة لتحسين القراءة */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.3); /* طبقة سوداء شبه شفافة */
        z-index: -1;
    }
    /* ضبط لون النصوص والعناصر لتكون واضحة */
    h1, h2, h3, p, label, .stTextInput>label, .stSelectbox>label, .stButton>button {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    /* ضبط لون خلفية مربعات الإدخال لتكون مرئية */
    .stTextInput>div>input, .stSelectbox>div>select {
        background-color: rgba(255, 255, 255, 0.9);
        color: black;
    }
    /* ضبط أزرار الحذف لتكون مرئية */
    .delete-button {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.title("📝 To Do List")

# Header with Welcome Message and Developer Credit
st.markdown("""
### Welcome to my App, Feel Free to use this
**Developed by Eng/Ahmed Akram Amer**
""")

# Initialize session state for dynamic update choice
if 'update_choice' not in st.session_state:
    st.session_state.update_choice = "Name"

# Create Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Add Tasks", "Delete Tasks", "View Tasks", "Update Tasks", "Filter Tasks"])

# ---- Add Tasks Tab ----
with tab1:
    st.subheader("➕ Add a New Task")
    with st.form("add_task_form", clear_on_submit=True):
        name = st.text_input("Task Name")
        task_date = st.date_input("Task Date (Optional)", value=None)
        status = st.selectbox("Status", ["Pending", "In Progress", "Finished"])
        submitted = st.form_submit_button("Add Task")
        if submitted:
            if not name:
                st.error("Task name cannot be empty!")
            else:
                success, message = task.Add_Task(
                    name, str(task_date) if task_date else '', status)
                if success:
                    st.success(message)
                else:
                    st.error(message)

# ---- Delete Tasks Tab ----
with tab2:
    st.subheader("🗑️ Delete Task")
    del_id = st.number_input("Enter Task ID to Delete",
                             min_value=1, step=1, key="delete_id")
    if st.button("Delete Task"):
        success, message = task.Delete_Task(del_id)
        if success:
            st.success(message)
        else:
            st.error(message)

# ---- View Tasks Tab ----
with tab3:
    st.subheader("📋 View All Tasks")
    if st.button("Refresh Tasks"):
        st.rerun()  # Using st.rerun() as per previous fix
    success, result = task.View_Tasks()
    if success:
        df = pd.DataFrame(result, columns=["ID", "Name", "Date", "Status"])
        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download All Tasks as CSV",
            data=csv,
            file_name="all_tasks.csv",
            mime="text/csv"
        )
    else:
        st.info(result)

# ---- Update Tasks Tab ----
with tab4:
    st.subheader("✏️ Update Task")
    with st.form("update_task_form"):
        uid = st.number_input("Enter Task ID", min_value=1, step=1)
        choice = st.selectbox("What do you want to update?", [
                              "Name", "Date", "Status"], key="update_choice_select")

        # Update session state when choice changes
        if choice != st.session_state.update_choice:
            st.session_state.update_choice = choice
            st.rerun()  # Rerun to update the input label dynamically

        # Set placeholder based on choice
        placeholder = "e.g., Buy groceries" if choice == "Name" else "YYYY-MM-DD" if choice == "Date" else "Pending, In Progress, or Finished"
        new_value = st.text_input(
            f"Enter new {choice}", placeholder=placeholder)
        update_submit = st.form_submit_button("Update")
        if update_submit:
            if not new_value:
                st.error(f"New {choice} cannot be empty!")
            else:
                success, message = task.Update_Task(
                    uid, choice.lower(), new_value)
                if success:
                    st.success(message)
                else:
                    st.error(message)

# ---- Filter Tasks Tab ----
with tab5:
    st.subheader("🔍 Filter Tasks")
    with st.form("filter_task_form"):
        filter_choice = st.selectbox("Filter By", ["Name", "Date", "Status"])
        filter_value = st.text_input(f"Enter {filter_choice} value")
        filter_submit = st.form_submit_button("Apply Filter")
        if filter_submit:
            if not filter_value:
                st.error(f"{filter_choice} value cannot be empty!")
            else:
                success, result = task.Filter_Tasks(
                    filter_choice.lower(), filter_value)
                if success:
                    df = pd.DataFrame(
                        result, columns=["ID", "Name", "Date", "Status"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info(result)
