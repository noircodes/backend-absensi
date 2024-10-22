from functools import lru_cache
import json
from typing import Any, TypeVar
from bson.objectid import ObjectId as BsonObjectId
from fastapi.encoders import ENCODERS_BY_TYPE, jsonable_encoder
from pydantic import BaseModel as _BaseModel, ConfigDict, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue


class ObjectIdStr(BsonObjectId):

    invalid_object_id = "invalid_object_id"
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        
        def validate_from_str(value: str) -> ObjectIdStr:
            try:
                result = ObjectIdStr(value)
            except:
                raise ValueError("Invalid ObjectIdStr")
            return result

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        def validate_from_BsonObjectId(value: BsonObjectId) -> ObjectIdStr:
            try:
                result = ObjectIdStr(value)
            except:
                raise ValueError("Invalid ObjectIdStr")
            return result
        
        from_BsonObjectId_schema = core_schema.chain_schema(
            [
                core_schema.is_instance_schema(BsonObjectId),
                core_schema.no_info_plain_validator_function(validate_from_BsonObjectId),
            ]
        )

        def serialize(value: Any, info: core_schema.SerializationInfo) -> str | ObjectIdStr:
            if info.mode == 'json':
                return str(value)
            else:
                return ObjectIdStr(value)

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectIdStr),
                    from_BsonObjectId_schema,
                    from_str_schema,
                ],
                custom_error_message="Bukan object Id",
                custom_error_type=ObjectIdStr.invalid_object_id
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                info_arg=True,
                when_used='always',
            ),
            ref="ObjectIdStr"
        )
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema.str_schema())
        json_schema.update(
            type="string",
            description="ObjectIdStr",
            examples=["000000000000000000000000"],
            example="000000000000000000000000"
        )
        return json_schema

class BaseModel(_BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_attribute_docstrings=True
    )

    @classmethod
    @lru_cache(maxsize=None)
    def Projection(cls):
        return {s if m.alias is None else m.alias: 1 for s, m in cls.model_fields.items()}
    
    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> 'BaseModel':
        try:
            ret = super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)
            return ret
        except Exception as err:
            print("model_validate error:", err)
            raise err
        
    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> 'BaseModel':
        try:
            ret = super().model_validate_json(json_data, strict=strict, context=context)
            return ret
        except Exception as err:
            print("model_validate_json error:", err)
            raise err
        
    def MsJsonString(self) -> str:
        d = self.model_dump(mode="json")
        return json.dumps(
            jsonable_encoder(d),
            sort_keys=True,
            indent=0,
            separators=None
        )
    
ENCODERS_BY_TYPE[ObjectIdStr] = str
ENCODERS_BY_TYPE[BsonObjectId] = str

TGenericBaseModel = TypeVar("TGenericBaseModel", bound=BaseModel)