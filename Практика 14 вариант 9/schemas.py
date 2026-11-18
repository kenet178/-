from datetime import datetime
from typing import Literal
from pydantic import BaseModel,Field,ConfigDict,model_validator
Status=Literal['scheduled','delayed','boarding','cancelled','completed']
class FlightBase(BaseModel):
    number:str=Field(min_length=3,max_length=16)
    origin:str=Field(min_length=2,max_length=80)
    destination:str=Field(min_length=2,max_length=80)
    departure:datetime
    aircraft:str=Field(min_length=2,max_length=80)
    price:float=Field(gt=0)
    seats:int=Field(ge=0)
    status:Status='scheduled'
    @model_validator(mode='after')
    def different_airports(self):
        if self.origin==self.destination:raise ValueError('Отправление и назначение должны отличаться')
        return self
class FlightCreate(FlightBase):pass
class FlightPut(FlightBase):pass
class FlightPatch(BaseModel):
    origin:str|None=Field(default=None,min_length=2)
    destination:str|None=Field(default=None,min_length=2)
    departure:datetime|None=None
    aircraft:str|None=Field(default=None,min_length=2)
    price:float|None=Field(default=None,gt=0)
    seats:int|None=Field(default=None,ge=0)
    status:Status|None=None
class FlightOut(FlightBase):
    id:int
    model_config=ConfigDict(from_attributes=True)
