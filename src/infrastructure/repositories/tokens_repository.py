from datetime import datetime, timedelta
from jose import jwt
from typing import Union, Any
from domain.entities.tokens import RefreshTokens
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from security import ACCESS_TOKEN_EXPIRE_HOURS, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_HOURS
from domain.repositories.tokens_repository import TokensRepositoryBaseModel

class TokensRepository():
  __RefreshTokens__: list[RefreshTokens] = []

  def createUserToken(self, subject: Union[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS
        )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encoded_jwt

  def createRefreshToken(self, email: str) -> str:
      expire = datetime.utcnow() + timedelta(
          hours=REFRESH_TOKEN_EXPIRE_HOURS
      )
      to_encode = {"exp": expire, "sub": email}
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

      for token in self.__RefreshTokens__:
        if token.email == email:
          token.refreshToken = encoded_jwt
          break

      id = len(self.__RefreshTokens__)
      self.__RefreshTokens__.append(RefreshTokens(id=id, email=email, refreshToken=encoded_jwt))
      return encoded_jwt

  '''Returns userToken and refreshToken'''
  def refreshToken(self, refresh_token: str) -> tuple[str, str] | None:
    refresh_token = refresh_token.split(" ")[1]
    for index, token in enumerate(self.__RefreshTokens__):
      if(token.refreshToken == refresh_token):
        self.__RefreshTokens__[index].refreshToken = self.createRefreshToken(token.email)

        newRefreshToken = token.refreshToken
        newUserToken = self.createUserToken(token.email)
        return (newUserToken, newRefreshToken)

    return None
  
  def verifyToken(self, token: str) -> Any:
    decodedJwt = jwt.decode(token.split(" ")[1], SECRET_KEY, ALGORITHM).get('sub')
    
    return decodedJwt

  def delete_refresh_token(self, refresh_token: str) -> None:
      for index, token in enumerate(self.__RefreshTokens__):
        if(token.refreshToken == refresh_token):
          self.__RefreshTokens__.pop(index)
          break

assert isinstance(TokensRepository(), TokensRepositoryBaseModel)
