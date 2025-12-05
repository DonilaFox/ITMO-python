from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
import sys

from models import Author
from controllers.databasecontroller import CurrencyRatesCRUD

# === Инициализация ===
author = Author(name="Daniil Zhohov", group="P3123")
db = CurrencyRatesCRUD()

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            # === / — Главная ===
            if path == '/':
                currencies = db.read_all_currencies()
                self._render('index.html', {
                    'app_name': 'CurrenciesListApp',
                    'author_name': author.name,
                    'group': author.group,
                    'currencies': currencies
                })

            # === /author ===
            elif path == '/author':
                self._render('author.html', {
                    'author_name': author.name,
                    'group': author.group
                })

            # === /users ===
            elif path == '/users':
                users = db.get_all_users()
                self._render('users.html', {'users': users})

            # === /user?id=... ===
            elif path == '/user':
                user_id_str = query.get('id', [None])[0]
                if not user_id_str or not user_id_str.isdigit():
                    self.send_error(400, "Invalid user ID")
                    return
                user_id = int(user_id_str)
                user = db.get_user_by_id(user_id)
                if not user:
                    self.send_error(404, "User not found")
                    return
                currencies = db.get_user_currencies(user_id)
                self._render('user.html', {'user': user, 'currencies': currencies})

            # === /currencies ===
            elif path == '/currencies':
                currencies = db.read_all_currencies()
                self._render('currencies.html', {'currencies': currencies})

            # === /currency/delete?id=... ===
            elif path == '/currency/delete':
                currency_id_str = query.get('id', [None])[0]
                if currency_id_str and currency_id_str.isdigit():
                    db.delete_currency(int(currency_id_str))
                self._redirect('/currencies')

            # === /currency/update?USD=... ===
            elif path == '/currency/update':
                # Ищем любой ключ в query (например, 'USD', 'EUR')
                if query:
                    for char_code, values in query.items():
                        if values and char_code.isalpha() and len(char_code) == 3:
                            try:
                                new_value = float(values[0])
                                db.update_currency_value(char_code, new_value)
                            except ValueError:
                                pass  # игнорируем некорректные значения
                self._redirect('/currencies')

            # === /currency/show ===
            elif path == '/currency/show':
                currencies = db.read_all_currencies()
                print("\n=== Валюты в базе (DEBUG) ===")
                for c in currencies:
                    print(f"{c.char_code}: {c.name} = {c.value} за {c.nominal}")
                print("=== Конец списка ===\n")
                self._redirect('/currencies')

            else:
                self.send_error(404)

        except Exception as e:
            import traceback
            print("Ошибка:", e)
            traceback.print_exc()
            self.send_error(500, str(e))

    def _render(self, template_name, context):
        template = env.get_template(template_name)
        html = template.render(**context)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Сервер запущен на http://localhost:8000")
    print("Доступные маршруты:")
    print("  /")
    print("  /author")
    print("  /users")
    print("  /user?id=1")
    print("  /currencies")
    print("  /currency/delete?id=1")
    print("  /currency/update?USD=100.5")
    print("  /currency/show")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        db.close()
        print("\nСервер остановлен.")

if __name__ == '__main__':
    run()