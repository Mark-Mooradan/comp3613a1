from sqlmodel import Session, select

from app.models.volunteer_entry import VolunteerEntry, VolunteerEntryStatus
from app.models.user import User


class VolunteerEntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, entry: VolunteerEntry) -> VolunteerEntry:
        """Persist and return one volunteer-hours entry."""
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_pending_with_students(self) -> list[tuple[VolunteerEntry, User]]:
        statement = (
            select(VolunteerEntry, User)
            .join(User, VolunteerEntry.student_id == User.id)
            .where(VolunteerEntry.status == VolunteerEntryStatus.PENDING)
            .order_by(VolunteerEntry.date, VolunteerEntry.id)
        )
        return list(self.db.exec(statement).all())

    def update_status(
        self,
        entry_id: int,
        status: VolunteerEntryStatus,
    ) -> VolunteerEntry | None:
        entry = self.db.get(VolunteerEntry, entry_id)
        if entry is None or entry.status != VolunteerEntryStatus.PENDING:
            return None

        try:
            entry.status = status
            self.db.add(entry)
            self.db.commit()
            self.db.refresh(entry)
            return entry
        except Exception:
            self.db.rollback()
            raise