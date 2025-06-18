import os
import asyncio
from vitap_vtop_client.client import VtopClient
from vitap_vtop_client.constants import SemSubID
from vitap_vtop_client.exceptions import (
    VitapVtopClientError,
    VtopLoginError,
    VtopAttendanceError,
)


async def fetch_semester_details(client: VtopClient, sem_name: str, sem_id: str):
    """Fetch attendance, timetable, exam schedule and marks sequentially."""
    results = {}
    for key, func in [
        ("attendance", client.get_attendance),
        ("timetable", client.get_timetable),
        ("exam_schedule", client.get_exam_schedule),
        ("marks", client.get_marks),
    ]:
        try:
            results[key] = await func(sem_sub_id=sem_id)
        except Exception as e:
            results[key] = e
    return sem_name, sem_id, results


async def main():
    username = os.getenv("VTOP_USERNAME", "24BES7016")
    password = os.getenv("VTOP_PASSWORD", "Vitpassword@1")
    timeout = float(os.getenv("VTOP_TIMEOUT", "60"))
    async with VtopClient(username, password, timeout=timeout) as client:
        try:
            profile_task = client.get_profile()
            mentor_task = client.get_mentor()
            grade_history_task = client.get_grade_history()
            profile, mentor, grade_history = await asyncio.gather(
                profile_task, mentor_task, grade_history_task
            )
            print("PROFILE:", profile)
            print("MENTOR:", mentor)
            print("GRADE HISTORY:", grade_history)

            # Auto-detect semesters with attendance data sequentially
            available_sems: list[tuple[str, str]] = []
            for sem_name, sem_id in SemSubID.items():
                try:
                    data = await client.get_attendance(sem_sub_id=sem_id)
                    if data:
                        available_sems.append((sem_name, sem_id))
                        print(f"Found semester with data: {sem_name} -> {sem_id}")
                except (VtopAttendanceError, VitapVtopClientError, Exception):
                    continue

            print("AVAILABLE SEMESTERS:", available_sems)

            for sem_name, sem_id in available_sems:
                _, _, results = await fetch_semester_details(client, sem_name, sem_id)
                print(f"\n--- Data for {sem_name} ({sem_id}) ---")
                for key, value in results.items():
                    label = key.upper()
                    if isinstance(value, Exception):
                        print(f"{label} fetch failed: {value}")
                    else:
                        print(f"{label}: {value}")

            try:
                biometric = await client.get_biometric(date="14/08/2024")
            except Exception as e:
                biometric = e
            try:
                weekend_outings = await client.get_weekend_outing_requests()
            except Exception as e:
                weekend_outings = e
            try:
                general_outings = await client.get_general_outing_requests()
            except Exception as e:
                general_outings = e
            try:
                pending_payments = await client.get_pending_payments()
            except Exception as e:
                pending_payments = e
            try:
                payment_receipts = await client.get_payment_receipts()
            except Exception as e:
                payment_receipts = e

            print("BIOMETRIC:", biometric)
            print("WEEKEND OUTINGS:", weekend_outings)
            print("GENERAL OUTINGS:", general_outings)
            print("PENDING PAYMENTS:", pending_payments)
            print("PAYMENT RECEIPTS:", payment_receipts)

        except VtopLoginError as e:
            print(f"Login failed: {e}")
        except VitapVtopClientError as e:
            print(f"A VTOP client error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
