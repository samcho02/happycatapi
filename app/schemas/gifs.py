from bson.objectid import ObjectId
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import ConfigDict, BaseModel, HttpUrl, Field
from pydantic.functional_validators import BeforeValidator

'''
Adapted from MongoDB Getting Started With MongoDB and FastAPI tutorial: 
https://github.com/mongodb-developer/mongodb-with-fastapi/blob/master/app.py
'''

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class GIFmodel(BaseModel):
    """
    Container for a single cat GIF data.
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    url: HttpUrl = Field(...)
    tag: list[str] = Field(...)
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "happycat",
                "url": "https://tenor.com/bXAn9.gif",
                "tag": ["happy", "tabby"],
            }
        },
    )
    
class UpdateGIFmodel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    tag: Optional[list[str]] = None
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "happycat",
                "url": "https://tenor.com/bXAn9.gif",
                "tag": ["happy", "tabby"],
            }
        },
    )
    
class GIFcollection(BaseModel):
    """
    A container holding a list of `GIFmodel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    gifs: List[GIFmodel]
