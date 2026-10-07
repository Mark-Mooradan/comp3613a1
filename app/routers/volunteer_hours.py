from datetime import date

from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.volunteer_entry_repository import VolunteerEntryRepository
from app.services.volunteer_hours import VolunteerHoursService
from app.utilities.flash import flash
from app.dependencies.auth import AdminDep
from . import router, templates


@router.get("/volunteer-hours", response_class=HTMLResponse, name="volunteer_hours_form")
async def volunteer_hours_form(request: Request, user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="log-hours.html",
        context={"user": user},
    )


@router.post("/volunteer-hours")
async def submit_volunteer_hours(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    activity_name: str = Form(),
    organization: str = Form(),
    hours: float = Form(),
    entry_date: date = Form(alias="date"),
):
    service = VolunteerHoursService(VolunteerEntryRepository(db))
    service.submit_entry(
        student_id=user.id,
        activity_name=activity_name,
        organization=organization,
        hours=hours,
        entry_date=entry_date,
    )

    flash(request, "Entry submitted pending approval.")
    return RedirectResponse(url=request.url_for("volunteer_hours_form"), status_code=303)


@router.post("/admin/volunteer-hours/{entry_id}/review", name="review_volunteer_entry")
async def review_volunteer_entry(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    entry_id: int,
    action: str = Form(),
):
    service = VolunteerHoursService(VolunteerEntryRepository(db))
    entry = service.review_entry(entry_id=entry_id, action=action)

    flash(request, f"Entry {entry.id} {entry.status.value.lower()}.")
    return RedirectResponse(url=request.url_for("admin_review_hours"), status_code=303)