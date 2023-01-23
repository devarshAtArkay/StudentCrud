from typing import List
from fastapi import APIRouter, Depends, Path, Query
import routers.admin.v1.schemas as schemas

from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

import routers.admin.v1.crud.students as students

# A post request for creating a student
@router.post("/student", tags=["Students"])
def create_student(student: schemas.StudentBase, db: Session = Depends(get_db)):

    return students.create_student(db=db, student=student)


# A get request for getting the students with skip and limit,sortby,search,order
@router.get("/students", response_model=schemas.StudentList, tags=["Students"])
def get_students(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = Query(
        "all",
        min_length=3,
        max_length=10,
        description="sort by name, email, class, stream, roll_no",
    ),
    order: str = Query(
        "all", min_length=3, max_length=4, description="Enter either asc or desc"
    ),
    search: str = Query(
        "all",
        min_length=1,
        max_length=50,
        description="Search by first_name,last_name,email",
    ),
    db: Session = Depends(get_db),
):
    all_students = students.get_students(
        db=db, skip=skip, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return all_students


@router.get(
    "/all_students", response_model=List[schemas.StudentShow], tags=["Students"]
)
def get_all_students(db: Session = Depends(get_db)):
    all_students = students.get_all_students(db=db)
    return all_students


# A get request to get a student by an id
@router.get(
    "/student/{student_id}", response_model=schemas.StudentShow, tags=["Students"]
)
def get_player_by_id(
    student_id: str = Path(default=None, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_student = students.get_student(db=db, student_id=student_id)

    return db_student


# update function to update students data
@router.put(
    "/student/{student_id}", response_model=schemas.StudentShow, tags=["Students"]
)
def update_student(
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    student_id: str = Path(default=None, min_length=36, max_length=36),
):

    return students.update_student(db=db, student_id=student_id, student=student)


# A delete request for deleting a student from its id
@router.delete("/student/{student_id}", tags=["Students"])
def delete_student(
    student_id: str = Path(default=None, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):

    students.delete_student(db, student_id=student_id)
    return {"message:student has been deleted"}
