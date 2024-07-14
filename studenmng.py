import streamlit as st
from pymongo import MongoClient
client = MongoClient("mongodb+srv://khushi_25:Abcs1234@cluster0.hkvlg4z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['khushidb']
students_collection =db['students']
courses_collection =db['course']
st.title("Student Course Management")
menu=["Add Student","View Student","Update Student","Delete Student"]
choice=st.sidebar.selectbox("Menu",menu)
def submit_form():
    student = {
        "usn": st.session_state.USN,
        "name": st.session_state.NAME,
        "branch": st.session_state.BRANCH,
        "enrollment":[]
    }
    students_collection.insert_one(student)
    st.success("Student Added Successfully")
    st.session_state.USN=""
    st.session_state.NAME=""
    st.session_state.BRANCH=""
if choice=="Add Student":
    st.header("Add Student")
    with st.form(key="Add Student"):
     usn=st.text_input("Enter Student USN",key="USN")
     name=st.text_input("Enter Student Name",key="NAME")
     branch=st.text_input("Enter Student Branch",key="BRANCH")
     submit=st.form_submit_button(label="Add Student",on_click=submit_form)
elif choice=="View Student":
    st.subheader("View Student")
    student=list(students_collection.find())
    for student in student:
        st.write(f"USN: {student['usn']}, NAME: {student['name']}, BRANCH: {student['branch']}")
elif choice == "Update Student":
    st.subheader("Update Student")
    students = list(students_collection.find())
    student_options = {student['name']: student['_id'] for student in students}
    selected_student = st.selectbox("Select Student", options=list(student_options.keys()))
    new_name = st.text_input("New Name")
    new_branch = st.text_input("New Branch")
    new_usn= st.text_input("New Usn")
    if st.button("Update Student"):
        student_id = student_options[selected_student]
        update_fields = {}
        if new_name:
            update_fields['name'] = new_name
        if new_branch:
            update_fields['branch'] = new_branch
        if new_usn:
            update_fields['usn'] = new_usn
        if update_fields:
            students_collection.update_one({"_id": student_id}, {"$set": update_fields})
            st.success(f"Updated student {selected_student}")
            
elif choice == "Delete Student":
    st.subheader("Delete Student")
    students = list(students_collection.find())
    student_options = {student['name']: student['_id'] for student in students}
    selected_student = st.selectbox("Select Student", options=list(student_options.keys()))
    if st.button("Delete Student"):
        student_id = student_options[selected_student]
        students_collection.delete_one({"_id": student_id})
        st.success(f"Deleted student {selected_student}")

elif choice == "Enroll Student":
    st.subheader("Enroll Student in Course")
    students = list(students_collection.find())
    courses = list(courses_collection.find())
    student_options = {student['name']: student['_id'] for student in students}
    course_options = {course['course_name']: course['_id'] for course in courses}
    selected_student = st.selectbox("Select Student", options=list(student_options.keys()))
    selected_course = st.selectbox("Select Course", options=list(course_options.keys()))
    if st.button("Enroll"):
        student_id = student_options[selected_student]
        course_id = course_options[selected_course]
        # Fetch the student's current enrollments
        student = students_collection.find_one({"_id": student_id})
        enrolments = student.get("enrolments", [])

        # Check if the student is already enrolled in the selected course
        if course_id in enrolments:
            st.warning(f"{selected_student} is already enrolled in {selected_course}")
        else:
            students_collection.update_one({"_id": student_id}, {"$addToSet": {"enrolments": course_id}})
            st.success(f"Enrolled {selected_student} in {selected_course}")

elif choice == "View Enrollments":
    st.subheader("Enrolled Students")
    courses = list(courses_collection.find())
    course_options = {course['course_name']: course['_id'] for course in courses}
    selected_course = st.selectbox("Select Course", options=list(course_options.keys()))
    if st.button("View"):
        course_id = course_options[selected_course]
        students = list(students_collection.find({"enrolments": course_id}))
        st.write(f"Course: {selected_course}")
        if students:
            for student in students:
                st.write(f" - {student['name']} ({student['usn']})")
        else:
            st.error("No Students Found")

