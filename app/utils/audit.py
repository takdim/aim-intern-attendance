import json
from typing import Any, Optional

from app.extensions import db
from app.models import AuditLog


def log_action(actor_user_id: Optional[int], action: str, entity: str, entity_id: Optional[int] = None, metadata: Optional[dict[str, Any]] = None) -> None:
    if not actor_user_id:
        return

    row = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        metadata_json=json.dumps(metadata or {}, ensure_ascii=True),
    )
    db.session.add(row)
