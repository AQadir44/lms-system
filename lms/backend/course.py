from ..models import User , Course
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from ..database import get_db 
from lms import course_pb2

router = APIRouter()

@router.get('/courses/', status_code=status.HTTP_200_OK)
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()

    return {
        "status": 'success',
        "courses": courses
    }

@router.post('/courses/', status_code=status.HTTP_201_CREATED)
def signup(payload: Course, db: Session = Depends(get_db)):

    course = Course(**payload.model_dump())

    db.add(course)

    db.commit()

    db.refresh(course)

    return {
        "status": 'success',
        "course": course
    }


@router.patch('/{course_id}', status_code=status.HTTP_202_ACCEPTED)
def create_course(course_id : str , payload: Course, db: Session = Depends(get_db)):

    course_query = db.query(Course).filter(Course.id == course_id)
    db_course = course_query.first()
    
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f'No course with this id : {course_id}')
    
    update_data = payload.model_dump(exclude_unset=True)
    
    course_query.filter(Course.id == course_id).update(update_data , synchronize_session=False)
    
    db.commit()
    
    db.refresh(db_course)
    return {
        "status": 'success',
        "courses": db_course
    }


@router.get('/{course_id}')
def get_post(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No course with this id: {course_id} found")
    return {"status": "success", "course": course}

@router.delete('/{course_id}')
def delete_post(course_id: str, db: Session = Depends(get_db)):
    course_query = db.query(Course).filter(Course.id == course_id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No course with this id: {id} found')
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
