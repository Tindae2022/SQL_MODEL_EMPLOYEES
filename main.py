from fastapi import FastAPI
from App.api.positions import router as positio_router
from App.api.departments import router as department_router
from App.api.employees import router as employee_router

app = FastAPI(title="Tindae Company", version="0.0.1")

app.include_router(positio_router)
app.include_router(department_router)
app.include_router(employee_router)