"""scatter.py - A Python library for the Scatter chat platform bot API."""

__version__ = "0.1.0"

from .client import Client, Typing
from .errors import (
    AuthenticationError,
    Forbidden,
    GatewayError,
    HTTPException,
    NotFound,
    ScatterException,
)
from .models import (
    Attachment,
    Channel,
    ChannelCategory,
    CustomEmoji,
    Embed,
    Invite,
    Member,
    MemberRoleInfo,
    Message,
    MessagePreview,
    Reaction,
    Role,
    RolePermission,
    Space,
    User,
)
from .types import ChannelType, Permission, PresenceStatus
