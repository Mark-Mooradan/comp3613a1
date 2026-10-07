from app.models.prize import Prize
from app.repositories.prize_repository import PrizeRepository


class PrizeService:
    def __init__(self, prize_repository: PrizeRepository):
        self.prize_repository = prize_repository

    def create_prize(
        self,
        *,
        name: str,
        description: str,
        cost_in_hours: int,
        quantity_available: int,
    ) -> Prize:
        prize = Prize(
            name=name,
            description=description,
            cost_in_hours=cost_in_hours,
            quantity_available=quantity_available,
        )
        return self.prize_repository.create(prize)
