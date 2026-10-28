"""Run with: python -m unittest discover -s tests -v (Node.js required)."""
import json
import os
from pathlib import Path
import re
import subprocess
import unittest

# Set before importing the package: its app factory creates tables on import.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from ordiniBarScuolaBorsa import app, scheduler
from ordiniBarScuolaBorsa.models import Prodotto, User, db

if scheduler.running:
    scheduler.shutdown(wait=False)


class AdminTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.context = app.app_context()
        self.context.push()
        self.addCleanup(self.context.pop)
        self.assertEqual(db.engine.url.database, ":memory:")
        db.drop_all()
        db.create_all()
        app.config['ADMIN_EMAILS'] = {'admin@example.test'}
        user = User(google_id='admin', email='admin@example.test')
        db.session.add(user)
        db.session.commit()
        self.client = app.test_client()
        with self.client.session_transaction() as session:
            session['_user_id'] = str(user.id)
            session['_fresh'] = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def render_admin(self, path="/admin"):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    def check_frontend(self, html, scenario):
        result = subprocess.run(
            ["node", str(Path(__file__).with_name("test_admin_frontend.cjs")), scenario],
            input=html, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_database_and_both_urls(self):
        html = self.render_admin()
        self.assertEqual(html, self.render_admin("/admin/"))
        self.check_frontend(html, "empty")

    def test_database_products_filters_prices_and_read_only_display(self):
        name = 'Caffè </script><img src=x onerror=alert(1)> & "latte"'
        db.session.add_all([
            Prodotto(id=1, nome=name, costo=0, prezzo_euro=2.5,
                     prezzo_interni=0, categoria=" BEVANDE ", attivo=True),
            Prodotto(id=2, nome=name, categoria="bevande", attivo=False),
            Prodotto(id=3, nome="Toast", costo=1, prezzo_euro=2, categoria="cibi"),
            Prodotto(id=4, nome="Panino", costo=1, prezzo_euro=0, categoria="CIBO"),
            Prodotto(id=5, nome="Torta", categoria="dolci"),
            Prodotto(id=6, nome="Altro", categoria=None),
            Prodotto(id=7, nome="Speciale", categoria=" Stagionali "),
        ])
        db.session.commit()
        html = self.render_admin()
        payload = json.loads(re.search(r"const prodotti = (.*);", html).group(1))
        self.assertEqual([p["id"] for p in payload], list(range(1, 8)))
        self.assertEqual(payload[0]["nome"], name)
        self.assertEqual(payload[0]["prezzo"], 2.5)
        self.assertEqual(payload[0]["interni"], 0)
        self.assertIsNone(payload[1]["costo"])
        self.assertFalse(payload[1]["attivo"])
        self.assertNotIn(name, html)  # Script-closing characters are JSON-escaped.
        self.assertNotIn("cyber_menu_v3", html)
        self.assertNotIn('onclick="salva()"', html)
        self.assertNotIn('id="modal"', html)
        self.check_frontend(html, "products")
        self.assertEqual(Prodotto.query.count(), 7)


if __name__ == "__main__":
    unittest.main()
