"""Event context objects that wrap models with convenience methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client, Typing
    from .models import Message, User


class MessageContext:
    """Context for message events, providing shortcuts to common actions.

    Attributes:
        message: The underlying :class:`Message` object.
        client: The :class:`Client` instance.

    Example::

        @client.event
        async def on_message(ctx: scatter.MessageContext):
            if ctx.content == "!ping":
                await ctx.send("Pong!")
    """

    __slots__ = ("message", "client")

    def __init__(self, client: Client, message: Message):
        self.client = client
        self.message = message

    # ── Shortcuts to Message fields ────────────────────────────

    @property
    def author(self) -> User:
        return self.message.author

    @property
    def content(self) -> str:
        return self.message.content

    @property
    def channel_id(self) -> str:
        return self.message.channel_id

    @property
    def space_id(self) -> str | None:
        return self.message.space_id

    @property
    def message_id(self) -> str:
        return self.message.id

    # ── Convenience actions ────────────────────────────────────

    async def send(self, content: str) -> Message:
        """Send a message to the same channel."""
        return await self.client.send_message(
            self.message.space_id, self.message.channel_id, content
        )

    async def reply(self, content: str) -> Message:
        """Reply to this message."""
        return await self.client.send_message(
            self.message.space_id,
            self.message.channel_id,
            content,
            reply_to=self.message.id,
        )

    async def react(self, emoji: str) -> None:
        """Add a reaction to this message."""
        await self.client.add_reaction(
            self.message.space_id,
            self.message.channel_id,
            self.message.id,
            emoji,
        )

    async def delete(self) -> None:
        """Delete this message."""
        await self.client.delete_message(
            self.message.space_id,
            self.message.channel_id,
            self.message.id,
        )

    def typing(self) -> Typing:
        """Return a typing indicator context manager for this channel.

        Usage::

            async with ctx.typing():
                result = await slow_operation()
                await ctx.send(result)
        """
        return self.client.typing(self.message.channel_id)
