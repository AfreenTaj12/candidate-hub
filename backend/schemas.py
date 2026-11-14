from pydantic import BaseModel, EmailStr, ConfigDict


class CandidateRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CandidateLogin(BaseModel):
    email: EmailStr
    password: str

class CandidateProfileUpdate(BaseModel):
    name: str


class CandidateProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)