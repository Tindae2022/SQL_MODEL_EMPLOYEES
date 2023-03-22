from typing import Optional, List
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlmodel import select, Session
from App.api.models import get_session
from App.api.models import Employee, EmployeeBase, EmployeeRead, EmployeeCreate, EmployeeUpdate

router = APIRouter(tags=["Employee"], prefix="/employee")


@router.post("/", response_model=EmployeeRead)
def create_employee(*, session: Session = Depends(get_session), employee: EmployeeCreate):
    db_employee = Employee.from_orm(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.get("/{employee_id}", response_model=EmployeeRead)
def read_employee_by_id(*, session: Session = Depends(get_session), employee_id: int):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return db_employee


@router.get("/", response_model=List[EmployeeRead])
def read_all_employees(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100)
):
    db_employee = session.exec(select(Employee).offset(offset).limit(limit)).all()
    return db_employee


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(*, employee_id: int, employee: EmployeeUpdate,
                    session: Session = Depends(get_session)
                    ):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    employee_data = employee.dict(exclude_unset=True)
    for key, value in employee_data.items():
        setattr(db_employee, key, value)
        session.add(db_employee)
        session.commit()
        session.refresh(db_employee)
        return db_employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    session.delete(db_employee)
    session.commit()
    return f"The employee with id {employee_id} has been deleted successfully"
