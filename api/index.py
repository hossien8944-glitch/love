from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.parse
import urllib.request

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        response = {"status": "ok", "message": "Love Question API is working ❤️"}
        self.wfile.write(json.dumps(response).encode("utf-8"))

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
                "💌 جواب جدید رسید!\n\n"
                f"👤 اسم: {name}\n"
                f"❤️ جواب: {answer}"
            )

            telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
            telegram_data = urllib.parse.urlencode({
                "chat_id": chat_id,
                "text": message
            }).encode()

            req = urllib.request.Request(telegram_url, data=telegram_data, method="POST")
            urllib.request.urlopen(req)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
