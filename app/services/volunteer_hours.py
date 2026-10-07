from datetime import date

from app.models.volunteer_entry import VolunteerEntry, VolunteerEntryStatus
from app.models.user import User
from app.repositories.volunteer_entry_repository import VolunteerEntryRepository


class VolunteerHoursService:
    def __init__(self, volunteer_entry_repository: VolunteerEntryRepository):
        self.volunteer_entry_repository = volunteer_entry_repository

    def submit_entry(
        self,
        *,
        student_id: int,
        activity_name: str,
        organization: str,
        hours: float,
        entry_date: date,
    ) -> VolunteerEntry:
        """Create and persist a student's volunteer-hours submission."""
        entry = VolunteerEntry(
            student_id=student_id,
            activity_name=activity_name,
            organization=organization,
            hours=hours,
            date=entry_date,
            status=VolunteerEntryStatus.PENDING,
        )
        return self.volunteer_entry_repository.create(entry)

    def get_pending_entries(self) -> list[tuple[VolunteerEntry, User]]:
        return self.volunteer_entry_repository.get_pending_with_students()

    def review_entry(self, *, entry_id: int, action: str) -> VolunteerEntry:
        decisions = {
            "approve": VolunteerEntryStatus.APPROVED,
            "reject": VolunteerEntryStatus.REJECTED,
        }
        status = decisions.get(action.strip().lower())
        if status is None:
            raise ValueError("Action must be approve or reject")

        result = self.volunteer_entry_repository.update_status(entry_id, status)
        if result is None:
            raise ValueError(f"Entry {entry_id} not found or already decided")
        return result