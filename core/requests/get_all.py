async def get_all_request(offset: int = 0, limit: int = 100, order_by: str = None):
    """ Dependencies with the common parameters for look for in a list """
    return {
        "offset": offset,
        "limit": limit,
        "order_by":  order_by
    }
