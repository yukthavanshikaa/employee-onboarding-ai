import time
import statistics
import psutil
import os
import pandas as pd


# ------------------------------------
# PERFORMANCE TESTING CONFIGURATION
# ------------------------------------

EMPLOYEE_COUNTS = [10, 100, 500, 1000]


def generate_employee_records(count):
    """Generate synthetic employee records for testing."""

    departments = [
        "Engineering",
        "Human Resources",
        "Finance",
        "Sales",
        "Operations",
    ]

    records = []

    for i in range(count):
        records.append({
            "employee_id": f"EMP-{i + 1:06d}",
            "name": f"Employee {i + 1}",
            "email": f"employee{i + 1}@example.com",
            "department": departments[i % len(departments)],
            "documents": [
                "Government ID",
                "Educational Certificate",
            ],
            "training_completed": [],
            "status": "Pending",
        })

    return records


def process_employee_records(records):
    """Simulate lightweight onboarding checks."""

    for employee in records:

        documents_complete = (
            "Government ID" in employee["documents"]
            and "Educational Certificate" in employee["documents"]
            and "Photograph" in employee["documents"]
            and "Signed Offer Letter" in employee["documents"]
        )

        employee["status"] = (
            "Complete"
            if documents_complete
            else "Pending"
        )

    return records


def run_performance_test(count):

    process = psutil.Process(os.getpid())

    records = generate_employee_records(count)

    memory_before = (
        process.memory_info().rss / (1024 * 1024)
    )

    start_time = time.perf_counter()

    process_employee_records(records)

    end_time = time.perf_counter()

    memory_after = (
        process.memory_info().rss / (1024 * 1024)
    )

    elapsed = end_time - start_time

    return {
        "Employee Count": count,
        "Execution Time (seconds)": round(elapsed, 6),
        "Average Time per Employee (ms)": round(
            elapsed / count * 1000, 6
        ),
        "Memory Before (MB)": round(memory_before, 2),
        "Memory After (MB)": round(memory_after, 2),
        "Memory Difference (MB)": round(
            memory_after - memory_before, 2
        ),
    }


def main():

    results = []

    print("\nHR ONBOARDING SYSTEM PERFORMANCE TEST")
    print("=" * 65)

    for count in EMPLOYEE_COUNTS:

        result = run_performance_test(count)

        results.append(result)

        print(f"\nEmployee Count: {count}")
        print(
            "Execution Time:",
            result["Execution Time (seconds)"],
            "seconds"
        )
        print(
            "Average Time per Employee:",
            result["Average Time per Employee (ms)"],
            "ms"
        )
        print(
            "Memory Difference:",
            result["Memory Difference (MB)"],
            "MB"
        )

    dataframe = pd.DataFrame(results)

    dataframe.to_csv(
        "performance_results.csv",
        index=False
    )

    print("\n" + "=" * 65)
    print("PERFORMANCE TEST COMPLETED")
    print("Results saved to performance_results.csv")


if __name__ == "__main__":
    main()