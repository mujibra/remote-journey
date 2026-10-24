from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI(title="Job Application Tracker")

class ApplicationCreate(BaseModel):
    company: str
    position: str


@app.on_event("startup")
def startup():
    database.initialize_database()


@app.get("/applications")
def list_applications():
    return database.get_applications()

@app.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    try:
        application_id = database.add_application(
            application.company,
            application.position
        )

        return {
            "id": application_id,
            "company": application.company.strip(),
            "position": application.position.strip(),
            "status": "Applied"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )
    
class StatusUpdate(BaseModel):
    status: str

@app.patch("/applications/{application_id}")
def update_status(application_id: int, request: StatusUpdate):
    try:
        updated = database.update_application_status(
            application_id,
            request.status
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "id": application_id,
        "status": request.status
    }

@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    deleted = database.delete_application(application_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return None