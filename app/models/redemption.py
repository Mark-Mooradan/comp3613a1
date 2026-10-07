from datetime import datetime

from sqlmodel import Field, SQLModel


class Redemption(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    student_id: int = Field(foreign_key="user.id")
    prize_id: int = Field(foreign_key="prize.id")
    redeemed_at: datetime = Field(default_factory=datetime.utcnow)