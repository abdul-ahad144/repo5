import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------
# SAME FILE USED BY DASHBOARD
# ---------------------------------------------------

FILE = "students.csv"


# ---------------------------------------------------
# LOAD STUDENTS
# ---------------------------------------------------

def load_students():

    if not os.path.exists(FILE):

        df = pd.DataFrame(columns=[

            "Student_ID",
            "Name",
            "CGPA",
            "Domain",
            "Job_Role",
            "Company_Tier",
            "Skill_Programs",
            "Projects",
            "Internships",
            "Applied",
            "Shortlisted",
            "Interview_Attended",
            "Offer_Received",
            "Joined",
            "Salary_LPA",
            "Failed_Stage"

        ])

        df.to_csv(FILE, index=False)

    return pd.read_csv(FILE)


# ---------------------------------------------------
# SAVE STUDENTS
# ---------------------------------------------------

def save_students(df):

    df.to_csv(FILE, index=False)


# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

def student_management_page():

    st.title("🎓 Student Management System")

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    df = load_students()

    # ---------------------------------------------------
    # TOP BUTTONS
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅ Back To Dashboard"):

            st.session_state.page = "dashboard"

            st.rerun()

    with col2:

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False

            st.session_state.page = "landing"

            st.rerun()

    st.markdown("---")

    # ===================================================
    # ADD STUDENT
    # ===================================================

    st.subheader("➕ Add Student")

    col1, col2 = st.columns(2)

    # ---------------------------------------------------
    # LEFT SIDE
    # ---------------------------------------------------

    with col1:

        sid = st.text_input("Student ID")

        name = st.text_input("Student Name")

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1
        )

        domain = st.selectbox(

            "Domain",

            [
                "AI",
                "Web Development",
                "Cloud Computing",
                "Cyber Security",
                "Data Science"
            ]
        )

        applied = st.selectbox(
            "Applied",
            [0, 1]
        )

        shortlisted = st.selectbox(
            "Shortlisted",
            [0, 1]
        )

        interview = st.selectbox(
            "Interview Attended",
            [0, 1]
        )

    # ---------------------------------------------------
    # RIGHT SIDE
    # ---------------------------------------------------

    with col2:

        role = st.selectbox(

            "Job Role",

            [
                "ML Engineer",
                "Software Developer",
                "Cloud Engineer",
                "Tester",
                "Data Analyst"
            ]
        )

        company = st.selectbox(

            "Company Tier",

            [
                "Tier 1",
                "Tier 2",
                "Tier 3"
            ]
        )

        skills = st.slider(
            "Skill Programs",
            0,
            10,
            2
        )

        projects = st.slider(
            "Projects",
            0,
            10,
            2
        )

        internships = st.slider(
            "Internships",
            0,
            5,
            1
        )

        offer = st.selectbox(
            "Offer Received",
            [0, 1]
        )

        joined = st.selectbox(
            "Joined",
            [0, 1]
        )

        salary = st.number_input(
            "Salary LPA",
            min_value=0,
            max_value=100,
            value=5
        )

        failed_stage = st.selectbox(

            "Failed Stage",

            [
                "None",
                "Aptitude",
                "Shortlisting",
                "Interview",
                "Technical Round",
                "Coding Round",
                "HR Round"
            ]
        )

    # ---------------------------------------------------
    # ADD BUTTON
    # ---------------------------------------------------

    if st.button("✅ ADD STUDENT"):

        sid = str(sid).strip()

        if sid == "" or name == "":

            st.error("Please fill all required fields")

        elif sid in df["Student_ID"].astype(str).values:

            st.error("Student ID already exists")

        else:

            new_student = pd.DataFrame([{

                "Student_ID": sid,
                "Name": name,
                "CGPA": cgpa,
                "Domain": domain,
                "Job_Role": role,
                "Company_Tier": company,
                "Skill_Programs": skills,
                "Projects": projects,
                "Internships": internships,
                "Applied": applied,
                "Shortlisted": shortlisted,
                "Interview_Attended": interview,
                "Offer_Received": offer,
                "Joined": joined,
                "Salary_LPA": salary,
                "Failed_Stage": failed_stage

            }])

            # ADD NEW STUDENT

            df = pd.concat(
                [df, new_student],
                ignore_index=True
            )

            # SAVE TO SAME CSV

            save_students(df)

            st.success(
                "Student Added Successfully ✅"
            )

            st.rerun()

    st.markdown("---")

    # ===================================================
    # REMOVE STUDENT
    # ===================================================

    st.subheader("❌ Remove Student")

    remove_id = st.text_input(
        "Enter Student ID To Remove"
    )

    if st.button("🗑 REMOVE STUDENT"):

        remove_id = str(remove_id).strip()

        if remove_id in df["Student_ID"].astype(str).values:

            # REMOVE STUDENT

            df = df[
                df["Student_ID"].astype(str) != remove_id
            ]

            # SAVE UPDATED CSV

            save_students(df)

            st.success(
                "Student Removed Successfully ✅"
            )

            st.rerun()

        else:

            st.error("Student ID Not Found")

    st.markdown("---")

    # ===================================================
    # SEARCH STUDENT
    # ===================================================

    st.subheader("🔍 Search Student")

    search_id = st.text_input(
        "Enter Student ID"
    )

    if search_id:

        result = df[
            df["Student_ID"].astype(str) == search_id
        ]

        if result.empty:

            st.warning("No Student Found")

        else:

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")

    # ===================================================
    # ALL STUDENTS
    # ===================================================

    st.subheader("📋 All Students")

    st.dataframe(

        df,

        use_container_width=True,
        hide_index=True

    )

    st.markdown("---")

    # ===================================================
    # DOWNLOAD CSV
    # ===================================================

    st.subheader("📥 Download Student Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        "⬇ Download CSV",

        csv,

        "students.csv",

        "text/csv"

    )
