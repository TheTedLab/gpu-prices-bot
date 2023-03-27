import os
import asyncio
import pytest
import pytest_asyncio
from src.bot.constants import shops_logo_dir
from telethon import TelegramClient
from telethon.sessions import StringSession


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def client():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    session_str = os.getenv('SESSION_STRING')
    telegram_client: TelegramClient = TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )
    # Connect to the server
    await telegram_client.connect()
    # Issue a high level command to start receiving message
    await telegram_client.get_me()
    # Fill the entity cache
    await telegram_client.get_dialogs()

    yield telegram_client

    await telegram_client.disconnect()
    await telegram_client.disconnected


@pytest.fixture(autouse=True)
def mocked_update_context(mocker):
    mocked_update = mocker.Mock()
    mocked_context = mocker.Mock()
    mock_context_dict = {}
    mocked_context.user_data.__setitem__ = mocker.Mock()
    mocked_context.user_data.__getitem__ = mocker.Mock()
    mocked_context.user_data.__setitem__.side_effect = mock_context_dict.__setitem__
    mocked_context.user_data.__getitem__.side_effect = mock_context_dict.__getitem__
    return mocked_update, mocked_context


@pytest.fixture()
def shops_logo_path(tmp_path_factory):
    image_path = tmp_path_factory.mktemp('test_images') / "shops_logo.jpg"
    with open(shops_logo_dir, 'rb') as image:
        image_string = image.read()
        with open(image_path, 'wb') as dest_image:
            dest_image.write(image_string)

    return image_path

@pytest.fixture()
def graph_data():

    return {
        "MVIDEO": {
            "1": {
                "cardName": "Product A"
            },
            "2": {
                "cardName": "Product B"
            },
            "3": None
        },
        "CITILINK": {
            "1": None,
            "2": {
                "cardName": "Product C"
            },
            "3": {
                "cardName": "Product D"
            }
        }
    }


@pytest.fixture()
def vendor():
    return "Vendor A"


@pytest.fixture()
def graph_offers_vendors_data():
    return {
            "PALIT": {
                "2022-12-06": {
                    "GEFORCE PALIT RTX 3090 GAMINGPRO 24G": 109999,
                    "GEFORCE RTX 3070 TI GAMEROCK 8GB": 52499
                },
                "2022-12-12": {
                    "GEFORCE RTX 4080 GAMEROCK OC 16GB": 108499,
                    "GEFORCE RTX 4090 GAMEROCK 24GB": 174999,
                }
            },
            "ASUS": {
                "2022-12-05": {
                    "RADEON RX 6650 XT DUAL-RX6650XT-O8G OC": 34190,
                    "GEFORCE RTX 3060 PH-RTX3060-12G-V2": 35990
                },
                "2022-12-19": {
                    "GEFORCE RTX 3060 TI DUAL-RTX3060TI-O8G-V2 OC": 47690,
                    "RADEON RX 6400 DUAL-RX6400-4G": 15790
                }
            }
        }
