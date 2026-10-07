from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep, IsUserLoggedIn, get_current_user, is_admin
from app.repositories.volunteer_entry_repository import VolunteerEntryRepository
from app.services.volunteer_hours import VolunteerHoursService
from . import router, templates


@router.get("/admin", response_class=HTMLResponse)
async def admin_home_view(
    request: Request,
    user: AdminDep,
    db:SessionDep
):
    service = VolunteerHoursService(VolunteerEntryRepository(db))
    return templates.TemplateResponse(
        request=request, 
        name="admin.html",
        context={
            "user": user,
            "pending_entries": service.get_pending_entries(),
        }
    )


@router.get(
    "/admin/volunteer-hours",
    response_class=HTMLResponse,
    name="admin_review_hours",
)
async def admin_review_hours(
    request: Request,
    user: AdminDep,
    db: SessionDep,
):
    service = VolunteerHoursService(VolunteerEntryRepository(db))
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "user": user,
            "pending_entries": service.get_pending_entries(),
        },
    )
