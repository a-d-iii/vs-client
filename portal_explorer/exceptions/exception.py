import httpx


class PortalExplorerError(Exception):
    """Base exception for all portal-related errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class VtopConnectionError(PortalExplorerError):
    """Raised for network-related errors during VTOP communication."""

    def __init__(
        self,
        message: str,
        original_exception: httpx.RequestError | None = None,
        status_code: int | None = None,
    ):
        super().__init__(message, status_code)
        self.original_exception = original_exception


class VtopLoginError(PortalExplorerError):
    """Raised when login fails due to invalid credentials, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopAttendanceError(PortalExplorerError):
    """Raised when fetching attendance fails due to attendance parsing, invalid semSubId, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopTimetableError(PortalExplorerError):
    """Raised when fetching timetable fails due to data parsing, invalid semSubId, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopGradeHistoryError(PortalExplorerError):
    """Raised when fetching greades history fails due to data parsing, invalid semester id, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopMentorError(PortalExplorerError):
    """Raised when fetching biometric fails due to data parsing, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopBiometricError(PortalExplorerError):
    """Raised when fetching biometric fails due to data parsing, invalid date, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopProfileError(PortalExplorerError):
    """Raised when fetching biometric fails due to data parsing, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopExamScheduleError(PortalExplorerError):
    """Raised when fetching exam schedule fails due to data parsing, invalid semester id, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopMarksError(PortalExplorerError):
    """Raised when fetching marks fails due to data parsing, invalid semester id, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopGeneralOutingError(PortalExplorerError):
    """Raised when fetching/posting marks fails due to data parsing, invalid semester id, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopWeekendOutingError(PortalExplorerError):
    """Raised when fetching/posting marks fails due to data parsing, invalid semester id, server-side validation, etc."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopCaptchaError(VtopLoginError):
    """Raised for errors specifically related to CAPTCHA fetching or solving."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopCsrfError(VtopLoginError):
    """Raised for errors specifically related to CSRF scraping and fetching."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopParsingError(PortalExplorerError):
    """Raised when data parsing fails unexpectedly (e.g., new HTML format)."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)


class VtopSessionError(PortalExplorerError):
    """Raised when an operation requires an active session but one is not available or valid."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message, status_code)
