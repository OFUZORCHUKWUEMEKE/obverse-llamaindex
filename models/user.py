# from .base import BaseSchema
from typing import Optional , List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserSchema(BaseModel):
    """
    Container for a single User Record
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username:str
    telegram_id:str
    first_name:str
    last_name:str
    merchant_name:Optional[str]=None
    isAdmin:bool = False
    wallet_addresses:Optional[List[str]] = None
    total_transactions:int=0
    logo_url:Optional[str] = None
    model_config= ConfigDict(
        populate_by_name=True,
        aarbitrary_types_allowed=True,
    )

class UpdateUser(BaseModel):
    username:Optional[str]=None
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    merchant_name:Optional[str]=None
    logo_url:Optional[str]=None
    wallet_addresses:Optional[str]=None

class UserCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.
    """
    users:List[UserSchema]


