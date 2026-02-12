"""Exception hierarchy for scatter.py."""


class ScatterException(Exception):
    """Base exception for all scatter.py errors."""


class HTTPException(ScatterException):
    """Raised when the API returns an error response."""

    def __init__(self, status: int, body: dict):
        self.status = status
        self.body = body
        message = body.get("error", f"HTTP {status}")
        super().__init__(message)


class NotFound(HTTPException):
    """Raised for 404 responses."""


class Forbidden(HTTPException):
    """Raised for 403 responses."""


class GatewayError(ScatterException):
    """Raised for WebSocket-level errors."""


class AuthenticationError(ScatterException):
    """Raised when the bot token is invalid or rejected."""
