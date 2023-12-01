from domain.entities.user import UserDB, UserBase
from domain.repositories import user_repository
from .field_repository import FieldValidation
from sqlalchemy.orm import Session
from typing import Callable

class UserRepository:

    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session

    def find_all(self) -> list[UserDB]:
        session = self.database()
        res = session.query(UserDB).all()
        session.close()
        return res
    

    def find_by_email(self, email : str) -> UserDB | None:
        session = self.database()
        return session.query(UserDB).filter(UserDB.email == email).first()


    def save(self, userSent: UserDB) -> UserDB:
        session = self.database()
        userUpdated = session.merge(userSent)
        session.commit()
        session.refresh(userUpdated)
        return userUpdated
    

    def delete_by_email(self, email: str) -> None:
        session = self.database()
        user_object = session.query(UserDB).filter(
            UserDB.email == email).first()

        if user_object is not None:
            session.delete(user_object)
            session.commit()

        session.close()

    
    def validate_user(self, user : UserBase) -> dict:

        fieldInfoDict = {}
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            user.email))
        fieldInfoDict["name"] = vars(FieldValidation.nameValidation(
            user.name))
        fieldInfoDict["password"] = vars(FieldValidation.passwordValidation(
            user.password))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict
    
        
assert isinstance(UserRepository(
    {}), user_repository.UserRepositoryBaseModel)
