def apply_filters(query, model, filters: dict):
    for field, value in filters.items():
        if value is not None:
            query = query.filter(getattr(model, field) == value)
    return query