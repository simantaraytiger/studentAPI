import streamlit as st
import requests

API_URL = "https://studentapi-2an5.onrender.com/"

st.title("Student Management")

# @st.cache_data(ttl=600)
def fetch_students():
    try:
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            return response.json().get("data", [])
    except:
        return []


students = fetch_students()

# list

st.subheader("All Students")

if students:
    for student in students:
        cols = st.columns([1, 4, 4, 2, 2])
        cols[0].markdown(f"**ID**: {student['id']}")
        cols[1].markdown(f"**Name**: {student['name']}")
        cols[2].markdown(f"**Email**: {student['email']}")

        if cols[3].button("Edit", key=f"edit-{student['id']}"):
            st.session_state.editing_id = student["id"]
            st.session_state.edit_name = student["name"]
            st.session_state.edit_email = student["email"]

        if cols[4].button("Delete", key=f"delete-{student['id']}"):
            del_res = requests.delete(f"{API_URL}/students/{student['id']}")
            if del_res.status_code == 200:
                st.success(f"Deleted student ID {student['id']}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Delete failed")
else:
    st.text("Api Failed to reload! Empty List")


# edit student

st.subheader("Edit Student")
if "editing_id" in st.session_state:
    with st.form("edit_form"):
        name = st.text_input("Name", value=st.session_state.edit_name)
        email = st.text_input("Email", value=st.session_state.edit_email)
        submitted = st.form_submit_button("Update")

        if submitted:
            payload = {"name": name, "email": email}
            res = requests.put(
                f"{API_URL}/students/{st.session_state.editing_id}", json=payload
            )
            if res.status_code == 200:
                st.success("Student updated!")
                st.cache_data.clear()
                del st.session_state.editing_id
                st.rerun()
            else:
                st.error("Update failed")
else:
    st.text("Nothing to Edit")

# add student
st.subheader("Add New Student")
with st.form("add_student"):
    name = st.text_input("Student Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        payload = {"name": name, "email": email}
        res = requests.post(f"{API_URL}/students", json=payload)
        if res.status_code == 200:
            st.success("Student added!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Failed to add student")
