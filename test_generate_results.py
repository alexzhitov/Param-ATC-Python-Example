import json
import os

import allure
from datetime import datetime
import pytest
from allure import attachment_type
from allure_commons.types import Severity
from pathlib import Path

RESULTS_DIR = "allure-results"
os.makedirs(RESULTS_DIR, exist_ok=True)

RESOURCES = Path(__file__).parent / "resources"

ATTACHMENTS_PER_TEST = int(os.getenv("LOAD_ATTACHMENTS_PER_TEST", "75"))
TEST_COUNT = int(os.getenv("LOAD_TEST_COUNT", "500"))

@pytest.mark.parametrize("case_number", range(TEST_COUNT))
def test_customer_like_result(case_number):
    allure.dynamic.feature("Customer load test")
    allure.dynamic.story("500 results with 75 attachments")
    allure.dynamic.title(f"Customer synthetic test #{case_number:04d}")

    for attachment_number in range(ATTACHMENTS_PER_TEST):
        if attachment_number % 2 == 0:
            allure.attach.file(
                RESOURCES / "image.png",
                name=f"screenshot-{attachment_number:03d}",
                attachment_type=attachment_type.JPG,
            )
        else:
            allure.attach.file(
                RESOURCES / "chekhov.txt",
                name=f"log-{attachment_number:03d}",
                attachment_type=attachment_type.TEXT,
            )

    assert True











