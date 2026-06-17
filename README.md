# Patient Management API

A simple Patient Management REST API built with **FastAPI** as a learning project to explore backend development in Python.

The API allows users to create, retrieve, update, delete, and sort patient records. Patient data is stored in a JSON file, and the application uses Pydantic models for data validation and automatic documentation generation.

## Features

* Create new patient records
* View patient details by ID
* Update existing patient information
* Delete patient records
* Sort patients by height, weight, or BMI
* Automatic BMI calculation
* BMI-based health verdict generation
* Request validation using Pydantic
* Interactive API documentation with Swagger UI

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* JSON

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/Patient-API.git
cd Patient-API
```

2. Create a virtual environment

```bash
python -m venv myenv
```

3. Activate the virtual environment

Windows:

```bash
myenv\Scripts\activate
```

4. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```


## API Endpoints

| Method | Endpoint                 | Description                |
| ------ | ------------------------ | -------------------------- |
| GET    | `/`                      | Welcome message            |
| GET    | `/about`                 | API information            |
| GET    | `/patients/{patient_id}` | Get patient details        |
| GET    | `/sort`                  | Sort patient records       |
| POST   | `/create`                | Create a new patient       |
| PUT    | `/edit/{patient_id}`     | Update patient information |
| DELETE | `/delete/{patient_id}`   | Delete a patient           |

Built as a backend development learning project using FastAPI.
