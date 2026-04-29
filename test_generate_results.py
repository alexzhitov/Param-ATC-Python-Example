import base64
import os

import allure
import pytest
from allure import attachment_type

RESULTS_DIR = "allure-results"
os.makedirs(RESULTS_DIR, exist_ok=True)

TEST_COUNT = int(os.getenv("LOAD_TEST_COUNT", "2000"))
TEST_CATALOG_SIZE = int(os.getenv("LOAD_TEST_CATALOG_SIZE", "35000"))
ATTACHMENTS_MIN = int(os.getenv("LOAD_ATTACHMENTS_MIN", "50"))
ATTACHMENTS_MAX = int(os.getenv("LOAD_ATTACHMENTS_MAX", "100"))
IMAGE_ATTACHMENT_SIZE_BYTES = int(os.getenv("LOAD_IMAGE_ATTACHMENT_SIZE_BYTES", "262144"))
TEXT_ATTACHMENT_SIZE_BYTES = int(os.getenv("LOAD_TEXT_ATTACHMENT_SIZE_BYTES", "4096"))
IMAGE_ATTACHMENT_PERCENT = int(os.getenv("LOAD_IMAGE_ATTACHMENT_PERCENT", "70"))
FAILED_RESULTS_PERCENT = int(os.getenv("LOAD_FAILED_RESULTS_PERCENT", "0"))
TEST_ID_OFFSET = int(os.getenv("LOAD_TEST_ID_OFFSET", "0"))

TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def sized_payload(prefix: bytes, target_size: int) -> bytes:
    if target_size <= len(prefix):
        return prefix[:target_size]

    return prefix + (b"0" * (target_size - len(prefix)))


IMAGE_PAYLOAD = sized_payload(TINY_PNG, IMAGE_ATTACHMENT_SIZE_BYTES)
TEXT_PAYLOAD = sized_payload(
    b"Customer-like synthetic log line. upload pipeline payload.\n",
    TEXT_ATTACHMENT_SIZE_BYTES,
).decode("ascii")


def attachment_count_for(case_number: int) -> int:
    if ATTACHMENTS_MAX <= ATTACHMENTS_MIN:
        return ATTACHMENTS_MIN

    span = ATTACHMENTS_MAX - ATTACHMENTS_MIN + 1
    return ATTACHMENTS_MIN + (case_number % span)


def is_image_attachment(case_number: int, attachment_number: int) -> bool:
    return ((case_number * 31 + attachment_number * 17) % 100) < IMAGE_ATTACHMENT_PERCENT


def should_fail(case_number: int) -> bool:
    return FAILED_RESULTS_PERCENT > 0 and (case_number % 100) < FAILED_RESULTS_PERCENT


@pytest.mark.parametrize("result_number", range(TEST_COUNT))
def test_customer_like_result(result_number):
    test_id = (TEST_ID_OFFSET + result_number) % TEST_CATALOG_SIZE
    attachment_count = attachment_count_for(result_number)

    allure.dynamic.feature("Customer load test")
    allure.dynamic.story(
        f"{TEST_COUNT} results from {TEST_CATALOG_SIZE} automated tests, "
        f"{ATTACHMENTS_MIN}-{ATTACHMENTS_MAX} attachments/result"
    )
    allure.dynamic.title(f"Customer synthetic test #{test_id:05d} result #{result_number:05d}")
    allure.dynamic.parameter("synthetic_test_id", f"TC-{test_id:05d}")
    allure.dynamic.parameter("attachment_count", attachment_count)

    for attachment_number in range(attachment_count):
        if is_image_attachment(result_number, attachment_number):
            allure.attach(
                IMAGE_PAYLOAD,
                name=f"screenshot-{attachment_number:03d}.png",
                attachment_type=attachment_type.PNG,
            )
        else:
            allure.attach(
                TEXT_PAYLOAD,
                name=f"log-{attachment_number:03d}.txt",
                attachment_type=attachment_type.TEXT,
            )

    assert not should_fail(result_number)
