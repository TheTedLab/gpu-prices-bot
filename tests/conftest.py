import pytest
from src.bot.constants import shops_logo_dir

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


@pytest.fixture(autouse=True)
def shops_logo_path(tmp_path_factory):
    image_path = tmp_path_factory.mktemp('test_images') / "shops_logo.jpg"
    with open(shops_logo_dir, 'rb') as image:
        image_string = image.read()
        with open(image_path, 'wb') as dest_image:
            dest_image.write(image_string)

    return image_path
