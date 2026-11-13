import pytest

from routers import moderation as moderation_router

REQUIRED_FIELDS = [
    "seller_id",
    "is_verified_seller",
    "item_id",
    "name",
    "description",
    "category",
    "images_qty",
]


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


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
def test_predict_success(client, valid_ad, is_verified_seller, images_qty, expected):
    valid_ad["is_verified_seller"] = is_verified_seller
    valid_ad["images_qty"] = images_qty

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 200
    assert response.json() is expected


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_predict_missing_field(client, valid_ad, field):
    del valid_ad[field]

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 400
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["type"] == "missing"
    assert errors[0]["loc"] == ["body", field]


@pytest.mark.parametrize(
    "field, value",
    [
        ("seller_id", "1"),
        ("item_id", "abc"),
        ("category", "3"),
        ("images_qty", "2"),
        ("images_qty", 1.5),
        ("is_verified_seller", "true"),
        ("is_verified_seller", 1),
        ("is_verified_seller", 0),
        ("name", {"title": "Велосипед"}),
        ("name", ["Велосипед"]),
        ("description", {"text": "Описание"}),
        ("description", ["Описание"]),
        ("name", 123),
    ],
)
def test_predict_wrong_type(client, valid_ad, field, value):
    valid_ad[field] = value

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 400
    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["body", field]


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_predict_null_value(client, valid_ad, field):
    valid_ad[field] = None

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 400
    assert response.json()["detail"][0]["loc"] == ["body", field]


@pytest.mark.parametrize(
    "field, value, error_type",
    [
        ("images_qty", -1, "greater_than_equal"),
        ("seller_id", 0, "greater_than"),
        ("item_id", -5, "greater_than"),
        ("name", "", "string_too_short"),
    ],
)
def test_predict_invalid_value(client, valid_ad, field, value, error_type):
    valid_ad[field] = value

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 400
    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["body", field]
    assert errors[0]["type"] == error_type


def test_predict_invalid_json(client):
    response = client.post(
        "/predict",
        content="{not a json}",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400


def test_predict_service_error(client, valid_ad, monkeypatch):
    def broken_predict(ad):
        raise RuntimeError("secret internal details")

    monkeypatch.setattr(moderation_router.service, "predict", broken_predict)

    response = client.post("/predict", json=valid_ad)

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert "secret internal details" not in response.text