from domain.entities.user import UserDB, UserBase
from typing import Protocol, runtime_checkable

@runtime_checkable
class UserRepositoryBaseModel(Protocol):

    def find_all(self) -> list[UserDB]:
        '''Função para fazer uma query de todas as User da DB'''
        ...

    def find_by_email(self, email: str) -> UserDB | None:
        '''Função para fazer uma query por email de um objeto User na DB'''
        ...

    def save(self, userSent: UserDB) -> UserDB:
        '''Função para salvar um objeto user na DB'''
        ...

    def delete_by_email(self, email: str) -> None:
        '''Função para excluir um objeto user da DB dado o email'''
        ...

    def validate_user(self, user: UserBase) -> dict:
        '''Função para validar os campos de um objeto user'''
        ...