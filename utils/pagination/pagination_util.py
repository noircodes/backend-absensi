from typing import Any, Dict

import pymongo
from config.mongodb_type_checking import TMongoCollection, TMongoClientSession

from utils.pagination.model_pagination_util import (MsPagination, MsPaginationResult,
                                             QuerySortingOrder,
                                             TGenericPaginationModel)
async def Paginate(
    collection: TMongoCollection,
    query_filter: Dict[Any, Any],
    params: MsPagination,
    resultItemsClass: type[TGenericPaginationModel], # must derived from BaseModel
    session: TMongoClientSession | None = None,
    **kwargs: Any,
) -> MsPaginationResult[TGenericPaginationModel]:
    query_filter = query_filter or {}
    total = await collection.count_documents(query_filter)
    offset = params.size * (params.page - 1)
    cursor = collection.find(
        query_filter,
        {s if m.alias is None else m.alias: 1 for s, m in resultItemsClass.model_fields.items()},
        skip=offset,
        limit=params.size,
        session=session,
        **kwargs
    )
    if (params.sortby is not None) and (len(params.sortby) > 0):
        if params.order is None:
            params.order = QuerySortingOrder.Ascending
        cursor.sort(params.sortby, pymongo.ASCENDING if params.order == QuerySortingOrder.Ascending else pymongo.DESCENDING)
    items: list[dict[str, Any]]= await cursor.to_list(length=params.size) # type: ignore

    return MsPaginationResult[resultItemsClass](
        sortby=params.sortby,
        size=params.size,
        page=params.page,
        order=params.order,
        total=total,
        items=[resultItemsClass(**item) for item in  items],
    )