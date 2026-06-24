from sqlalchemy import or_

def generic_search( query, model, fields, keyword):
    conditions = []
    for field in fields:
        conditions.append(getattr(model, field).ilike(f"%{keyword}%"))
    return (query.filter(or_(*conditions)).all())

def paginate(query, page: int = 1, size: int = 10):
    offset = (page - 1) * size
    total = query.count()
    records = (query.offset(offset).limit(size).all())
    return {"total": total, "page": page, "size": size, "records": records}

def filter_records(query, filters: dict):
    for key, value in filters.items():
        if value is not None:
            query = query.filter_by(**{key: value})
    return query.all()