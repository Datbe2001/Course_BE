def calc_skip_record_query(page, limit):
    if not (page and limit):
        return None, None

    skip_record = (page - 1) * limit
    return skip_record, limit


def make_response_pagination(items, page, limit, total, meta=dict({})):
    meta.update({
        "page": page,
        "limit": limit,
        "total": total
    })
    return {
        "data": items,
        "meta": meta
    }
