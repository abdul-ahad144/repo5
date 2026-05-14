import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from utils.metrics import (
    interview_success_rate,
    round_efficiency
)


def dashboard():

    st.title("🚀 PragyanAI Placement Intelligence Engine")

    # ---------------------------------------------------
    # LOAD SAME CSV USED BY STUDENT MANAGEMENT
    # ---------------------------------------------------

    @st.cache_data
    def load_data():

        if not os.path.exists("students.csv"):

            df = pd.DataFrame()

        else:

            df = pd.read_csv("students.csv")

        return df

    df = load_data()

    # ---------------------------------------------------
    # EMPTY DATA CHECK
    # ---------------------------------------------------

    if df.empty:

        st.warning("No student data available")

        return

    # ---------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------

    st.sidebar.title("⚙ Dashboard Panel")

    st.sidebar.header("🔍 Filters")

    domain = st.sidebar.multiselect(
        "Domain",
        df["Domain"].unique()
    )

    company = st.sidebar.multiselect(
        "Company Tier",
        df["Company_Tier"].unique()
    )

    role = st.sidebar.multiselect(
        "Job Role",
        df["Job_Role"].unique()
    )

    # ---------------------------------------------------
    # APPLY FILTERS
    # ---------------------------------------------------

    if st.sidebar.button("Apply Filters"):

        if domain:
            df = df[df["Domain"].isin(domain)]

        if company:
            df = df[df["Company_Tier"].isin(company)]

        if role:
            df = df[df["Job_Role"].isin(role)]

    # ---------------------------------------------------
    # RESET FILTERS
    # ---------------------------------------------------

    if st.sidebar.button("Reset Filters"):

        st.rerun()

    # ---------------------------------------------------
    # ADMIN PANEL
    # ---------------------------------------------------

    if st.session_state.get("user") == "admin":

        st.sidebar.markdown("---")

        st.sidebar.subheader("🛠 Admin Controls")

        if st.sidebar.button("🎓 Student Management"):

            st.session_state.page = "students"

            st.rerun()

    # ---------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.session_state.page = "landing"

        st.rerun()

    # ---------------------------------------------------
    # KPI SECTION
    # ---------------------------------------------------

    st.subheader("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Students",
        len(df)
    )

    col2.metric(
        "Success Rate",
        f"{interview_success_rate(df):.2%}"
    )

    col3.metric(
        "Efficiency",
        f"{round_efficiency(df):.2%}"
    )

    col4.metric(
        "Placed",
        int(df["Joined"].sum())
    )

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([

        "📉 Funnel",
        "🔥 Failures",
        "💼 Roles & Salary",
        "🧠 Skills"

    ])

    # ---------------------------------------------------
    # TAB 1
    # ---------------------------------------------------

    with tab1:

        st.subheader("📉 Placement Funnel")

        funnel_data = {

            "Applied": int(df["Applied"].sum()),
            "Shortlisted": int(df["Shortlisted"].sum()),
            "Interview": int(df["Interview_Attended"].sum()),
            "Offer": int(df["Offer_Received"].sum()),
            "Joined": int(df["Joined"].sum())

        }

        st.bar_chart(funnel_data)

    # ---------------------------------------------------
    # TAB 2
    # ---------------------------------------------------

    with tab2:

        st.subheader("🔥 Failure Stage Distribution")

        failure_data = df["Failed_Stage"].value_counts()

        st.bar_chart(failure_data)

    # ---------------------------------------------------
    # TAB 3
    # ---------------------------------------------------

    with tab3:

        st.subheader("📊 Job Roles vs Placement")

        role_data = df.groupby(
            "Job_Role"
        )["Joined"].sum()

        st.bar_chart(role_data)

        st.markdown("---")

        st.subheader("💰 Salary Distribution")

        fig, ax = plt.subplots()

        ax.hist(
            df["Salary_LPA"],
            bins=10
        )

        ax.set_title("Salary Distribution")

        ax.set_xlabel("Salary (LPA)")

        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    # ---------------------------------------------------
    # TAB 4
    # ---------------------------------------------------

    with tab4:

        st.subheader("🧠 Skills Impact")

        skill_data = df.groupby(
            "Skill_Programs"
        )["Joined"].mean()

        st.bar_chart(skill_data)

    # ---------------------------------------------------
    # SEARCH STUDENT
    # ---------------------------------------------------

    st.subheader("🔍 Student Search")

    sid = st.text_input("Enter Student ID")

    if sid:

        result = df[
            df["Student_ID"].astype(str) == sid
        ]

        st.dataframe(
            result,
            hide_index=True,
            use_container_width=True
        )

    # ---------------------------------------------------
    # TOP STUDENTS
    # ---------------------------------------------------

    st.subheader("🏆 Top Students")

    top = df.sort_values(
        by="CGPA",
        ascending=False
    ).head(10)

    st.dataframe(
        top,
        hide_index=True,
        use_container_width=True
    )

    # ---------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------

    st.subheader("📥 Download Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "students.csv"
    )

    st.markdown("---")

    st.write("🚀 Built with Streamlit")
