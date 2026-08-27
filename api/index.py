from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse
import urllib.request


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)

            name = data.get("name", "بدون نام")
            answer = data.get("answer", "بدون جواب")

            token = os.environ.get("BOT_TOKEN")
            chat_id = os.environ.get("CHAT_ID")

            message = (
                "💌 جواب جدید!\n\n"
                f"👤 اسم: {name}\n"
                f"❤️ جواب: {answer}"
            )

            telegram_url = (
                f"https://api.telegram.org/bot{token}/sendMessage"
            )

            telegram_data = urllib.parse.urlencode({
                "chat_id": chat_id,
                "text": message
            }).encode()

            request = urllib.request.Request(
                telegram_url,
                data=telegram_data,
                method="POST"
            )

            urllib.request.urlopen(request)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": True
                }).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode()
            )
