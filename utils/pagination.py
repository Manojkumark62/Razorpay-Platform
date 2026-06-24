def paginate(query, page: int, size: int):
    total = query.count()
    offset = (page - 1) * size
    records = (query.offset(offset).limit(size).all())
    return {"total": total, "page": page, "size": size, "pages":(total + size - 1) // size, "records": records}