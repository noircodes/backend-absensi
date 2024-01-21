from typing import Any
from bson.objectid import ObjectId as BsonObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from pydantic import BaseModel as _BaseModel, ConfigDict, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue


class ObjectIdStr(BsonObjectId):
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        
        def validate_from_str(value: str) -> ObjectIdStr:
            result = ObjectIdStr(value)
            return result

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(BsonObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance),
                when_used="json"
            )
        )
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema.str_schema())
        json_schema.update(
            type="string",
            examples=[str(ObjectIdStr())],
        )
        return json_schema

class BaseModel(_BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    
ENCODERS_BY_TYPE[ObjectIdStr] = str
ENCODERS_BY_TYPE[BsonObjectId] = str