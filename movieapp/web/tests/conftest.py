# https://djangostars.com/blog/django-pytest-testing/

import pytest


@pytest.fixture
def payload_genre():
    return {
        "name": "Action",
    }


@pytest.fixture
def payload_language():
    return {
        "name": "English",
    }


@pytest.fixture
def payload_mpaarating():
    return {
        "type": "PG",
        "label": "Some Violence"
    }


@pytest.fixture
def payload_movie():
    return {
        "id": 11,
        "name": "Marvel's Captain America: Civil War",
        "description": "Marvel’s Captain America: Civil War picks up where - Avengers: Age of Ultron - left off, as Steve Rogers leads the new team of Avengers in their continued efforts to safeguard humanity. After another international incident involving the Avengers results in collateral damage, political pressure mounts to install a system of accountability and a governing body to determine when to enlist the services of the team. The new status quo fractures the Avengers while they try to protect the world from a new and nefarious villain.",
        "imgPath": "assets/images/civilwar.jpg",
        "duration": 148,
        "genre": ["Action", "Adventure"],
        "language": "English",
        "mpaaRating": {
            "type": "PG",
            "label": "Some Violence"
        },
        "userRating": "5"
    }
