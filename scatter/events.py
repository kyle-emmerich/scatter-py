"""Event type constants and parsing."""

from __future__ import annotations

from .models import (
    Message,
    User,
    Channel,
    ChannelCategory,
    Role,
)

# Maps raw WS event "type" string -> on_<name> handler name.
# e.g. "new_message" dispatches to on_message, "member_joined" to on_member_join.
EVENT_MAP: dict[str, str] = {
    # auth / control
    "auth_ok": "ready",
    "error": "error",
    "subscribed": "subscribed",
    # channel events
    "new_message": "message",
    "message_edited": "message_edit",
    "message_deleted": "message_delete",
    "typing": "typing",
    "embeds_resolved": "embeds_resolved",
    "message_pinned": "message_pinned",
    "message_unpinned": "message_unpinned",
    "reaction_added": "reaction_add",
    "reaction_removed": "reaction_remove",
    # space events
    "member_joined": "member_join",
    "member_left": "member_remove",
    "presence_changed": "presence_update",
    "member_profile_updated": "member_update",
    "channel_created": "channel_create",
    "channel_updated": "channel_update",
    "channel_deleted": "channel_delete",
    "channel_permissions_updated": "channel_permissions_update",
    "role_created": "role_create",
    "role_updated": "role_update",
    "role_deleted": "role_delete",
    "member_roles_updated": "member_roles_update",
    "emoji_created": "emoji_create",
    "emoji_deleted": "emoji_delete",
    "category_created": "category_create",
    "category_updated": "category_update",
    "category_deleted": "category_delete",
    "mention": "mention",
    # voice events
    "voice_participant_joined": "voice_join",
    "voice_participant_left": "voice_leave",
    "voice_state_update": "voice_state_update",
    # DM events
    "dm_new_message": "dm_message",
    "dm_message_edited": "dm_message_edit",
    "dm_message_deleted": "dm_message_delete",
    "dm_typing": "dm_typing",
    "dm_conversation_created": "dm_conversation_create",
}


def parse_event(event_type: str, data: dict):
    """Convert a raw WS event dict into the appropriate model object.

    Returns a parsed model for events we understand,
    or the raw dict for events we don't have a parser for yet.
    """
    if event_type in ("new_message", "dm_new_message"):
        return Message.from_dict(data)

    if event_type in ("message_edited", "dm_message_edited"):
        # Partial update — no full author, just return raw dict
        return data

    if event_type in ("message_deleted", "dm_message_deleted"):
        return data

    if event_type == "member_joined":
        user_data = data.get("user", {})
        return User.from_dict(user_data)

    if event_type in ("channel_created", "channel_updated"):
        ch_data = data.get("channel", data)
        ch_data.setdefault("space_id", data.get("space_id", ""))
        return Channel.from_dict(ch_data)

    if event_type in ("role_created", "role_updated"):
        role_data = data.get("role", data)
        role_data.setdefault("space_id", data.get("space_id", ""))
        return Role.from_dict(role_data)

    if event_type in ("category_created", "category_updated"):
        cat_data = data.get("category", data)
        cat_data.setdefault("space_id", data.get("space_id", ""))
        return ChannelCategory.from_dict(cat_data)

    # Default: return the raw dict as-is
    return data
