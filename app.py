# part 1 - imports and page configuration
 
# import required libraries
import streamlit as st
 
import requests
 
import pandas as pd
 
import base64
 
import os

import joblib

# set the title and icon of the browser tab
st.set_page_config(page_title = "Insurance Complaint Management System", page_icon = "🛡️", layout = "wide")
 
# the address where the fastapi backend (main.py) is running
# make sure you start the backend first with: uvicorn main:app --reload
API_BASE_URL = "http://127.0.0.1:8001"

# Load trained ML model and CountVectorizer
mnb_model = joblib.load("mnb.pkl")
count_vectorizer = joblib.load("cv.pkl")

# ML prediction function
def predict_complaint_category(complaint_text):

    complaint_vector = count_vectorizer.transform(
        [complaint_text]
    )

    prediction = mnb_model.predict(
        complaint_vector
    )[0]

    category_mapping = {
        0: "Policy Cancellation",
        1: "Billing Dispute",
        2: "Coverage Denial",
        3: "Customer Service Issue",
        4: "Fraud Suspicion",
        5: "Claim Delay"
    }

    return category_mapping[int(prediction)]

 
# the categories this system supports, same ones used across the project
CATEGORIES = [
    "Policy Cancellation",
    "Billing Dispute",
    "Coverage Denial",
    "Customer Service Issue",
    "Fraud Suspicion",
    "Claim Delay"
]
 
# part 1b - custom css for a professional look
 
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    section[data-testid="stSidebar"] {
        background-color: #0f2b46;
    }
    section[data-testid="stSidebar"] * {
        color: #f5f7fa !important;
    }
    .hero-banner {
        background: linear-gradient(135deg, #0f2b46 0%, #1c4e80 100%);
        padding: 2.5rem 2rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero-banner h1 { color: white; margin-bottom: 0.3rem; }
    .hero-banner p { color: #d7e3f0; font-size: 1.05rem; margin: 0; }
    .metric-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #e6e9ee;
    }
    .metric-card .metric-value { font-size: 1.8rem; font-weight: 700; color: #0f2b46; }
    .metric-card .metric-label { font-size: 0.85rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.04em; }
    .category-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.85rem;
        color: white;
        background-color: #1c4e80;
    }
    .project-title {
        color: white !important;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.9);
    }

    .project-subtitle {
        color: white !important;
        font-size: 16px;
        text-align: center;
        margin-bottom: 25px;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    }
    .login-card {
        background-color: rgba(255,255,255,0.95);
        padding: 2.5rem;
        border-radius: 16px;
        max-width: 420px;
        margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .app-footer {
        text-align: center;
        color: #9aa5b1;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e6e9ee;
    }
</style>
""", unsafe_allow_html = True)
 
# part 1c - background image helper (used on the login/register screen)
def set_background(image_file):

    if not os.path.isfile(image_file):
        st.error(f"Background image not found: {image_file}")
        return

    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(15, 43, 70, 0.55),
                    rgba(15, 43, 70, 0.55)
                ),
                url("data:image/jpeg;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Login page text */
        .login-card,
        .login-card label,
        .login-card p,
        .login-card span,
        .login-card div {{
            color: white !important;
        }}

        .login-card h1,
        .login-card h2,
        .login-card h3 {{
            color: white !important;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8);
        }}

        /* Login and Register tabs */
        .stTabs [data-baseweb="tab"] {{
            color: white !important;
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            color: #ffffff !important;
        }}

        /* Input labels */
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label {{
            color: white !important;
            font-weight: 600;
        }}

        /* Caption text */
        .stCaption,
        [data-testid="stCaptionContainer"] {{
            color: white !important;
        }}

        /* Login/Register input boxes */
        .stTextInput input {{
            color: #111827 !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    ) 
 
# part 1d - small reusable helper to draw a metric card
 
def metric_card(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html = True)
 
# part 1e - session state setup
# this is how streamlit "remembers" whether the user is logged in, across reruns
 
if "token" not in st.session_state:
    st.session_state.token = None
 
if "username" not in st.session_state:
    st.session_state.username = None
 
# part 1f - helper to build the authorization header for protected api calls
 
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}
 
# part 1g - helper to safely call the api and show a friendly error if something goes wrong
 
def call_api(method, endpoint, **kwargs):
 
    try:
        response = requests.request(method, f"{API_BASE_URL}{endpoint}", timeout = 10, **kwargs)
        return response
 
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure it's running with: uvicorn main:app --reload")
        return None
 
# ============================================================
# part 2 - login / register screen (shown when not logged in)
# ============================================================
 
# ============================================================
# part 2 - login / register screen (shown when not logged in)
# ============================================================

if st.session_state.token is None:

    # show the background image only on this screen
    image_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "images"
    )

    # Find the background image automatically
    image_path = None

    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_folder, filename)
            break

    # Apply background image
    if image_path:
        set_background(image_path)
    else:
        st.error(f"No background image found in: {image_folder}")

    # Login card
    st.markdown(
        '<div class="login-card">',
        unsafe_allow_html=True
    )

    # Project title
    st.markdown(
        """
        <div class="project-title">
            🛡️ Insurance Complaint Management System
        </div>

        <div class="project-subtitle">
            Sign in to manage complaints, or create a new account.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Login and Register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])

    # --------------------------------------------------------
    # LOGIN TAB
    # --------------------------------------------------------

    with tab1:

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            if (
                login_username.strip() == ""
                or login_password.strip() == ""
            ):
                st.warning(
                    "Please enter both username and password."
                )

            else:

                response = call_api(
                    "POST",
                    "/login",
                    json={
                        "username": login_username,
                        "password": login_password
                    }
                )

                if response is not None:

                    if response.status_code == 200:

                        st.session_state.token = (
                            response.json()["access_token"]
                        )

                        st.session_state.username = login_username

                        st.rerun()

                    else:

                        st.error(
                            response.json().get(
                                "detail",
                                "Login failed"
                            )
                        )

    # --------------------------------------------------------
    # REGISTER TAB
    # --------------------------------------------------------

    with tab2:

        reg_id = st.number_input(
            "User ID",
            min_value=1,
            step=1,
            key="reg_id"
        )

        reg_username = st.text_input(
            "Choose a username",
            key="reg_username"
        )

        reg_password = st.text_input(
            "Choose a password",
            type="password",
            key="reg_password"
        )

        reg_role = st.selectbox(
            "Role",
            ["customer", "agent", "admin"],
            key="reg_role"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if (
                reg_username.strip() == ""
                or reg_password.strip() == ""
            ):
                st.warning(
                    "Please fill in all fields."
                )

            else:

                response = call_api(
                    "POST",
                    "/register",
                    json={
                        "id": int(reg_id),
                        "username": reg_username,
                        "password": reg_password,
                        "role": reg_role
                    }
                )

                if response is not None:

                    if response.status_code == 200:

                        st.success(
                            "Account created! "
                            "Switch to the Login tab to sign in."
                        )

                    else:

                        st.error(
                            response.json().get(
                                "detail",
                                "Registration failed"
                            )
                        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
 
# ============================================================
# part 3 - main dashboard (shown after login)
# ============================================================
 
else:
 
    # display a small brand header + logged in user above the navigation
    st.sidebar.markdown("### 🛡️ Insurance AI")
    st.sidebar.caption(f"Logged in as **{st.session_state.username}**")
    st.sidebar.divider()
 
    page = st.sidebar.radio("Navigation", [
        "Dashboard",
        "Create Complaint",
        "View Complaints",
        "Update Complaint",
        "Delete Complaint",
        "Search",
        "Filter by Category",
        "Upload File",
    ])
 
    st.sidebar.divider()
 
    if st.sidebar.button("Logout", use_container_width = True):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()
 
    # ---- dashboard page ----
    if page == "Dashboard":
 
        st.markdown(f"""
        <div class="hero-banner">
            <h1>🛡️ Insurance Complaint Dashboard</h1>
            <p>Welcome back, {st.session_state.username}. Manage, search, and track customer complaints below.</p>
        </div>
        """, unsafe_allow_html = True)
 
        # pull a batch of complaints just to build quick summary metrics
        response = call_api("GET", "/view_complaints", params = {"skip": 0, "limit": 100}, headers = auth_headers())
 
        if response is not None and response.status_code == 200:
 
            complaints = response.json()
            df = pd.DataFrame(complaints)
 
            col1, col2, col3 = st.columns(3)
 
            with col1:
                metric_card("Total Complaints", len(df))
 
            with col2:
                unique_products = df["insurance_product"].nunique() if not df.empty and "insurance_product" in df else 0
                metric_card("Insurance Products", unique_products)
 
            with col3:
                metric_card("Categories Tracked", len(CATEGORIES))
 
            st.write("")
            st.subheader("Recent complaints")
 
            if df.empty:
                st.info("No complaints yet. Create one from the sidebar.")
            else:
                st.dataframe(df, use_container_width = True, hide_index = True)
 
        elif response is not None:
            st.error(response.json().get("detail", "Could not load dashboard data"))
 
    # ---- create complaint page ----
    elif page == "Create Complaint":

        st.title("📝 Create Complaint")
        st.caption("Enter your complaint and let the ML model predict its category.")

        insurance_product = st.selectbox(
            "Insurance Product",
            [
            "life insurance",
            "health insurance",
            "home insurance",
            "auto insurance",
            "travel insurance"
            ]
        )

        complaint_text = st.text_area(
            "Complaint Text",
            height=150,
            placeholder="Describe your insurance complaint..."
        )

    # Predict complaint category
        if st.button("🤖 Predict Complaint Category"):

            if complaint_text.strip() == "":
                st.warning("Please enter the complaint text.")

            else:

                predicted_category = predict_complaint_category(
                    complaint_text
                )

                st.session_state.predicted_category = predicted_category

                st.success(
                    f"🤖 Predicted Category: {predicted_category}"
                )

    # Get predicted category
        predicted_category = st.session_state.get(
            "predicted_category",
            None
        )

    # Submit complaint after prediction
        if predicted_category:

            st.info(
                f"Complaint Category: **{predicted_category}**"
            )

            if st.button("Submit Complaint", type="primary"):

                response = call_api(
                    "POST",
                    "/create_complaint",
                    json={
                        "insurance_product": insurance_product,
                        "complaint_text": complaint_text,
                        "complaint_category": predicted_category
                    },
                    headers=auth_headers()
                )

                if response is not None:

                    if response.status_code == 200:

                        st.success(
                            response.json()["message"]
                    )

                        st.json(
                            response.json()["data"]
                    )

                    else:

                        st.error(
                            response.json().get(
                                "detail",
                                "Could not create complaint"
                            )
                        )
    # ---- view complaints page ----
    elif page == "View Complaints":
 
        st.title("📋 View Complaints")
 
        col1, col2 = st.columns(2)
 
        with col1:
            skip = st.number_input("Skip (start from record)", min_value = 0, value = 0, step = 1)
 
        with col2:
            limit = st.number_input("Limit (how many to show)", min_value = 1, value = 5, step = 1)
 
        if st.button("Load Complaints", type = "primary"):
 
            response = call_api("GET", "/view_complaints", params = {"skip": int(skip), "limit": int(limit)}, headers = auth_headers())
 
            if response is not None:
 
                if response.status_code == 200:
 
                    complaints = response.json()
 
                    if len(complaints) == 0:
                        st.info("No complaints found for this range.")
                    else:
                        st.dataframe(pd.DataFrame(complaints), use_container_width = True, hide_index = True)
 
                else:
                    st.error(response.json().get("detail", "Could not load complaints"))
 
    # ---- update complaint page ----
    elif page == "Update Complaint":
 
        st.title("✏️ Update Complaint")
 
        complaint_id = st.number_input("Complaint ID to update", min_value = 1, step = 1)
        insurance_product = st.selectbox("Insurance Product", ["life insurance", "health insurance", "home insurance", "auto insurance", "travel insurance"], key = "update_product")
        complaint_text = st.text_area("Updated complaint text", height = 150, key = "update_text")
        complaint_category = st.selectbox("Complaint Category", CATEGORIES, key = "update_category")
 
        if st.button("Update Complaint", type = "primary"):
 
            response = call_api("PUT", f"/update_complaint/{int(complaint_id)}", json = {
                "insurance_product": insurance_product,
                "complaint_text": complaint_text,
                "complaint_category": complaint_category
            }, headers = auth_headers())
 
            if response is not None:
 
                if response.status_code == 200:
                    st.success(response.json()["message"])
 
                else:
                    st.error(response.json().get("detail", "Could not update complaint"))
 
    # ---- delete complaint page ----
    elif page == "Delete Complaint":
 
        st.title("🗑️ Delete Complaint")
 
        complaint_id = st.number_input("Complaint ID to delete", min_value = 1, step = 1)
 
        st.warning("This action cannot be undone.")
 
        if st.button("Delete Complaint", type = "primary"):
 
            response = call_api("DELETE", f"/delete_complaint/{int(complaint_id)}", headers = auth_headers())
 
            if response is not None:
 
                if response.status_code == 200:
                    st.success(response.json()["message"])
 
                else:
                    st.error(response.json().get("detail", "Could not delete complaint"))
 
    # ---- search page ----
    elif page == "Search":
 
        st.title("🔎 Search by Insurance Product")
 
        search_term = st.text_input("Insurance product contains...", placeholder = "e.g. life, health, auto")
 
        if st.button("Search", type = "primary"):
 
            if search_term.strip() == "":
                st.warning("please enter a search term.")
 
            else:
                response = call_api("GET", "/search_complaint", params = {"insurance_product": search_term}, headers = auth_headers())
 
                if response is not None:
 
                    if response.status_code == 200:
 
                        results = response.json()
 
                        if len(results) == 0:
                            st.info("No matching complaints found.")
                        else:
                            st.dataframe(pd.DataFrame(results), use_container_width = True, hide_index = True)
 
                    else:
                        st.error(response.json().get("detail", "Search failed"))
 
    # ---- filter page ----
    elif page == "Filter by Category":
 
        st.title("🗂️ Filter by Category")
 
        selected_category = st.selectbox("Complaint Category", CATEGORIES)
 
        if st.button("Filter", type = "primary"):
 
            response = call_api("GET", "/filter_complaint", params = {"complaint_category": selected_category}, headers = auth_headers())
 
            if response is not None:
 
                if response.status_code == 200:
 
                    results = response.json()
 
                    if len(results) == 0:
                        st.info("No complaints found in this category.")
                    else:
                        st.dataframe(pd.DataFrame(results), use_container_width = True, hide_index = True)
 
                else:
                    st.error(response.json().get("detail", "Filter failed"))
 
    # ---- upload file page ----
    elif page == "Upload File":
 
        st.title("📎 Upload Supporting File")
        st.caption("e.g. a photo of damage, a scanned document, or an invoice.")
 
        uploaded_file = st.file_uploader("Choose a file")
 
        if uploaded_file is not None:
 
            if st.button("Upload", type = "primary"):
 
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
 
                response = call_api("POST", "/upload", files = files, headers = auth_headers())
 
                if response is not None:
 
                    if response.status_code == 200:
                        st.success(f"Uploaded successfully: {response.json()['filename']}")
 
                    else:
                        st.error(response.json().get("detail", "Upload failed"))
 
    # ---- footer ----
    st.markdown("""
    <div class="app-footer">
        Insurance Complaint Dashboard &middot; Streamlit frontend &middot; FastAPI backend
    </div>
    """, unsafe_allow_html = True)