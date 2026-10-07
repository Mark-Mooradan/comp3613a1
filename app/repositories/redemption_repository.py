from datetime import datetime, timezone

from sqlmodel import Session, func, select, update

from app.models.prize import Prize
from app.models.redemption import Redemption
from app.models.volunteer_entry import VolunteerEntry, VolunteerEntryStatus


class RedemptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_prizes(self) -> list[Prize]:
        statement = select(Prize).order_by(Prize.name)
        return list(self.db.exec(statement).all())

    def get_prize(self, prize_id: int) -> Prize | None:
        return self.db.get(Prize, prize_id)

    def get_balance(self, student_id: int) -> float:
        approved_statement = select(
            func.coalesce(func.sum(VolunteerEntry.hours), 0)
        ).where(
            VolunteerEntry.student_id == student_id,
            VolunteerEntry.status == VolunteerEntryStatus.APPROVED,
        )
        approved_hours = float(self.db.exec(approved_statement).one())

        redeemed_statement = (
            select(func.coalesce(func.sum(Prize.cost_in_hours), 0))
            .join(Redemption, Redemption.prize_id == Prize.id)
            .where(Redemption.student_id == student_id)
        )
        redeemed_hours = float(self.db.exec(redeemed_statement).one())
        return approved_hours - redeemed_hours

    def create_redemption_and_decrement_inventory(
        self,
        *,
        student_id: int,
        prize_id: int,
    ) -> bool:
        """Atomically decrement available inventory and record the redemption."""
        try:
            result = self.db.exec(
                update(Prize)
                .where(Prize.id == prize_id, Prize.quantity_available > 0)
                .values(quantity_available=Prize.quantity_available - 1)
            )
            if result.rowcount != 1:
                self.db.rollback()
                return False

            self.db.add(
                Redemption(
                    student_id=student_id,
                    prize_id=prize_id,
                    redeemed_at=datetime.now(timezone.utc),
                )
            )
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise
