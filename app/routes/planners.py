import json
import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..deps import get_current_user_optional
from ..models import Recommendation, User
from ..schemas import (
    HomePlannerRequest,
    JewelryPlannerRequest,
    PartyPlannerRequest,
)
from ..services.recommendation_service import (
    generate_home_recommendation,
    generate_jewelry_recommendation,
    generate_party_recommendation,
)


router = APIRouter(
    tags=["AI Planners"],
)


def save_recommendation(
    db: Session,
    user: User | None,
    planner_type: str,
    title: str,
    input_data: dict,
    result: dict,
) -> Recommendation:

    recommendation = Recommendation(
        user_id=user.id if user else None,
        planner_type=planner_type,
        title=title,
        input_json=json.dumps(input_data),
        result_json=json.dumps(result),
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.post("/generate-home")
def generate_home(
    data: HomePlannerRequest,
    db: Session = Depends(get_db),
    user: User | None = Depends(
        get_current_user_optional
    ),
):
    result = generate_home_recommendation(
        data.model_dump()
    )

    saved = save_recommendation(
        db=db,
        user=user,
        planner_type="home",
        title="Home Planner",
        input_data=data.model_dump(),
        result=result,
    )

    result["recommendation_id"] = saved.id

    return result


@router.post("/generate-party")
def generate_party(
    data: PartyPlannerRequest,
    db: Session = Depends(get_db),
    user: User | None = Depends(
        get_current_user_optional
    ),
):
    result = generate_party_recommendation(
        data.model_dump()
    )

    saved = save_recommendation(
        db=db,
        user=user,
        planner_type="party",
        title="Party Planner",
        input_data=data.model_dump(),
        result=result,
    )

    result["recommendation_id"] = saved.id

    return result


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form("Casual"),
    jewelry_type: str = Form("Necklace"),
    metal: str = Form("Any"),
    style: str = Form("Minimal"),
    outfit_color: str = Form("Any"),
    image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    user: User | None = Depends(
        get_current_user_optional
    ),
):
    image_path = None

    if image is not None:
        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG and WEBP images are allowed.",
            )

        max_size = (
            settings.max_upload_size_mb
            * 1024
            * 1024
        )

        content = await image.read()

        if len(content) > max_size:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is too large.",
            )

        extension = os.path.splitext(
            image.filename or ""
        )[1].lower()

        if extension not in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }:
            extension = ".jpg"

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        image_path = os.path.join(
            settings.upload_dir,
            filename,
        )

        with open(image_path, "wb") as file:
            file.write(content)

    data = {
        "budget": budget,
        "occasion": occasion,
        "jewelry_type": jewelry_type,
        "metal": metal,
        "style": style,
        "outfit_color": outfit_color,
        "image_path": image_path,
    }

    result = generate_jewelry_recommendation(
        data
    )

    saved = save_recommendation(
        db=db,
        user=user,
        planner_type="jewelry",
        title="Jewelry Planner",
        input_data=data,
        result=result,
    )

    result["recommendation_id"] = saved.id

    return result