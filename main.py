import asyncio
from telethon import TelegramClient, events

# =========================================================
# ⚙️ CREDENTIALS AUTOMATICALLY PLUGGED IN FOR YOU
# =========================================================

API_ID = 34195900  # Your Telegram App api_id
API_HASH = '1b8f2c2a7f8c3580eea7b568b2bdeace'  # Your Telegram App api_hash

# The exact name of your private group
TARGET_GROUP_NAME = 'SolHouse Signal VIP'

# Your specific VIP keywords (set to lowercase for perfect matching)
KEYWORDS = ['💎 diamond', 'high risk signal']

# =========================================================
# 🛑 DO NOT TOUCH ANYTHING BELOW THIS LINE
# =========================================================

client = TelegramClient('iphone_final_session', API_ID, API_HASH)


async def main():
  print('Logging in and scanning your chats...')
  await client.start()

  target_chat_id = None
  async for dialog in client.iter_dialogs():
    if dialog.name == TARGET_GROUP_NAME:
      target_chat_id = dialog.id
      print(f'-> Connected to group "{dialog.name}" successfully!')
      break

  if not target_chat_id:
    print(
        f'❌ ERROR: Could not find any group named "{TARGET_GROUP_NAME}". Check'
        ' your spelling!'
    )
    return

  @client.on(events.NewMessage(chats=target_chat_id))
  async def handle_new_message(event):
    if event.text:
      message_text = event.text.lower()
      if any(keyword in message_text for keyword in KEYWORDS):
        try:
          await event.forward_to('me')
          print(f'Forwarded message matching keyword: "{event.text[:20]}..."')
        except Exception as e:
          print(f'Forwarding error: {e}')

  print('🎉 Script is successfully running and listening for keywords!')
  await client.run_until_disconnected()


if __name__ == '__main__':
  import asyncio

  asyncio.run(main())
