from sqlmodel import Session

from app.models.prize import Prize


class PrizeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, prize: Prize) -> Prize:
        try:
            self.db.add(prize)
            self.db.commit()
            self.db.refresh(prize)
            return prize
        except Exception:
            self.db.rollback()
            raise
