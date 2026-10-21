from performance_test import (
    generate_employee_records,
    process_employee_records,
)


def test_empty_employee_list():

    records = process_employee_records([])

    assert records == []


def test_employee_count():

    records = generate_employee_records(100)

    assert len(records) == 100


def test_missing_documents_are_pending():

    records = generate_employee_records(1)

    process_employee_records(records)

    assert records[0]["status"] == "Pending"


def test_all_required_documents_complete():

    records = generate_employee_records(1)

    records[0]["documents"] = [
        "Government ID",
        "Educational Certificate",
        "Photograph",
        "Signed Offer Letter",
    ]

    process_employee_records(records)

    assert records[0]["status"] == "Complete"


def test_multiple_employee_records():

    records = generate_employee_records(500)

    process_employee_records(records)

    assert len(records) == 500

    assert all(
        employee["status"] in ["Complete", "Pending"]
        for employee in records
    )