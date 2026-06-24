from datetime import datetime

def soft_delete(db, model, record_id):
    record = (db.query(model).filter(model.id == record_id).first())
    if not record:
        return False
    record.is_deleted = True
    record.deleted_at = (datetime.utcnow())
    db.commit()
    return True