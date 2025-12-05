from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App, User, UserCurrency
from utils.currencies_api import get_currencies

# Инициализация данных
author = Author(name="Daniil Zhohov", group="P3123")
app = App(name="CurrenciesListApp", version="1.0", author=author)

# Тестовые данные
users = [
    User("Alexander Radulov"),
    User("Alexander Yelesin"),
]
# Подписки (user_id → list of currency_id)
user_subscriptions = [
    UserCurrency(1, "R01235"),  # USD
    UserCurrency(1, "R01239"),  # EUR
    UserCurrency(2, "R01375"),  # CNY
]

# Jinja2 Environment
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        if path == '/':
            template = env.get_template("index.html")
            html = template.render(
                app_name=app.name,
                app_version=app.version,
                author_name=author.name,
                group=author.group
            )
        elif path == '/author':
            template = env.get_template("index.html")
            html = template.render(
                app_name="Информация об авторе",
                author_name=author.name,
                group=author.group
            )
        elif path == '/users':
            template = env.get_template("users.html")
            html = template.render(users=users)
        elif path == '/user':
            user_id = int(query.get('id', [None])[0])
            user = next((u for u in users if u.id == user_id), None)
            if not user:
                self.send_response(404)
                self.wfile.write(b"User not found")
                return
            # Находим подписки
            subs = [uc for uc in user_subscriptions if uc.user_id == user.id]
            # Получаем курсы
            try:
                currencies = {c.id: c for c in get_currencies()}
                user_currencies = [currencies[uc.currency_id] for uc in subs if uc.currency_id in currencies]
            except:
                user_currencies = []

            template = env.get_template("user.html")
            html = template.render(user=user, currencies=user_currencies)
        elif path == '/currencies':
            try:
                currencies = get_currencies()
            except:
                currencies = []
            template = env.get_template("currencies.html")
            html = template.render(currencies=currencies)
        else:
            self.send_response(404)
            self.wfile.write(b"Not found")
            return

        self.wfile.write(html.encode('utf-8'))

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Сервер запущен на http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    run()