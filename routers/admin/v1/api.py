from typing import List
from fastapi import APIRouter, Depends, Path, Query,Header,status,Response
import routers.admin.v1.schemas as schemas
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

import routers.admin.v1.crud.students as students


#A post request for login 
@router.post('/students/login', response_model=schemas.StudentLoginResponse,tags=["Students"])

def login_student(
    student: schemas.StudentLogin,
    db: Session = Depends(get_db)
):
    db_student = students.sign_in(db, student)
    return db_student

# A post request for creating a student
@router.post("/students", tags=["Students"])
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
    token:str = Header(None),
    db: Session = Depends(get_db),
):
    students.verify_token(db=db,token=token)
    all_students = students.get_students(
        db=db, skip=skip, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return all_students


@router.get(
    "/students/all_students", response_model=List[schemas.StudentShow], tags=["Students"]
)
def get_all_students( token:str = Header(None),db: Session = Depends(get_db)):
    students.verify_token(db=db,token=token)
    all_students = students.get_all_students(db=db)
    return all_students


# A get request to get a student by an id
@router.get(
    "/students/{student_id}", response_model=schemas.StudentShow, tags=["Students"]
)
def get_player_by_id(
    student_id: str = Path(..., min_length=36, max_length=36),
    token:str = Header(None),
    db: Session = Depends(get_db),
):
    students.verify_token(db=db,token=token)
    db_student = students.get_student(db=db, student_id=student_id)

    return db_student


# update function to update students data
@router.put(
    "/students/{student_id}", response_model=schemas.StudentShow, tags=["Students"]
)
def update_student(
    student: schemas.StudentUpdate,
    token:str = Header(None),
    db: Session = Depends(get_db),
    student_id: str = Path(...,  min_length=36, max_length=36),
):
    students.verify_token(db=db,token=token)
    return students.update_student(db=db, student_id=student_id, student=student)


# A delete request for deleting a student from its id
@router.delete(
        "/students/{student_id}",
        tags=["Students"]
)
def delete_student(
    student_id: str = Path(..., min_length=36, max_length=36),
    token:str = Header(None),
    db: Session = Depends(get_db),
):
    students.verify_token(db=db,token=token)
    students.delete_student(db, student_id=student_id)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
