from datetime import date as date_type
from enum import Enum

from sqlmodel import Field, SQLModel


class VolunteerEntryStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class VolunteerEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.id")
    activity_name: str
    organization: str
    hours: float
    date: date_type
    status: VolunteerEntryStatus = Field(default=VolunteerEntryStatus.PENDING)