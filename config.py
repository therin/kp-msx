import os


MSX_HOST = os.environ.get('RENDER_EXTERNAL_URL') or os.environ.get('MSX_HOST')
MONGODB_URL = os.environ.get('MONGODB_URL')
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION') or 'kp'
SQLITE_URL = os.environ.get('SQLITE_URL') or './kp-sqlite.db'
IS_SQLITE = (MONGODB_URL is None or len(MONGODB_URL) == 0) and len(SQLITE_URL) > 0
PORT = os.environ.get('PORT') or 10000
PLAYER = os.environ.get('PLAYER') or 'https://slonopot.github.io/msx-hlsx/hlsx.html'
ALTERNATIVE_PLAYER = os.environ.get('ALTERNATIVE_PLAYER') or 'http://msx.benzac.de/plugins/html5x.html'
KP_CLIENT_ID = os.environ.get('KP_CLIENT_ID') or 'xbmc'
KP_CLIENT_SECRET = os.environ.get('KP_CLIENT_SECRET') or 'cgg3gtifu46urtfp2zp1nqtba0k2ezxh'
QUALITY = os.environ.get('QUALITY')
PROTOCOL = os.environ.get('PROTOCOL') or 'hls4'
TIZEN = os.environ.get('TIZEN') == 'yes'

# Bearer token guarding the public /metrics endpoint (Prometheus scrape auth).
# Unset -> /metrics fails closed (403). Set as a Fly secret, never in the repo.
METRICS_TOKEN = os.environ.get('METRICS_TOKEN')

# Telegram operational alerts (e.g. new device paired). Unset -> alerts are no-ops.
# Set as Fly secrets, never in the repo.
TELEGRAM_ALERT_BOT_TOKEN = os.environ.get('TELEGRAM_ALERT_BOT_TOKEN')
TELEGRAM_ALERT_CHAT_ID = os.environ.get('TELEGRAM_ALERT_CHAT_ID')
