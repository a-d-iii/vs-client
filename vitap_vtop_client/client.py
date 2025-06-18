from typing import List
import httpx
import asyncio

from .constants import VTOP_BASE_URL

from .exceptions import (
    VtopLoginError,
    VtopCaptchaError,
    VtopConnectionError,
    VtopSessionError,
    VitapVtopClientError,
)

from .login import (
    fetch_csrf_token,
    pre_login,
    fetch_captcha,
    student_login,
    LoggedInStudent,
)

from .utils import solve_captcha

from .attendance import fetch_attendance, AttendanceModel
from .biometric import fetch_biometric, BiometricModel
from .timetable import fetch_timetable, TimetableModel
from .grade_history import fetch_grade_history, GradeHistoryModel
from .mentor import fetch_mentor_info, MentorModel
from .profile import fetch_profile, StudentProfileModel
from .exam_schedule import fetch_exam_schedule, ExamScheduleModel
from .marks import fetch_marks, MarksModel
from .outing import (
    fetch_general_outing_requests,
    fetch_weekend_outing_requests,
    submit_general_outing_request,
    submit_weekend_outing_request,
    WeekendOutingModel,
    GeneralOutingModel,
)
from .payments import (
    fetch_pending_payments,
    fetch_payment_receipts,
    PendingPayment,
    PaymentReceipt,
)


class VtopClient:
    """
    An asynchronous client for interacting with the VIT-AP VTOP portal.
    """

    def __init__(
        self,
        registration_number: str,
        password: str,
        max_login_retries: int = 3,
        captcha_retries: int = 5,
    ):
        """
        Initializes the VtopClient.

        Args:
            uregistration_numbersername: The VTOP registration number.
            password: The VTOP password.
            max_login_retries: Maximum number of overall login attempts.
            captcha_retries: Maximum number of captcha fetch/solve attempts per login.
        """
        if not registration_number or not password:
            raise VtopLoginError(
                "Registration number and password are required for VtopClient.",
                status_code=400,
            )
        # validate_registration_number(registration_number)

        self.username = registration_number.upper()
        self.password = password
        self._client = httpx.AsyncClient(
            timeout=30.0, follow_redirects=True, base_url=VTOP_BASE_URL
        )
        self._logged_in_student: LoggedInStudent | None = None
        self.max_login_retries = max_login_retries
        self.captcha_retries = captcha_retries
        self._login_lock = asyncio.Lock()  # Prevents concurrent login attempts

    async def _perform_login_sequence(self) -> LoggedInStudent:
        """
        Handles the complete login sequence.
        This sequence must be performed everytime when a user needs something.
        """
        for attempt in range(self.max_login_retries):
            print(
                f"VtopClient: Login attempt {attempt + 1}/{self.max_login_retries} for user {self.username[:5]}****"
            )
            try:
                # Step 1: Fetch initial CSRF token
                csrf_token = await fetch_csrf_token(self._client)
                print(
                    f"VtopClient: CSRF TOKEN: {csrf_token[:8]} - **** - **** - ************"
                )

                # Step 2: Pre-login setup
                await pre_login(self._client, csrf_token)

                # Step 3: Fetch and solve CAPTCHA
                captcha_base64 = await fetch_captcha(
                    self._client, retries=self.captcha_retries
                )
                captcha_value = await asyncio.to_thread(solve_captcha, captcha_base64)
                print(f"VtopClient: Solved captcha: {captcha_value}")

                # Step 4: Attempt login
                logged_in_student = await student_login(
                    self._client,
                    csrf_token,
                    self.username,
                    self.password,
                    captcha_value,
                )
                self._logged_in_student = logged_in_student
                print(f"VtopClient: Login successful for {self.username[:5]}****")
                return logged_in_student

            except VtopCaptchaError as e:
                print(f"VtopClient: Captcha error during login: {e}")
                if attempt == self.max_login_retries - 1:
                    raise
                await asyncio.sleep(1)  # Wait a bit before retrying captcha
            except VtopLoginError as e:  # Typically for bad credentials
                print(
                    f"VtopClient: Login failed due to invalid credentials or format: {e}"
                )
                raise  # No point retrying if credentials are bad
            except VtopConnectionError as e:
                raise

            except VtopSessionError as e:
                print(f"Session error (e.g., CSRF/session expired): {e}")
                raise
            except Exception as e:
                print(f"VtopClient: Unexpected error during login: {e}")
                if attempt == self.max_login_retries - 1:
                    raise VitapVtopClientError(
                        f"Login failed after {self.max_login_retries} attempts due to unexpected error: {e}"
                    )
                await asyncio.sleep(attempt + 1)

        # Should not be reached if loop completes without returning/raising
        raise VitapVtopClientError(
            f"Login failed for user {self.username} after {self.max_login_retries} attempts."
        )

    async def _ensure_logged_in(self) -> LoggedInStudent:
        """
        Ensures the client is logged in. If not, performs login.
        This method is idempotent.
        """
        # Check if already logged in and session is potentially valid
        if self._logged_in_student is not None:
            return self._logged_in_student

        async with self._login_lock:
            # Double-check after acquiring the lock, in case another coroutine logged in
            if self._logged_in_student is None:
                print(
                    f"VtopClient: Not logged in or session expired for {self.username[:5]}****. Initiating login."
                )
                await self._perform_login_sequence()

            if (
                self._logged_in_student is None
            ):  # Should be set by _perform_login_sequence on success
                raise VitapVtopClientError(
                    "VtopClient: Failed to establish a login session."
                )
            return self._logged_in_student

    async def get_attendance(self, sem_sub_id: str) -> list[AttendanceModel]:
        """
        Fetches attendance data for the given semester subject ID.

        Args:
            sem_sub_id: The semester subject ID (e.g., "AP2023242").

        Returns:
            A list containing the parsed attendance data(AttendanceModel).
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_attendance(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            semSubID=sem_sub_id,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_biometric(self, date: str) -> list[BiometricModel]:
        """
        Fetches biometric data for the given date.

        Args:
            date: The date for which the biometric log is requested, in 'dd/mm/yyyy' format.

        Returns:
            A list containing the parsed biometric data(AttendanceModel).
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_biometric(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            date=date,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_timetable(self, sem_sub_id: str) -> TimetableModel:
        """
        Fetches timetable data for the given semester.

        Args:
            sem_sub_id: The semester subject ID (e.g., "AP2023242").

        Returns:
            A TimetableModel containing the parsed timetable details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_timetable(
            client=self._client,
            username=logged_in_info.registration_number,
            semSubID=sem_sub_id,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_grade_history(self) -> GradeHistoryModel:
        """
        Fetches grade history for the given registration_number.

        Returns:
            A GradeHistoryModel containing the parsed grade history details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_grade_history(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_mentor(self) -> MentorModel:
        """
        Fetches mentor data for the given registration_number.

        Returns:
            A MentorModel containing the parsed mentor data.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_mentor_info(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_profile(self) -> StudentProfileModel:
        """
        Fetches profile data for the given registration_number.

        Returns:
            A StudentProfileModel containing the parsed student details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_profile(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_exam_schedule(self, sem_sub_id: str) -> ExamScheduleModel:
        """
        Fetches all exam schedules for the given semester.

        Returns:
            A ExamScheduleModel containing the parsed exam schedule details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_exam_schedule(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
            semSubID=sem_sub_id,
        )

    async def get_marks(self, sem_sub_id: str) -> MarksModel:
        """
        Fetches all marks for the given semester.

        Returns:
            A MarksModel containing the parsed mark details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_marks(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
            semSubID=sem_sub_id,
        )

    async def get_weekend_outing_requests(self) -> WeekendOutingModel:
        """
        Fetches all the previously submitted Weekend Outing requests.

        Returns:
            A WeekendOutingModel containing the previously submitted Weekend Outing details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_weekend_outing_requests(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_general_outing_requests(self) -> GeneralOutingModel:
        """
        Fetches all the previously submitted Genneral Outing requests.

        Returns:
            A GeneralOutingModel containing the previously submitted General Outing details.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_general_outing_requests(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_pending_payments(self) -> List[PendingPayment]:
        """
        Fetches a list of pending payments.

        Returns:
            A list of PendingPayment if found or an empty list.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_pending_payments(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def get_payment_receipts(self) -> List[PaymentReceipt]:
        """
        Fetches a list of previously made payment receipts.

        Returns:
            A list of PaymentReceipt if found or an empty list.
        """
        logged_in_info = await self._ensure_logged_in()
        return await fetch_payment_receipts(
            client=self._client,
            registration_number=logged_in_info.registration_number,
            csrf_token=logged_in_info.post_login_csrf_token,
        )

    async def close(self):
        """
        Closes the underlying HTTP client. Should be called when done with the VtopClient.
        """
        await self._client.aclose()

    async def __aenter__(self):
        """Allows using the client with 'async with'."""
        # You could optionally call await self._ensure_logged_in() here
        # if you want to ensure login upon entering the context.
        # However, lazy login (on first actual data request) is often preferred.
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the client when exiting 'async with' block."""
        await self.close()
