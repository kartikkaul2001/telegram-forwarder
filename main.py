import asyncio
import os
import sys
from telethon import TelegramClient, events

# Credentials
API_ID = 34195900
API_HASH = '1b8f2c2a7f8c3580eea7b568b2bdeace'
TARGET_GROUP_NAME = 'SolHouse Signal VIP'
KEYWORDS = ['💎 diamond', 'high risk signal']

# Retrieve phone and code from Render environment variables
PHONE = os.getenv('TELEGRAM_PHONE')
CODE = os.getenv('TELEGRAM_CODE')

if not PHONE:
  print(
      '❌ ERROR: TELEGRAM_PHONE variable is missing. Please add it in Render'
      ' Settings!'
  )
  sys.exit(1)


async def main():
  print('Initializing Telegram client...')
  client = TelegramClient('render_session', API_ID, API_HASH)

  await client.connect()

  # If not authorized, try logging in using the variables
  if not await client.is_user_authorized():
    if not CODE:
      print(f'Sending login code request to {PHONE}...')
      await client.send_code_request(PHONE)
      print(
          '➡️ STEP 1 COMPLETE: Login code sent! Please check your Telegram app,'
          ' copy the code, add it as TELEGRAM_CODE in Render Settings, and'
          ' redeploy.'
      )
      return
    else:
      try:
        print(f'Attempting to log in with code: {CODE}...')
        await client.sign_in(PHONE, CODE)
        print('✅ Logged in successfully!')
      except Exception as e:
        print(f'❌ Login failed: {e}. Please update TELEGRAM_CODE and try again.')
        return

  print('Scanning your chats...')
  target_chat_id = None
  async for dialog in client.iter_dialogs():
    if dialog.name == TARGET_GROUP_NAME:
      target_chat_id = dialog.id
      print(f'-> Connected to group "{dialog.name}" successfully!')
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
          print(f'Forwarded message: "{event.text[:20]}..."')
        except Exception as e:
          print(f'Forwarding error: {e}')

  print('🎉 Script is successfully running and listening for keywords!')
  await client.run_until_disconnected()


if __name__ == '__main__':
  import asyncio

  asyncio.run(main())

