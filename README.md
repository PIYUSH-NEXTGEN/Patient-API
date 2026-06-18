# 🏥 Patient Management System

A full-stack Patient Management System built with **FastAPI** and **Streamlit**.

Built as a learning project to explore Python backend and frontend development.

This project allows users to create, view, update, delete, and sort patient records through an interactive web interface.

---

## 🚀 Features

### Backend (FastAPI)

* Create new patient records
* Retrieve patient details using Patient ID
* Update existing patient information
* Delete patient records
* Sort patients by Height, Weight, or BMI
* Automatic BMI calculation
* BMI health verdict generation
* Request validation using Pydantic
* Interactive API documentation

### Frontend (Streamlit)

* Patient search with ID format guidance
* Create patient form
* Update patient records
* Delete patient records
* Sort and analyze patient data
* Backend status monitoring
* Responsive and user-friendly layout

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn
* Streamlit
* Pandas


---
## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PIYUSH-NEXTGEN/Patient-API.git
cd Patient-API
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate the Virtual Environment

Windows:

```bash
myenv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```


---

## 🎨 Running the Frontend

In a new terminal:

```bash
streamlit run frontend.py
```

Frontend URL:

Make sure the FastAPI backend is running before launching the frontend.

---

## 📌 API Endpoints

| Method | Endpoint                 | Description          |
| ------ | ------------------------ | -------------------- |
| GET    | `/`                      | Welcome message      |
| GET    | `/about`                 | API information      |
| GET    | `/patients/{patient_id}` | View patient details |
| GET    | `/sort`                  | Sort patient records |
| POST   | `/create`                | Create patient       |
| PUT    | `/edit/{patient_id}`     | Update patient       |
| DELETE | `/delete/{patient_id}`   | Delete patient       |

---

## 🧮 Patient Data

Each patient record contains:

* Patient ID
* Name
* City
* Age
* Gender
* Height
* Weight
* BMI
* Health Verdict

BMI and health verdicts are automatically calculated using patient height and weight.

---