import conftest
import pytest
from pydantic import ValidationError

from app.config import Settings

GOOD = "x" * 40


@pytest.mark.parametrize("field", ["jwt_secret", "guest_cookie_secret"])
@pytest.mark.parametrize("value", ["doi-gia-tri-nay", "ngan-qua"])
def test_rejects_placeholder_or_short_secrets(field, value):
    kwargs = {"database_url": "postgresql+psycopg://u:p@localhost/db", "jwt_secret": GOOD, "guest_cookie_secret": GOOD}
    with pytest.raises(ValidationError):
        Settings(**{**kwargs, field: value})


def test_refuses_test_db_equal_to_dev_db():
    dev = "postgresql+psycopg://mediflow:mediflow@localhost:5432/mediflow"
    with pytest.raises(RuntimeError):
        conftest.check_test_url(dev, dev)
    assert conftest.check_test_url(dev.replace("/mediflow", "/mediflow_test"), dev).database == "mediflow_test"
