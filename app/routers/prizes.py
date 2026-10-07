from fastapi import Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AdminDep
from app.dependencies.session import SessionDep
from app.repositories.prize_repository import PrizeRepository
from app.services.prize_service import PrizeService
from app.utilities.flash import flash
from . import router, templates


@router.get(
    "/admin/prizes/new",
    response_class=HTMLResponse,
    name="admin_create_prize_form",
)
async def admin_create_prize_form(request: Request, user: AdminDep):
    return templates.TemplateResponse(
        request=request,
        name="create-prize.html",
        context={"user": user},
    )


@router.post("/admin/prizes/new", name="create_prize")
async def create_prize(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(),
    description: str = Form(),
    cost_in_hours: float = Form(),
    quantity_available: int = Form(),
):
    service = PrizeService(PrizeRepository(db))
    service.create_prize(
        name=name,
        description=description,
        cost_in_hours=cost_in_hours,
        quantity_available=quantity_available,
    )

    flash(request, f"Prize '{name}' created.")
    return RedirectResponse(url=request.url_for("admin_create_prize_form"), status_code=303)