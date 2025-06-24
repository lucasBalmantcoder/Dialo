from scr.db import db
from scr.controllers.models.models import AuditLog

def log_audit(user_id, action, details=None):
    entry = AuditLog(user_id=user_id, action=action, details=details)
    db.session.add(entry)
    db.session.commit()
