import asyncio
import os
import sys
from telethon import TelegramClient, events

API_ID = 34195900
API_HASH = '1b8f2c2a7f8c3580eea7b568b2bdeace'
TARGET_GROUP_NAME = 'SolHouse Signal VIP'
KEYWORDS = ['💎 diamond', 'high risk signal']

PHONE = os.getenv('TELEGRAM_PHONE')
CODE = os.getenv('TELEGRAM_CODE')


async def main():
  # We use a persistent session file name so Render saves the login state
  client = TelegramClient(
      '/opt/render/project/src/session_name', API_ID, API_HASH
  )

  await client.connect()

  if not await client.is_user_authorized():
    if not CODE:
      print(f'Sending code request to {PHONE}...')
      await client.send_code_request(PHONE)
      print('➡️ STATUS: New code requested! Check Telegram and update TELEGRAM_CODE.')
      return
    else:
      try:
        # If a code is provided, log in safely
        await client.sign_in(PHONE, CODE)
        print('✅ Logged in successfully!')
      except Exception as e:
        print(f'❌ Login failed: {e}. Please request a fresh code.')
        return

  print('Scanning your chats...')
  target_chat_id = None
  async for dialog in client.iter_dialogs():
    if dialog.name == TARGET_GROUP_NAME:
      target_chat_id = dialog.id
      break

  if not target_chat_id:
    print(f'❌ ERROR: Could not find any group named "{TARGET_GROUP_NAME}".')
    return

  @client.on(events.NewMessage(chats=target_chat_id))
  async def handle_new_message(event):
    if event.text:
      message_text = event.text.lower()
      if any(keyword in message_text for keyword in KEYWORDS):
        try:
          await event.forward_to('me')
          print(f'Forwarded matching message!')
        except Exception as e:
          print(f'Forwarding error: {e}')

  print('🎉 Script is successfully running and listening for keywords!')
  await client.run_until_disconnected()


if __name__ == '__main__':
  import asyncio

  asyncio.run(main())
