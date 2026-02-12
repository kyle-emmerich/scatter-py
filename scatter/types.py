"""Enums and type aliases for the Scatter API."""

try:
    from enum import StrEnum
except ImportError:
    # Python < 3.11 fallback
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class PresenceStatus(StrEnum):
    ONLINE = "online"
    IDLE = "idle"
    DND = "dnd"
    OFFLINE = "offline"
    INVISIBLE = "invisible"


class ChannelType(StrEnum):
    TEXT = "text"
    VOICE = "voice"


class Permission(StrEnum):
    SEND_MESSAGES = "send_messages"
    ATTACH_FILES = "attach_files"
    EMBED_LINKS = "embed_links"
    MANAGE_MESSAGES = "manage_messages"
    MANAGE_CHANNELS = "manage_channels"
    KICK_MEMBERS = "kick_members"
    MANAGE_ROLES = "manage_roles"
    MANAGE_SPACE = "manage_space"
    MENTION_EVERYONE = "mention_everyone"
    PIN_MESSAGES = "pin_messages"
    CREATE_INVITES = "create_invites"
    MANAGE_INVITES = "manage_invites"
