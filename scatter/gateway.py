"""WebSocket gateway connection manager."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Callable

import aiohttp

from .errors import AuthenticationError, GatewayError

log = logging.getLogger(__name__)

DEFAULT_WS_URL = "wss://scatter.starforge.games/ws"


class Gateway:
    """Manages the WebSocket connection to Scatter, with auto-reconnection."""

    def __init__(
        self,
        token: str,
        dispatch: Callable,
        *,
        ws_url: str = DEFAULT_WS_URL,
    ):
        self._token = token
        self._dispatch = dispatch  # async callback(event_type, data)
        self._ws_url = ws_url
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._session: aiohttp.ClientSession | None = None
        self._closed = False
        self._reconnect_delay = 1.0
        self._max_reconnect_delay = 60.0
        self._subscribed_channels: set[str] = set()
        self._subscribed_spaces: set[str] = set()

    async def connect(self):
        """Connect and enter the receive loop. Reconnects automatically on failure."""
        while not self._closed:
            try:
                await self._do_connect()
                self._reconnect_delay = 1.0  # reset on success
                await self._receive_loop()
            except (
                aiohttp.WSServerHandshakeError,
                aiohttp.ClientError,
                ConnectionError,
                OSError,
            ) as exc:
                if self._closed:
                    break
                log.warning(
                    "Gateway disconnected: %s. Reconnecting in %.1fs...",
                    exc,
                    self._reconnect_delay,
                )
                await asyncio.sleep(self._reconnect_delay)
                self._reconnect_delay = min(
                    self._reconnect_delay * 2, self._max_reconnect_delay
                )

    async def _do_connect(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        self._ws = await self._session.ws_connect(self._ws_url)
        # Authenticate immediately
        await self.send({"type": "auth", "token": self._token})

    async def _receive_loop(self):
        assert self._ws is not None
        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                event_type = data.get("type")

                if event_type == "auth_ok":
                    log.info("Authenticated as user %s", data.get("user_id"))
                    # Re-subscribe to everything we were tracking
                    for ch_id in self._subscribed_channels:
                        await self.send(
                            {"type": "subscribe", "channel_id": ch_id}
                        )
                    for sp_id in self._subscribed_spaces:
                        await self.send(
                            {"type": "subscribe_space", "space_id": sp_id}
                        )
                    await self._dispatch("auth_ok", data)

                elif event_type == "error":
                    error_msg = data.get("message", "Unknown error")
                    log.error("Gateway error: %s", error_msg)
                    if "auth" in error_msg.lower() or "token" in error_msg.lower():
                        raise AuthenticationError(error_msg)
                    await self._dispatch("error", data)

                else:
                    await self._dispatch(event_type, data)

            elif msg.type in (
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.ERROR,
            ):
                break

    async def send(self, data: dict):
        """Send a JSON message over the WebSocket."""
        if self._ws and not self._ws.closed:
            await self._ws.send_json(data)

    def track_channel(self, channel_id: str):
        """Track a channel subscription for auto-resubscribe on reconnect."""
        self._subscribed_channels.add(channel_id)

    def untrack_channel(self, channel_id: str):
        self._subscribed_channels.discard(channel_id)

    def track_space(self, space_id: str):
        """Track a space subscription for auto-resubscribe on reconnect."""
        self._subscribed_spaces.add(space_id)

    def untrack_space(self, space_id: str):
        self._subscribed_spaces.discard(space_id)

    async def close(self):
        """Gracefully close the WebSocket connection."""
        self._closed = True
        if self._ws and not self._ws.closed:
            await self._ws.close()
        if self._session and not self._session.closed:
            await self._session.close()
