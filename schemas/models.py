import pydantic
class Ticker(pydantic.BaseModel):
    SYMBOL: str
    NAME_OF_COMPANY: str


    
