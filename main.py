# Importing the necessary libraries and modules
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import *
from typing import Annotated, Literal, Optional
import json


app = FastAPI() #creating an instance of FastAPI

# Defining the Patient model using Pydantic BaseModel
class Patient(BaseModel):
    id:     Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:   Annotated[str,Field(...,description='Name of the patient')]
    city:   Annotated[str,Field(...,description='City of the patient')]
    age:    Annotated[int,Field(...,gt=0,lt=120 ,description='Age of the patient')]
    gender: Annotated[Literal['Male','Female','Others'],str,Field(..., description='Gender of the patient')]
    height: Annotated[float,Field(...,gt=0,description='Height of the patient in meters')]
    weight: Annotated[float,Field(...,gt=0, description='Weight of the patient in kilograms')]

    @computed_field()                   # decorator to indicate that this field is computed based on other fields.
    @property
    def bmi(self) -> float:             # method to calculate BMI based on weight and height.
        bmi = round(self.weight / (self.height**2),2)
        return bmi

    @computed_field()
    @property
    def verdict(self) -> str:           # method to determine the BMI category based on the calculated BMI value.
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 25:
            return 'Normal weight'
        elif 25 <= self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

#
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# Function to load patient data from a JSON file.
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


# Defining the root endpoint of the API that returns a welcome message.
@app.get("/")
def hello():
    return {"message": "Patient management system API "}

# Defining an endpoint to provide information about the API.
@app.get('/about')
def about():
    return {'message':' An API to manage the patients records '}

# Defining an endpoint to view the details of a specific patient based on their patient ID.
@app.get("/patients/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="""
        ID of the patient in the database.
        """,
        example="P001"
    )
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")

# Defining an endpoint to sort patients based on specified criteria (height, weight, or BMI) and order (ascending or descending)
@app.get('/sort')
def sort_patients(sort_by: str=Query(..., description='Sort on the basis of height, weight or BMI.'),
                  order: str=Query('asc', description='Order of sorting either ascending or descending')):

    valid_fields = ['height', 'weight', 'BMI']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")

    if order not in ['aesc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'aesc' or 'desc'")

    data = load_data()

    sort_order = True if order == 'aesc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# Defining an endpoint to create a new patient record in the database.
@app.post('/create')
def create_patient(patient: Patient):

    data = load_data()

    # check if id already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    # add new patient to the db
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)

    # return a JSON response indicating successful creation of the patient record.
    return JSONResponse(status_code=201,content={'message': 'Patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str,  patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient[key] = value

    existing_patient['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient)
    existing_patient = patient_pydantic_object.model_dump(exclude={'id'})


    data[patient_id] = existing_patient
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def del_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})