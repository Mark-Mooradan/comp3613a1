from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.redemption_repository import RedemptionRepository
from app.services.redemption_service import RedemptionService
from app.utilities.flash import flash
from . import router, templates


@router.get("/rewards", response_class=HTMLResponse, name="rewards_list")
async def rewards_list(request: Request, user: AuthDep, db: SessionDep):
    service = RedemptionService(RedemptionRepository(db))
    balance, prizes = service.get_rewards(user.id)
    return templates.TemplateResponse(
        request=request,
        name="rewards.html",
        context={"user": user, "balance": balance, "prizes": prizes},
    )


@router.post("/rewards/{prize_id}/redeem", name="redeem_prize")
async def redeem_prize(request: Request, user: AuthDep, db: SessionDep, prize_id: int):
    service = RedemptionService(RedemptionRepository(db))
    try:
        service.redeem_prize(student_id=user.id, prize_id=prize_id)
    except ValueError as exc:
        flash(request, str(exc))
    else:
        flash(request, "Prize redeemed successfully.")
    return RedirectResponse(url=request.url_for("rewards_list"), status_code=303)