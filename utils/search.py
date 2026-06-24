from sqlalchemy import or_

def search_records(query, model, keyword, fields):
    conditions = []
    for field in fields:
        conditions.append(getattr(model, field).ilike(f"%{keyword}%"))
    return query.filter(or_(*conditions))