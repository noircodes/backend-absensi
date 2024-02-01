from typing import Any, Dict

import pymongo
from motor.core import AgnosticClientSession, AgnosticCollection

from utils.pagination.model_pagination_util import (MsPagination, MsPaginationResult,
                                             QuerySortingOrder,
                                             TGenericPaginationModel)
async def Paginate(
    collection: AgnosticCollection,
    query_filter: Dict[Any, Any],
    params: MsPagination,
    session: AgnosticClientSession = None,
    resultItemsClass: TGenericPaginationModel = TGenericPaginationModel, # must derived from BaseModel
    **kwargs: Any,
) -> MsPaginationResult[TGenericPaginationModel]:
    query_filter = query_filter or {}
    total = await collection.count_documents(query_filter)
    offset = params.size * (params.page - 1)
    cursor = collection.find(
        query_filter,
        {s if m.alias is None else m.alias: 1 for s, m in resultItemsClass.__fields__.items()},
        skip=offset,
        limit=params.size,
        session=session,
        **kwargs
    )
    if (params.sortby is not None) and (len(params.sortby) > 0):
        if params.order is None:
            params.order = QuerySortingOrder.Ascending
        cursor.sort(params.sortby, pymongo.ASCENDING if params.order == QuerySortingOrder.Ascending else pymongo.DESCENDING)
    items = await cursor.to_list(length=params.size)

    return MsPaginationResult[resultItemsClass](
        sortby=params.sortby,
        size=params.size,
        page=params.page,
        order=params.order,
        total=total,
        items=items,
    )