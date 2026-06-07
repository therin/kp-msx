"""Best-effort Telegram alerts for kp-msx operational events.

Bot token + chat id come from env (Fly secrets), never from the repo. A failure
to deliver an alert must never break the request that triggered it.
"""
import hashlib
import html
import logging

import aiohttp

import config

log = logging.getLogger('kpmsx.alert')


async def send_telegram(text: str) -> None:
    token = config.TELEGRAM_ALERT_BOT_TOKEN
    chat_id = config.TELEGRAM_ALERT_CHAT_ID
    if not token or not chat_id:
        return
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as s:
            await s.post(
                f'https://api.telegram.org/bot{token}/sendMessage',
                json={
                    'chat_id': chat_id,
                    'text': text,
                    'parse_mode': 'HTML',
                    'disable_web_page_preview': True,
                },
            )
    except Exception as e:
        log.warning('Telegram alert failed: %s', e)


def new_device_message(device_id, user_agent) -> str:
    # The raw device id is the auth secret -> never send it. A short sha256 tag
    # is enough to correlate without leaking. user_agent is client-controlled and
    # parse_mode=HTML, so it must be escaped.
    tag = hashlib.sha256((device_id or '').encode()).hexdigest()[:10]
    ua = html.escape(user_agent or 'unknown')
    return (
        '🆕 <b>kp-msx: new device paired</b>\n'
        f'device: <code>{tag}</code>\n'
        f'user-agent: {ua}'
    )
