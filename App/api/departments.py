from typing import Optional, List
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlmodel import select, Session
from App.api.models import get_session
from App.api.models import Department, DepartmentBase, DepartmentCreate, DepartmentRead, DepartmentUpdate

router = APIRouter(tags=["Department"], prefix="/department")


@router.post("/", response_model=DepartmentRead)
def create_department(*, session: Session = Depends(get_session), department: DepartmentCreate):
    db_department = Department.from_orm(department)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department


@router.get("/{department_id}", response_model=DepartmentRead)
def read_department_by_id(*, session: Session = Depends(get_session), department_id: int):
    db_department = session.get(Department, department_id)
    if not db_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return db_department


@router.get("/", response_model=List[DepartmentRead])
def raed_all_departments(*, session: Session = Depends(get_session),
                         offset: int = 0,
                         limit: int = Query(default=100, lte=100)):
    db_department = session.exec(select(Department).offset(offset).limit(limit)).all()
    return db_department


@router.patch("/{department_id}", response_model=DepartmentRead)
def update_department(*, department_id: int,
                      department: DepartmentUpdate,
                      session: Session = Depends(get_session)
                      ):
    db_department = session.get(Department, department_id)
    if not db_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    department_data = department.dict(exclude_unset=True)
    for key, value in department_data.items():
        setattr(db_department, key, value)
        session.add(db_department)
        session.commit()
        session.refresh(db_department)
        return db_department


@router.delete("/{department_id}")
def delete_department(department_id: int, session: Session = Depends(get_session)):
    db_department = session.get(Department, department_id)
    if not db_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    session.delete(db_department)
    session.commit()
    return f"The department with id {department_id} has been deleted successfully"
