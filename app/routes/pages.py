from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Pages"],
)


templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request},
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request},
    )


@router.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(request: Request):
    return templates.TemplateResponse(
        "history.html",
        {"request": request},
    )


@router.get(
    "/planner/home",
    response_class=HTMLResponse,
)
def home_planner_page(request: Request):
    return templates.TemplateResponse(
        "home_planner.html",
        {"request": request},
    )


@router.get(
    "/planner/party",
    response_class=HTMLResponse,
)
def party_planner_page(request: Request):
    return templates.TemplateResponse(
        "party_planner.html",
        {"request": request},
    )


@router.get(
    "/planner/jewelry",
    response_class=HTMLResponse,
)
def jewelry_planner_page(request: Request):
    return templates.TemplateResponse(
        "jewelry_planner.html",
        {"request": request},
    )


@router.get(
    "/recommendation/{recommendation_id}",
    response_class=HTMLResponse,
)
def recommendation_page(
    request: Request,
    recommendation_id: int,
):
    return templates.TemplateResponse(
        "recommendation.html",
        {
            "request": request,
            "recommendation_id": recommendation_id,
        },
    )