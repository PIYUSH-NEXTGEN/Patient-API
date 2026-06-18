from typing import Dict, Any, Optional

import pandas as pd
import requests
import streamlit as st

# Base URL of the FastAPI backend
BASE_URL = "http://127.0.0.1:8000"


def set_styles() -> None:
    """Inject custom CSS for modern, rounded cards and spacing."""
    st.markdown(
        """
        <style>
        /* Rounded card */
        .card {
            background: white;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 18px;
            color: #1a202c;
        }
        .card h3, .card h4 {
            color: #1a202c;
            margin-top: 0;
        }
        .card p {
            color: #4a5568;
        }
        .muted { color: #6b7280; }
        .feature { 
            font-size: 14px; 
            color: #1a202c;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


###############
# API Helpers
###############


def check_api() -> bool:
    """Return True if backend is reachable."""
    try:
        resp = requests.get(f"{BASE_URL}/docs")
        return resp.status_code < 500
    except requests.RequestException:
        return False


def get_patient(patient_id: str) -> Dict[str, Any]:
    try:
        resp = requests.get(f"{BASE_URL}/patients/{patient_id}")
        return {"ok": resp.ok, "status_code": resp.status_code, "data": resp.json()}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def create_patient(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        resp = requests.post(f"{BASE_URL}/create", json=payload)
        return {"ok": resp.ok, "status_code": resp.status_code, "data": resp.json()}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def update_patient(patient_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        resp = requests.put(f"{BASE_URL}/edit/{patient_id}", json=payload)
        return {"ok": resp.ok, "status_code": resp.status_code, "data": resp.json()}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def delete_patient(patient_id: str) -> Dict[str, Any]:
    try:
        resp = requests.delete(f"{BASE_URL}/delete/{patient_id}")
        return {"ok": resp.ok, "status_code": resp.status_code, "data": resp.json()}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def sort_patients(sort_by: str, order: str) -> Dict[str, Any]:
    try:
        resp = requests.get(f"{BASE_URL}/sort", params={"sort_by": sort_by, "order": order})
        return {"ok": resp.ok, "status_code": resp.status_code, "data": resp.json()}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


###############
# Utilities
###############


def calculate_bmi(weight: float, height: float) -> Optional[float]:
    try:
        if not height or height <= 0:
            return None
        bmi = weight / (height * height)
        return round(bmi, 2)
    except Exception:
        return None


def bmi_verdict(bmi: Optional[float]) -> str:
    if bmi is None:
        return "Unknown"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


###############
# Pages
###############


def page_home() -> None:
    st.title("🏥 Patient Management System")
    st.markdown("Manage patient records using a FastAPI backend with a clean Streamlit dashboard.")

    # Status indicator and features
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("✨ Features")
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        with feat_col1:
            st.write("✅ Create Patients")
            st.write("✅ View Patients")
        with feat_col2:
            st.write("✅ Update Patients")
            st.write("✅ Delete Patients")
        with feat_col3:
            st.write("✅ BMI Calculation")
            st.write("✅ Patient Sorting")
    
    with col2:
        api_ok = check_api()
        if api_ok:
            st.success("✅ Backend reachable")
        else:
            st.error("❌ Backend not reachable\nStart FastAPI at\nhttp://127.0.0.1:8000")

    st.markdown("---")
    st.markdown("#### 💡 Quick Tips")
    st.markdown("Use the sidebar to navigate between pages. All actions communicate directly with the FastAPI server.")


def page_create() -> None:
    st.header("Create Patient")
    st.info("📝 Fill in all required fields to create a new patient. Patient ID format: e.g., P001")
    st.markdown("Create a new patient record in the backend.")

    with st.form("create_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_id = st.text_input("Patient ID", max_chars=20, placeholder="e.g., P001")
            name = st.text_input("Name", placeholder="e.g., John Doe")
            city = st.text_input("City", placeholder="e.g., New York")
        with col2:
            age = st.number_input("Age", min_value=0, max_value=150, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col3:
            height = st.number_input("Height (m)", min_value=0.0, format="%.2f", value=1.75)
            weight = st.number_input("Weight (kg)", min_value=0.0, format="%.1f", value=70.0)

        submitted = st.form_submit_button("✅ Create Patient")

    if submitted:
        # Basic validation
        if not patient_id.strip():
            st.error("Patient ID is required.")
            return
        if not name.strip():
            st.error("Name is required.")
            return

        payload = {
            "id": patient_id.strip(),
            "name": name.strip(),
            "city": city.strip(),
            "age": int(age),
            "gender": gender,
            "height": float(height),
            "weight": float(weight),
        }

        with st.spinner("Creating patient..."):
            resp = create_patient(payload)

        if resp.get("ok"):
            st.success("Patient created successfully ✅")
            st.json(resp.get("data"))
        else:
            err = resp.get("data") or resp.get("error") or {}
            st.error(f"Failed to create patient: {err}")


def render_patient_card(data: Dict[str, Any]) -> None:
    """Build a visual patient card using native Streamlit components."""
    name = data.get("name", "—")
    age = data.get("age", "—")
    gender = data.get("gender", "—")
    height = data.get("height", None)
    weight = data.get("weight", None)
    city = data.get("city", "—")
    bmi = None
    if height and weight:
        bmi = calculate_bmi(float(weight), float(height))

    # Use columns and metrics for cleaner display
    st.subheader(f"👤 {name}")
    st.write(f"**Location:** {city}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Age", age)
    col2.metric("Gender", gender)
    col3.metric("Height (m)", height if height else "—")
    col4.metric("BMI", bmi if bmi is not None else "—")

    with st.expander("📋 Full Details"):
        verdict = bmi_verdict(bmi)
        detail_cols = st.columns(2)
        with detail_cols[0]:
            st.write(f"**Weight (kg):** {weight}")
            st.write(f"**BMI Verdict:** {verdict}")
        with detail_cols[1]:
            st.write(f"**Patient ID:** {data.get('id', '—')}")


def page_view() -> None:
    st.header("View Patient")
    st.info("📝 Enter a Patient ID (e.g., P001) to view patient details.")
    patient_id = st.text_input("Patient ID to search", placeholder="e.g., P001")
    if st.button("🔍 Search"):
        if not patient_id.strip():
            st.error("Please provide Patient ID")
            return
        with st.spinner("Fetching patient..."):
            resp = get_patient(patient_id.strip())

        if resp.get("ok"):
            data = resp.get("data")
            # Show metrics and data
            st.success("Patient found ✅")
            render_patient_card(data)
            st.markdown("---")
            st.subheader("Raw JSON")
            st.json(data)
            st.subheader("Table View")
            df = pd.DataFrame([data])
            st.dataframe(df)
        else:
            err = resp.get("data") or resp.get("error") or {}
            st.error(f"Failed to fetch patient: {err}")


def page_update() -> None:
    st.header("Update Patient")
    st.info("📝 Enter Patient ID (e.g., P001) and update only the fields you want to change.")
    st.markdown("Provide Patient ID and fields to update (only non-empty fields will be sent).")

    with st.form("update_form"):
        pid = st.text_input("Patient ID", placeholder="e.g., P001")
        name = st.text_input("Name (leave blank to keep)", placeholder="e.g., Jane Doe")
        city = st.text_input("City (leave blank to keep)", placeholder="e.g., Los Angeles")
        age = st.text_input("Age (leave blank to keep)", placeholder="e.g., 30")
        gender = st.selectbox("Gender (leave as-is by choosing 'Select')", ["Select", "Male", "Female", "Other"]) 
        height = st.text_input("Height in meters (leave blank to keep)", placeholder="e.g., 1.75")
        weight = st.text_input("Weight in kg (leave blank to keep)", placeholder="e.g., 70.5")
        submitted = st.form_submit_button("✅ Update Patient")

    if submitted:
        if not pid.strip():
            st.error("Patient ID is required for update")
            return

        payload: Dict[str, Any] = {}
        if name.strip():
            payload["name"] = name.strip()
        if city.strip():
            payload["city"] = city.strip()
        if age.strip():
            try:
                payload["age"] = int(age.strip())
            except ValueError:
                st.error("Age must be an integer")
                return
        if gender != "Select":
            payload["gender"] = gender
        if height.strip():
            try:
                payload["height"] = float(height.strip())
            except ValueError:
                st.error("Height must be a number")
                return
        if weight.strip():
            try:
                payload["weight"] = float(weight.strip())
            except ValueError:
                st.error("Weight must be a number")
                return

        if not payload:
            st.info("No fields to update — modify at least one field.")
            return

        with st.spinner("Updating patient..."):
            resp = update_patient(pid.strip(), payload)

        if resp.get("ok"):
            st.success("Patient updated successfully ✅")
            st.json(resp.get("data"))
        else:
            err = resp.get("data") or resp.get("error") or {}
            st.error(f"Failed to update patient: {err}")


def page_delete() -> None:
    st.header("Delete Patient")
    st.warning("⚠️ Warning: This will permanently delete the patient record from the backend.")
    st.info("📝 Enter Patient ID (e.g., P001) and confirm to proceed with deletion.")

    pid = st.text_input("Patient ID to delete", placeholder="e.g., P001")
    confirm = st.checkbox("I confirm I want to delete this patient")
    if st.button("🗑️ Delete Patient"):
        if not pid.strip():
            st.error("Please provide Patient ID")
            return
        if not confirm:
            st.warning("Please confirm deletion by checking the box.")
            return

        with st.spinner("Deleting patient..."):
            resp = delete_patient(pid.strip())

        if resp.get("ok"):
            st.success("Patient deleted ✅")
            st.json(resp.get("data"))
        else:
            err = resp.get("data") or resp.get("error") or {}
            st.error(f"Failed to delete patient: {err}")


def page_sort() -> None:
    st.header("Sort Patients")
    st.markdown("Sort the patients returned by the backend and review summary statistics.")

    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["height", "weight", "BMI"])
    with col2:
        order = st.selectbox("Order", ["asc", "desc"])

    if st.button("📊 Sort"):
        sort_key = sort_by.lower()
        order_key = order.lower()
        with st.spinner("Fetching sorted patients..."):
            resp = sort_patients(sort_key, order_key)

        if not resp.get("ok"):
            err = resp.get("data") or resp.get("error") or {}
            st.error(f"Failed to sort patients: {err}")
            return

        data = resp.get("data")
        # Expect data to be a list of patient dicts
        try:
            df = pd.DataFrame(data)
        except Exception:
            st.error("Unexpected response format from server")
            st.json(data)
            return

        if df.empty:
            st.info("No patients returned.")
            return

        # Compute BMI if not present
        if "BMI" not in df.columns and not "bmi" in df.columns:
            if "height" in df.columns and "weight" in df.columns:
                df["BMI"] = df.apply(lambda r: calculate_bmi(r.get("weight", None), r.get("height", None)), axis=1)

        st.dataframe(df)

        # Summary statistics
        total = len(df)
        avg_bmi = df["BMI"].dropna().astype(float).mean() if "BMI" in df.columns else None
        avg_height = df["height"].dropna().astype(float).mean() if "height" in df.columns else None
        avg_weight = df["weight"].dropna().astype(float).mean() if "weight" in df.columns else None

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Patients", total)
        c2.metric("Avg BMI", round(avg_bmi, 2) if avg_bmi is not None else "—")
        c3.metric("Avg Height (m)", round(avg_height, 2) if avg_height is not None else "—")
        c4.metric("Avg Weight (kg)", round(avg_weight, 2) if avg_weight is not None else "—")


def main() -> None:
    st.set_page_config(page_title="Patient Management System", page_icon="🏥", layout="wide")
    set_styles()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Create Patient", "View Patient", "Update Patient", "Delete Patient", "Sort Patients"]) 

    # Route to pages
    if page == "Home":
        page_home()
    elif page == "Create Patient":
        page_create()
    elif page == "View Patient":
        page_view()
    elif page == "Update Patient":
        page_update()
    elif page == "Delete Patient":
        page_delete()
    elif page == "Sort Patients":
        page_sort()


if __name__ == "__main__":
    main()




