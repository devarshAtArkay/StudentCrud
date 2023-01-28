from datetime import datetime
from models import StudentModel
from fastapi import HTTPException, status
import routers.admin.v1.schemas as schemas
from sqlalchemy.orm import Session
from sqlalchemy import or_
from libs.utils import generate_id, now, object_as_dict
import bcrypt
from jwcrypto import jwk, jwt
from config import config
import json
import traceback


# A function to check whether the roll no is unique or not
def check_roll_no(db: Session, roll_no: str):

    check_roll_no = (
        db.query(StudentModel).filter(StudentModel.roll_no == roll_no).first()
    )

    if check_roll_no:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Enter unique Roll No",
        )


# A function to get encrypted Jwtoken
def get_token(student_id, email):
    claims = {"id": student_id, "email": email, "time": str(now())}

    # Create a signed token with the generated key
    key = jwk.JWK(**config["jwt_key"])
    Token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
    Token.make_signed_token(key)

    # Further encrypt the token with the same key
    encrypted_token = jwt.JWT(
        header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=Token.serialize()
    )
    encrypted_token.make_encrypted_token(key)
    token = encrypted_token.serialize()
    return token


# A function to get verified token
def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    else:
        try:
            key = jwk.JWK(**config["jwt_key"])
            ET = jwt.JWT(key=key, jwt=token)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            claims = ST.claims
            claims = json.loads(claims)
            print(claims)
            db_student = get_student_by_id(db, student_id=claims["id"])
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if db_student is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Student not found"
            )
        elif db_student.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Student not found"
            )
        return db_student


# A create password function which encryptes a password and returns it
def _create_password(password):
    password = bytes(password, "utf-8")
    password = bcrypt.hashpw(password, config['salt'])
    password = password.decode("utf-8")
    return password


# function which creates a student with unique roll no
def create_student(db: Session, student: schemas.StudentBase):

    check_roll_no(db=db, roll_no=student.roll_no)

    student = student.dict()
    student_id = generate_id()

    password = student["password"]

    student["password"] = _create_password(password)

    db_student = StudentModel(id=student_id, **student)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student.id


# A signin function which gets token and returns the loginschema
def sign_in(db: Session, student: schemas.StudentLogin):
    db_student = get_student_by_email(db, email=student.email)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif db_student.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    hashed = db_student.password
    hashed = bytes(hashed, "utf-8")
    password = bytes(student.password, "utf-8")
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
   
    db_student.token = get_token(db_student.id, db_student.email)
    return db_student


# gets all the students
def get_all_students(db: Session):

    db_student = (
        db.query(StudentModel)
        .filter(StudentModel.is_deleted == False)
        .order_by(StudentModel.first_name, StudentModel.last_name)
        .all()
    )
    return db_student


# gets all the students with searching and sorting od first_name,last_name, class_no,stream,roll_no
def get_student_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = None,
    order: str = None,
    search: str = None,
):

    query = db.query(StudentModel).filter(StudentModel.is_deleted == False)

    if query is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No student available to show"
        )

    if search != "all":

        text = f"""%{search}%"""
        query = query.filter(
            or_(
                StudentModel.first_name.like(text),
                StudentModel.last_name.like(text),
                StudentModel.email.like(text),
            )
        )

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(StudentModel.first_name, StudentModel.last_name)
        else:
            query = query.order_by(StudentModel.first_name, StudentModel.last_name)
    elif sort_by == "email":
        if order == "desc":
            query = query.order_by(StudentModel.email.desc())
        else:
            query = query.order_by(StudentModel.email)
    elif sort_by == "class":
        if order == "desc":
            query = query.order_by(StudentModel.class_no.desc())
        else:
            query = query.order_by(StudentModel.class_no)
    elif sort_by == "stream":
        if order == "desc":
            query = query.order_by(StudentModel.streams.desc())
        else:
            query = query.order_by(StudentModel.streams)

    elif sort_by == "roll_no":
        if order == "desc":
            query = query.order_by(StudentModel.roll_no.desc())
        else:
            query = query.order_by(StudentModel.roll_no)

    elif sort_by == "gender":
        if order == "desc":
            query = query.order_by(
                StudentModel.gender.desc(),
                StudentModel.first_name.desc(),
                StudentModel.last_name.desc(),
            )
        else:
            query = query.order_by(
                StudentModel.gender, StudentModel.first_name, StudentModel.last_name
            )

    else:
        query = query.order_by(StudentModel.created_at.desc())

    rows = query.offset(skip).limit(limit).all()
    count = query.count()
    # students = []
    # for row in rows:
    #     name = row.first_name + " " + row.last_name
    #     roll_no = "" if row.roll_no is None else str(row.roll_no)
    #     class_no = 0 if row.class_no is None else int(row.class_no)
    #     student = object_as_dict(row)
    #     student["name"] = name
    #     student["roll_no"] = roll_no
    #     student["class_no"] = class_no
    #     students.append(student)
    data = {"count": count, "list": rows}
    return data


# function which gets student by id
def get_student_by_id(db: Session, student_id: str):

    db_student = (
        db.query(StudentModel)
        .filter(StudentModel.id == student_id, StudentModel.is_deleted == False)
        .first()
    )
    if db_student is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No student available to show"
        )
    return db_student


# A function to get student by email
def get_student_by_email(db: Session, email: str):
    return (
        db.query(StudentModel)
        .filter(StudentModel.email == email, StudentModel.is_deleted == False)
        .first()
    )


# function which calls get_student_by_id column
def get_student(db: Session, student_id: str):
    db_student = get_student_by_id(db, student_id=student_id)

    return db_student


# updates student from the id
def update_student(db: Session, student_id: str, student: schemas.StudentUpdate):
    db_student = get_student_by_id(db=db, student_id=student_id)

    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.email = student.email
    db_student.gender = student.gender
    db_student.phone_no = student.phone_no
    db_student.class_no = student.class_no
    db_student.streams = student.streams
    db_student.updated_at = now()
    db.commit()
    db.refresh(db_student)
    return db_student


# deletes student from the id
def delete_student(db: Session, student_id: str):
    db_student = get_student_by_id(db=db, student_id=student_id)

    db_student.is_deleted = True
    db_student.updated_at = now()
    db.commit()
    # db.refresh(db_student)

    return
