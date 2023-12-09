from typing import List
import pydantic
from pydantic import BaseModel

class Question(BaseModel):
    name: str | None
    type: str
    answers: List[pydantic.StrictInt | pydantic.StrictStr]
    right_answer: List[pydantic.StrictInt | pydantic.StrictStr]

class Test(BaseModel):
    name: str
    questions: List[Question]


class UserSolvedQuestion(BaseModel):
    type: str
    right_answer: List[pydantic.StrictInt | pydantic.StrictStr]


class UserSolvedTest(BaseModel):
    id: str
    questions: List[UserSolvedQuestion]