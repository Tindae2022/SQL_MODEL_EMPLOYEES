from typing import Optional, List
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlmodel import select, Session
from App.api.models import get_session
from App.api.models import Position, PositionBase, PositionCreate, PositionRead, PositionUpdate

router = APIRouter(tags=["Position"], prefix="/position")


@router.post("/", response_model=PositionRead)
def create_position(*, session: Session = Depends(get_session), position: PositionCreate):
    db_position = Position.from_orm(position)
    session.add(db_position)
    session.commit()
    session.refresh(db_position)
    return db_position


@router.get("/{position_id}", response_model=PositionRead)
def read_position_by_id(*, session: Session = Depends(get_session), position_id: int):
    db_position = session.get(Position, position_id)
    if not db_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return db_position


@router.get("/", response_model=List[PositionRead])
def read_all_positions(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100)
):
    db_position = session.exec(select(Position).offset(offset).limit(limit)).all()
    return db_position


'''@router.get("/Position/", response_model=List[PositionRead])
def read_positions(session: Session = Depends(get_session)):
    # with Session(engine) as session:
    position = session.exec(select(Position)).all()
    return position
'''


@router.patch("/{position_id}", response_model=PositionRead)
def update_position(*, position_id: int, position: PositionUpdate,
                    session: Session = Depends(get_session)
                    ):
    db_position = session.get(Position, position_id)
    if not db_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    position_data = position.dict(exclude_unset=True)
    for key, value in position_data.items():
        setattr(db_position, key, value)
        session.add(db_position)
        session.commit()
        session.refresh(db_position)
        return db_position


@router.delete("/{position_id}")
def delete_position(position_id: int, session: Session = Depends(get_session)):
    db_position = session.get(Position, position_id)
    if not db_position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    session.delete(db_position)
    session.commit()
    return f"The position with id {position_id} has been deleted successfully"
