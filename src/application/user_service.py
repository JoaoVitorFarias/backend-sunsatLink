from domain.entities.user import PerfilUsuarioEnum, Status, UserBase, UserDB, UserRequest, UserBase
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from domain.repositories.user_repository import UserRepositoryBaseModel
from fastapi import HTTPException, status
from infrastructure.repositories.field_repository import FieldValidation
from security import get_password_hash, verify_password
from jose import JWTError

class UserService:
    __usersRepository__: UserRepositoryBaseModel
    __tokensRepository__: TokensRepositoryBaseModel

    def __init__(
        self, usersRepository: UserRepositoryBaseModel,
        tokensRepository: TokensRepositoryBaseModel,
    ):
        self.__usersRepository__ = usersRepository
        self.__tokensRepository__ = tokensRepository
        

    def login(self, email: str, password: str) -> list[str, str, PerfilUsuarioEnum]:
        user = self.__usersRepository__.find_by_email(email)
        
        if not user or not verify_password(password, user.password):
            return None

        userToken = self.__tokensRepository__.createUserToken(user.email)
        refreshToken = self.__tokensRepository__.createRefreshToken(
            user.email)

        return (userToken, refreshToken, user.userRole, user.status)

    def verifyToken(self, token: str) -> UserBase:
        try:
            # Supõe-se que este método lance uma exceção se o token não for válido
            userLogin = self.__tokensRepository__.verifyToken(token=token)
            
            # Supõe-se que este método retorne None se o usuário não for encontrado
            user = self.__usersRepository__.find_by_email(userLogin)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user
        except JWTError as e:
            # Captura erros específicos relacionados ao JWT
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            # Captura outros tipos de exceções que você espera que possam acontecer
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
        isRefreshTokenValid = self.__tokensRepository__.verifyToken(
            token=refresh_token)

        if isRefreshTokenValid:
            return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)
        return None

            
    def find_by_email(self, email: str) -> UserBase | None:
        """Dado o email do user, retorna o objeto user, ou None se não existir"""
        return self.__usersRepository__.find_by_email(email=email)

    def find_all(self) -> list[UserDB]:
        """Faz uma query de todos os objetos User na DB,
        e retorna somente com os atributos User"""
        users_db = self.__usersRepository__.find_all()
        users = list()

        for user_db in  users_db:
            user = UserBase(
                email=user_db.email,
                name=user_db.name,
                password=user_db.password,
                userRole=user_db.userRole,
                status=user_db.status
            )
            users.append(user)
        
        return users

    def validate_user(self, user: UserRequest) -> dict:
        """Função para validar os campos de um objeto User"""

        fieldInfoDict = {
            "nome": vars(FieldValidation.nameValidation(user.name)),
            "email": vars(FieldValidation.emailValidation(user.email)),
            "password": vars(FieldValidation.passwordValidation(user.password))
        }

        completeStatus = all(info["status"] for info in fieldInfoDict.values())
        fieldInfoDict["completeStatus"] = completeStatus

        return fieldInfoDict

    def exists_by_email(self, email: str) -> bool:
        """Função para verificar se existe um objeto User com o email dado"""
        return self.__usersRepository__.find_by_email(email) is not None
    
    def delete_refresh_token(self, refresh_token: str):
        self.__tokensRepository__.delete_refresh_token(refresh_token)
        return None

    def save(self, user_request: UserRequest) -> UserDB:
        """Função para salvar um objeto User na DB, utilizada também como update"""

        newUser = UserDB()

        newUser.email = user_request.email
        newUser.name = user_request.name
        newUser.password = get_password_hash(user_request.password)
        newUser.status = Status.PENDING
        newUser.userRole = PerfilUsuarioEnum.USER

        return self.__usersRepository__.save(userSent=newUser)
    
    def update(self, user_model: UserRequest) -> UserDB:
        user_created = self.find_by_email(email=user_model.email)
        
        user_created.name = user_model.name
        return self.__usersRepository__.save(userSent=user_created)


    def delete_by_email(self, email: str) -> None:
        """Função para excluir um objeto User da DB dado o email"""
        self.__usersRepository__.delete_by_email(email=email)

    def update_approval_status(self, user: UserDB, status: int) -> UserDB:
        print(Status(status))
        user.status = Status(status)
        return self.__usersRepository__.save(user)

    def promote_user_to_admin(self, user: UserDB) -> UserDB:
        user.userRole = PerfilUsuarioEnum.ADMIN
        return self.__usersRepository__.save(user)