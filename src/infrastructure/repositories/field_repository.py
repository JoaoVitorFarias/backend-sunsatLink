from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

@dataclass
class fieldInfo:
    """Classe para armazenar informações sobre os campos de um modelo"""
    status: bool
    detail: str


class FieldValidation:
    """Validação quanto ao formato dos dados (não valida lógicas de negócio))"""
    @classmethod
    def nameValidation(cls, nome: str) -> fieldInfo:
        if len(nome) > 70:
            return fieldInfo(False, "Nome muito grande")
        elif len(nome) == 0:
            return fieldInfo(False, "Nome não pode ser vazio")
        return fieldInfo(True, "Nome válido")

    @classmethod
    def emailValidation(cls, email: str) -> fieldInfo:
        if len(email) > 100:
            return fieldInfo(False, "Email muito grande")

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return fieldInfo(False, "Email inválido")

        return fieldInfo(True, "Email válido")
    
    @classmethod
    def passwordValidation(cls, password: str) -> fieldInfo:
        if len(password) < 6:
            return fieldInfo(False, "The password is too small")

        return fieldInfo(True, "Valid password")