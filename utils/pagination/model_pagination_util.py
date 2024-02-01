from enum import Enum
from typing import Generic, List, TypeVar

from fastapi import Query
from pydantic import Field
from pydantic.generics import GenericModel

from utils.datatypes_util import BaseModel


class QuerySortingOrder(str, Enum):
    Ascending = "asc"
    Descending = "dsc"

class MsPagination(BaseModel):

    sortby: str = Field(
        default=None,
        example="createdTime"
    )
    size: int = Field(
        default=100,
        ge=1,
        le=100
    )
    page: int = Field(
        default=1,
        ge=1,
    )
    order: QuerySortingOrder = Field(
        default=QuerySortingOrder.Ascending
    )

    @classmethod
    def QueryParam(
        cls,
        sortby: str = Query(
            default="createdTime",
            description="Sort by field name"
        ),
        size: int = Query(
            default=10,
            ge=1,
            le=100,
            description="Number of items per page"
        ),
        page: int = Query(
            default=1,
            ge=1,
            description="Page number"
        ),
        order: QuerySortingOrder = Query(
            default=QuerySortingOrder.Ascending,
            description="Sorting order"
        )
    ) -> 'MsPagination':
        return cls(
            sortby=sortby,
            size=size,
            page=page,
            order=order
        )
    
TGenericPaginationModel = TypeVar("TGenericPaginationModel") # must derived from BaseModel
    
class MsPaginationResult(GenericModel, Generic[TGenericPaginationModel]):

    sortby: str = Field(
        default=None,
        example="_id"
    )
    size: int = Field(
        default=...,
        example=100
    )
    page: int = Field(
        default=...,
        example=1
    )
    order: QuerySortingOrder = Field(
        default=QuerySortingOrder.Ascending,
        example=QuerySortingOrder.Ascending
    )
    total: int = Field(
        default=...,
        example=10
    )
    items: List[TGenericPaginationModel] = Field(
        default=...
    )
