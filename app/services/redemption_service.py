from app.models.prize import Prize
from app.repositories.redemption_repository import RedemptionRepository


class RedemptionService:
    def __init__(self, redemption_repository: RedemptionRepository):
        self.redemption_repository = redemption_repository

    def get_rewards(self, student_id: int) -> tuple[float, list[Prize]]:
        balance = self.redemption_repository.get_balance(student_id)
        prizes = self.redemption_repository.list_prizes()
        return balance, prizes

    def redeem_prize(self, *, student_id: int, prize_id: int) -> Prize:
        prize = self.redemption_repository.get_prize(prize_id)
        if prize is None:
            raise ValueError("This prize is no longer available.")
        if prize.quantity_available <= 0:
            raise ValueError("This prize is out of stock.")

        balance = self.redemption_repository.get_balance(student_id)
        if balance < prize.cost_in_hours:
            raise ValueError(
                f"You need {prize.cost_in_hours:g} approved hours to redeem this prize."
            )

        inventory_updated = self.redemption_repository.create_redemption_and_decrement_inventory(
            student_id=student_id,
            prize_id=prize_id,
        )
        if not inventory_updated:
            raise ValueError("This prize is out of stock.")
        return prize
