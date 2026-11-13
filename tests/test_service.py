from unittest.mock import Mock

import pytest

from repositories.moderation import ModerationRepository
from schemas.advertisement import Advertisement
from services.moderation import ModerationService


def make_ad(is_verified_seller: bool, images_qty: int) -> Advertisement:
    return Advertisement(
        seller_id=1,
        is_verified_seller=is_verified_seller,
        item_id=100,
        name="Велосипед",
        description="Горный велосипед",
        category=3,
        images_qty=images_qty,
    )


@pytest.mark.parametrize(
    "is_verified_seller, images_qty, expected",
    [
        (True, 0, False),
        (True, 1, False),
        (True, 5, False),
        (False, 0, True),
        (False, 1, False),
        (False, 5, False),
    ],
)
def test_predict(is_verified_seller, images_qty, expected):
    service = ModerationService(ModerationRepository())

    result = service.predict(make_ad(is_verified_seller, images_qty))

    assert result is expected


def test_predict_raises_when_repository_fails():
    repository = Mock()
    repository.get_min_images_for_unverified_seller.side_effect = RuntimeError("storage is unavailable")
    service = ModerationService(repository)

    with pytest.raises(RuntimeError, match="storage is unavailable"):
        service.predict(make_ad(is_verified_seller=False, images_qty=0))