from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


class PositionBase(SQLModel):
    name: str = Field(index=True)
    description: str


class Position(PositionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    employees: List["Employee"] = Relationship(back_populates="position")


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: int


class PositionUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentBase(SQLModel):
    name: str = Field(index=True)
    location: str


class DepartmentUpdate(SQLModel):
    name: Optional[str] = None
    location: Optional[str] = None


class Department(DepartmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    employees: List["Employee"] = Relationship(back_populates="department")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int


class EmployeeBase(SQLModel):
    email: str = Field(unique=True)
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    position_id: Optional[int] = Field(default=None, foreign_key="position.id")
    name: str = Field(index=True)
    salary: float
    hireDate: datetime


class EmployeeUpdate(SQLModel):
    email: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    name: Optional[str] = None
    salary: Optional[float] = None
    hireDate: Optional[datetime] = datetime.now()


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    position: Optional[Position] = Relationship(back_populates="employees")
    department: Optional[Department] = Relationship(back_populates="employees")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


db_url = f"postgresql://postgres:12345@localhost/EMPLOYEESTEE"

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


create_db_and_tables()
