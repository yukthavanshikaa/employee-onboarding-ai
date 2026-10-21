import streamlit as st
import pandas as pd
from datetime import date
import uuid

st.set_page_config(
    page_title="HR Onboarding Portal",
    page_icon="🏢",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "employees" not in st.session_state:
    st.session_state.employees = []

if "activities" not in st.session_state:
    st.session_state.activities = []

# ---------------- AGENT DEFINITIONS ----------------

AGENTS = {
    "HR Coordinator Agent": "Coordinates the complete onboarding workflow.",
    "Document Verification Agent": "Checks employee document requirements.",
    "Employee Record Agent": "Creates and maintains employee records.",
    "Training Agent": "Recommends department-specific training.",
    "Compliance Agent": "Identifies incomplete onboarding requirements.",
    "IT Access Agent": "Recommends system access for HR approval."
}

REQUIRED_DOCUMENTS = [
    "Government ID",
    "Educational Certificate",
    "Photograph",
    "Signed Offer Letter"
]

TRAINING = {
    "Engineering": [
        "Security Awareness",
        "Engineering Tools",
        "Code of Conduct"
    ],
    "Human Resources": [
        "Data Privacy",
        "HR Systems",
        "Code of Conduct"
    ],
    "Finance": [
        "Finance Systems",
        "Data Privacy",
        "Code of Conduct"
    ],
    "Sales": [
        "CRM Training",
        "Product Training",
        "Code of Conduct"
    ],
    "Operations": [
        "Workplace Safety",
        "Operations Tools",
        "Code of Conduct"
    ]
}

# ---------------- SIMULATED AGENT WORKFLOW ----------------

def run_agents(employee):

    employee["training"] = TRAINING[employee["department"]]
    employee["training_completed"] = []

    employee["documents_status"] = (
        "Complete"
        if all(
            doc in employee["documents"]
            for doc in REQUIRED_DOCUMENTS
        )
        else "Pending"
    )

    employee["compliance"] = (
        "Needs HR Review"
        if employee["documents_status"] == "Pending"
        else "Ready for HR Review"
    )

    employee["it_access"] = {
        "Engineering": [
            "Company Email",
            "Development Environment",
            "Code Repository"
        ],
        "Human Resources": [
            "Company Email",
            "HRIS Portal"
        ],
        "Finance": [
            "Company Email",
            "Finance System"
        ],
        "Sales": [
            "Company Email",
            "CRM"
        ],
        "Operations": [
            "Company Email",
            "Operations Tools"
        ]
    }[employee["department"]]

    risk_points = 0

    if employee["documents_status"] == "Pending":
        risk_points += 2

    if employee["training"]:
        risk_points += 1

    employee["risk"] = (
        "High" if risk_points >= 4
        else "Medium" if risk_points >= 2
        else "Low"
    )

    completed_documents = sum(
        doc in employee["documents"]
        for doc in REQUIRED_DOCUMENTS
    )

    completed_training = len(
        employee["training_completed"]
    )

    total_tasks = (
        len(REQUIRED_DOCUMENTS)
        + len(employee["training"])
    )

    employee["progress"] = int(
        (completed_documents + completed_training)
        / total_tasks * 100
    )

    actions = [
        (
            "Document Verification Agent",
            f"Checked {len(employee['documents'])} of "
            f"{len(REQUIRED_DOCUMENTS)} required documents."
        ),
        (
            "Employee Record Agent",
            f"Created employee record {employee['id']}."
        ),
        (
            "Training Agent",
            f"Recommended {len(employee['training'])} training modules."
        ),
        (
            "Compliance Agent",
            f"Compliance status: {employee['compliance']}."
        ),
        (
            "IT Access Agent",
            "Prepared access recommendations for HR approval."
        ),
        (
            "HR Coordinator Agent",
            "Collected agent results and updated onboarding status."
        )
    ]

    for agent, action in actions:
        st.session_state.activities.insert(
            0,
            {
                "Employee": employee["name"],
                "Agent": agent,
                "Action": action,
                "Status": "Completed"
            }
        )


# ---------------- SIDEBAR ----------------

st.sidebar.title("🏢 Onboarding Portal")
st.sidebar.caption("Human Resources Management")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Register Employee",
        "Employee Directory",
        "Agent Workflow",
        "Compliance Reports"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### System Information")
st.sidebar.caption("Application: Employee Onboarding")
st.sidebar.caption("Mode: Frontend Demo")
st.sidebar.caption("Agents: Simulated")
st.sidebar.caption("Storage: Streamlit Session")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("🏢 AI-Powered Employee Onboarding System")

    st.write(
        "A multi-agent HR workflow for employee registration, "
        "document checks, training recommendations and compliance."
    )

    employees = st.session_state.employees

    total = len(employees)

    completed = sum(
        emp["progress"] == 100
        for emp in employees
    )

    pending = total - completed

    at_risk = sum(
        emp["risk"] in ["Medium", "High"]
        for emp in employees
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Employees", total)
    c2.metric("Completed Onboarding", completed)
    c3.metric("Pending Onboarding", pending)
    c4.metric("Employees at Risk", at_risk)

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("📊 Onboarding Progress")

        if employees:

            for emp in employees:

                st.write(
                    f"**{emp['name']}** · {emp['department']}"
                )

                st.progress(
                    emp["progress"] / 100,
                    text=f"{emp['progress']}% complete"
                )

                st.caption(
                    f"Documents: {emp['documents_status']} | "
                    f"Risk: {emp['risk']}"
                )

        else:

            st.info(
                "No employees registered yet. "
                "Use Register Employee to begin."
            )

    with right:

        st.subheader("🤖 Specialized Agent Network")

        for agent, description in AGENTS.items():

            st.markdown(f"**{agent}**")
            st.caption(description)

    st.divider()

    st.subheader("🕒 Recent Agent Activity")

    if st.session_state.activities:

        st.dataframe(
            pd.DataFrame(
                st.session_state.activities[:10]
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Agent activity will appear here after employee registration."
        )


# ---------------- REGISTER EMPLOYEE ----------------

elif page == "Register Employee":

    st.title("📝 Register New Employee")

    st.write(
        "Enter employee information to initiate the simulated "
        "multi-agent onboarding workflow."
    )

    with st.form("employee_form"):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input("Full Name")
            email = st.text_input("Work Email")

            department = st.selectbox(
                "Department",
                list(TRAINING.keys())
            )

        with col2:

            role = st.text_input("Job Title")
            manager = st.text_input("Reporting Manager")
            joining_date = st.date_input(
                "Joining Date",
                value=date.today()
            )

        documents = st.multiselect(
            "Documents Available",
            REQUIRED_DOCUMENTS
        )

        submit = st.form_submit_button(
            "Register Employee & Run Agents",
            type="primary",
            use_container_width=True
        )

    if submit:

        if not name.strip() or not email.strip() or not role.strip():

            st.error(
                "Please enter the employee name, email and job title."
            )

        elif any(
            emp["email"].lower() == email.strip().lower()
            for emp in st.session_state.employees
        ):

            st.error("This email is already registered.")

        else:

            employee = {
                "id": "EMP-" + uuid.uuid4().hex[:6].upper(),
                "name": name.strip(),
                "email": email.strip(),
                "department": department,
                "role": role.strip(),
                "manager": manager.strip() or "Not Assigned",
                "joining_date": joining_date,
                "documents": documents
            }

            st.session_state.employees.append(employee)

            run_agents(employee)

            st.success(
                f"Employee {employee['name']} registered successfully!"
            )

            st.subheader("🤖 Agent Workflow Results")

            a, b, c = st.columns(3)

            a.metric("Employee ID", employee["id"])
            b.metric("Onboarding Progress", f"{employee['progress']}%")
            c.metric("Risk Level", employee["risk"])

            st.markdown("### Document Verification Agent")
            st.write(employee["documents_status"])

            st.markdown("### Training Agent")
            for module in employee["training"]:
                st.write(f"📚 {module}")

            st.markdown("### Compliance Agent")
            st.write(employee["compliance"])

            st.markdown("### IT Access Agent")
            for access in employee["it_access"]:
                st.write(f"💻 {access}")

            st.caption(
                "IT access recommendations require human approval. "
                "No real accounts or documents are processed."
            )


# ---------------- EMPLOYEE DIRECTORY ----------------

elif page == "Employee Directory":

    st.title("👥 Employee Directory")

    employees = st.session_state.employees

    if not employees:

        st.info("No employees have been registered yet.")

    else:

        search = st.text_input(
            "Search employee by name, email or ID"
        )

        filtered = [
            emp for emp in employees
            if search.lower() in (
                emp["name"] + emp["email"] + emp["id"]
            ).lower()
        ]

        rows = []

        for emp in filtered:

            rows.append({
                "Employee ID": emp["id"],
                "Name": emp["name"],
                "Email": emp["email"],
                "Department": emp["department"],
                "Job Title": emp["role"],
                "Joining Date": str(emp["joining_date"]),
                "Progress": f"{emp['progress']}%",
                "Risk": emp["risk"]
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        csv = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Employee Directory CSV",
            csv,
            "employee_directory.csv",
            "text/csv"
        )


# ---------------- AGENT WORKFLOW ----------------

elif page == "Agent Workflow":

    st.title("🤖 Multi-Agent HR Workflow")

    st.write(
        "Each specialized agent handles one part of employee onboarding. "
        "The HR Coordinator combines the results for HR review."
    )

    for agent, description in AGENTS.items():

        with st.expander(agent, expanded=True):

            st.write(description)

            if agent == "HR Coordinator Agent":

                st.write(
                    "Coordinates the workflow and consolidates the results."
                )

            elif agent == "Document Verification Agent":

                st.write(
                    "Checks whether all required documents have been selected."
                )

            elif agent == "Employee Record Agent":

                st.write(
                    "Creates an employee record in the current session."
                )

            elif agent == "Training Agent":

                st.write(
                    "Creates a department-specific training checklist."
                )

            elif agent == "Compliance Agent":

                st.write(
                    "Flags missing requirements for HR review."
                )

            elif agent == "IT Access Agent":

                st.write(
                    "Recommends role-related system access for human approval."
                )

    st.subheader("Workflow Architecture")

    st.code(
        """
Employee Registration
        |
        v
HR Coordinator Agent
        |
        +--> Document Verification Agent
        |
        +--> Employee Record Agent
        |
        +--> Training Agent
        |
        +--> Compliance Agent
        |
        +--> IT Access Agent
        |
        v
HR Coordinator consolidates results
        |
        v
Final Human HR Review
        """,
        language="text"
    )

    st.subheader("Agent Execution Log")

    if st.session_state.activities:

        st.dataframe(
            pd.DataFrame(st.session_state.activities),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Register an employee to see the agent execution log.")


# ---------------- COMPLIANCE REPORTS ----------------

elif page == "Compliance Reports":

    st.title("🛡️ Compliance Reports")

    employees = st.session_state.employees

    if not employees:

        st.info("No employee records are available.")

    else:

        report = []

        for emp in employees:

            missing_docs = [
                doc for doc in REQUIRED_DOCUMENTS
                if doc not in emp["documents"]
            ]

            pending_training = [
                module for module in emp["training"]
                if module not in emp["training_completed"]
            ]

            report.append({
                "Employee": emp["name"],
                "Employee ID": emp["id"],
                "Missing Documents": ", ".join(missing_docs) or "None",
                "Pending Training": ", ".join(pending_training) or "None",
                "Compliance Status": emp["compliance"],
                "Risk Level": emp["risk"]
            })

        df = pd.DataFrame(report)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Compliance Report",
            df.to_csv(index=False).encode("utf-8"),
            "compliance_report.csv",
            "text/csv"
        )

        st.caption(
            "This is a demo report, not a legal compliance determination."
        )