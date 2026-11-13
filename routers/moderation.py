from fastapi import APIRouter

from repositories.moderation import ModerationRepository
from schemas.advertisement import Advertisement
from services.moderation import ModerationService

router = APIRouter()

service = ModerationService(ModerationRepository())


@router.post(
    "/predict",
    responses={
        200: {"description": "true - нарушение найдено, false - нарушения нет"},
        400: {"description": "Некорректные входные данные"},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
def predict(ad: Advertisement) -> bool:
    return service.predict(ad)