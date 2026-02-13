"""A simple ping/pong bot for Scatter.

Usage:
    python ping_bot.py

Set your bot token in the SCATTER_TOKEN environment variable,
or replace the token string below.
"""

import os

import scatter

token = os.environ.get("SCATTER_TOKEN", "scatter_bot_YOUR_TOKEN_HERE")
client = scatter.Client(token)


@client.event
async def on_ready(data):
    """Called when the bot successfully authenticates via WebSocket.

    The client automatically subscribes to all spaces and text channels,
    so there's no need to do it manually here.
    """
    print(f"Bot is ready! User ID: {client.user_id}")


@client.event
async def on_message(message: scatter.Message):
    """Called when a new message is received in a subscribed channel."""
    # Ignore our own messages
    if message.author.id == client.user_id:
        return

    if message.content == "!ping":
        await client.send_message(
            message.space_id, message.channel_id, "Pong!"
        )

    elif message.content == "!hello":
        await client.send_message(
            message.space_id,
            message.channel_id,
            f"Hello, {message.author.display_name}!",
        )


@client.event
async def on_member_join(user: scatter.User):
    """Called when someone joins a space the bot is subscribed to."""
    print(f"Member joined: {user.display_name}")


client.run()
