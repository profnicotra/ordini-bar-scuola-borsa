import json
import os
import re
import runpy
import unittest
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from flask import g
from ordiniBarScuolaBorsa import app, scheduler
from ordiniBarScuolaBorsa.models import (
    db, Prodotto, Posizione, NoteGruppo, Note, Ordine, OrdineRiga,
    OrdineRigaNota, User, Impostazione,
)

if scheduler.running:
    scheduler.shutdown(wait=False)


class OrderSecurityTests(unittest.TestCase):
    def setUp(self):
        self.context = app.app_context()
        self.context.push()
        self.addCleanup(self.context.pop)
        self.assertEqual(db.engine.url.database, ':memory:')
        db.drop_all()
        db.create_all()
        self.previous_config = {key: app.config.get(key) for key in (
            'TESTING', 'ADMIN_EMAILS', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET',
            'REQUIRE_OPERATOR_LOGIN',
        )}
        app.config.update(TESTING=True, ADMIN_EMAILS={'operator@example.test'}, REQUIRE_OPERATOR_LOGIN=True)
        self.p = Prodotto(nome='Stesso nome', prezzo_euro=Decimal('2.00'),
                          prezzo_interni=Decimal('1.50'), attivo=True, categoria='bevande')
        self.q = Prodotto(nome='Stesso nome', prezzo_euro=Decimal('3.00'),
                          prezzo_interni=Decimal('0.00'), attivo=True, categoria='cibo')
        self.position = Posizione(nome='Aula test')
        self.operator = User(google_id='operator', email='operator@example.test')
        self.prof = User(google_id='prof', email='prof@scuola-borsa.it', is_professor=True)
        db.session.add_all([self.p, self.q, self.position, self.operator, self.prof,
                            Impostazione(chiave='bar_aperto', valore='true')])
        db.session.commit()
        self.client = app.test_client()
        self.request('GET', '/orders/')
        with self.client.session_transaction() as session:
            self.csrf = session['csrf_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        app.config.update(self.previous_config)

    def request(self, method, path, **kwargs):
        # Flask-Login caches the user on g; these tests hold an app context.
        g.pop('_login_user', None)
        return self.client.open(path, method=method, **kwargs)

    def login(self, user):
        with self.client.session_transaction() as session:
            session['_user_id'] = str(user.id)
            session['_fresh'] = True

    def post_order(self, items=None, **overrides):
        data = dict(prodottiSelezionati=json.dumps(items if items is not None else [
            dict(id=self.p.id, qty=2, price=0.01, selectedNotes={}),
        ]), nome='Mario', cognome="D’Angelo", classe=str(self.position.id),
            total='0.01', csrf_token=self.csrf)
        data.update(overrides)
        return self.request('POST', '/orders/new_order', data=data)

    def group(self, product=None, required=False, exclusive=False):
        group = NoteGruppo(nome='Gruppo ' + str(NoteGruppo.query.count()),
                           id_prodotto=(product or self.p).id,
                           obbligatorio_default=required, esclusivo=exclusive)
        db.session.add(group)
        db.session.flush()
        notes = [Note(nome='Extra', id_gruppo=group.id, price_delta_euro=Decimal('0.50')),
                 Note(nome='Extra due', id_gruppo=group.id, price_delta_euro=Decimal('0.25'))]
        db.session.add_all(notes)
        db.session.commit()
        return group, notes

    def test_total_and_price_are_calculated_and_duplicate_names_use_id(self):
        response = self.post_order([dict(id=self.q.id, qty=2, name=self.p.nome, price=0)])
        self.assertEqual(response.status_code, 201)
        order = Ordine.query.one()
        self.assertEqual(order.righe[0].prodotto_id, self.q.id)
        self.assertEqual(order.righe[0].prezzo_euro_unit, Decimal('3.00'))
        self.assertEqual(order.totale_euro, Decimal('6.00'))
        self.assertEqual(response.json['totale_euro'], 6)

    def test_professor_price_in_menu_and_order_including_zero(self):
        self.login(self.prof)
        response = self.request('GET', '/menu')
        products = json.loads(re.search(r'<script id="prodotti-data" type="application/json">(.*?)</script>',
                                       response.text, re.S).group(1))
        self.assertEqual({p['id']: p['prezzo_euro'] for p in products},
                         {self.p.id: '1.50', self.q.id: '0.00'})
        response = self.post_order([dict(id=self.q.id, qty=1)])
        self.assertEqual(response.status_code, 201)
        order = Ordine.query.one()
        self.assertEqual(order.totale_euro, 0)
        self.assertEqual(order.righe[0].prezzo_euro_unit, 0)
        self.assertEqual(order.user_id, self.prof.id)

    def test_notes_supplements_and_decimal_totals_are_saved(self):
        group, notes = self.group()
        response = self.post_order([dict(id=self.p.id, qty=3, selectedNotes={
            str(group.id): [dict(id=n.id, price_delta_euro=0) for n in notes],
        })])
        self.assertEqual(response.status_code, 201)
        order = Ordine.query.one()
        self.assertEqual(order.righe[0].prezzo_euro_unit, Decimal('2.75'))
        self.assertEqual(order.totale_euro, Decimal('8.25'))
        self.assertEqual(len(order.righe[0].note_righe), 2)

    def test_required_exclusive_foreign_and_duplicate_notes_rejected(self):
        group, notes = self.group(required=True, exclusive=True)
        other, foreign = self.group(product=self.q)
        bad = [
            {}, {str(group.id): []},
            {str(group.id): [dict(id=n.id) for n in notes]},
            {str(group.id): dict(id=foreign[0].id)},
            {str(other.id): dict(id=foreign[0].id)},
            {str(group.id): [dict(id=notes[0].id), dict(id=notes[0].id)]},
            {str(group.id): 'not a list'},
            {str(group.id): dict(id=True)},
        ]
        for selected in bad:
            with self.subTest(selected=selected):
                self.assertEqual(self.post_order([dict(id=self.p.id, qty=1, selectedNotes=selected)]).status_code, 400)
                self.assertEqual(Ordine.query.count(), 0)
                self.assertEqual(OrdineRigaNota.query.count(), 0)
        good = self.post_order([dict(id=self.p.id, qty=1, selectedNotes={str(group.id): dict(id=notes[0].id)})])
        self.assertEqual(good.status_code, 201)

    def test_inactive_or_missing_row_rejects_entire_order(self):
        self.q.attivo = False
        db.session.commit()
        for product_id in [self.q.id, 99999]:
            response = self.post_order([dict(id=self.p.id, qty=1), dict(id=product_id, qty=1)])
            self.assertEqual(response.status_code, 409)
            self.assertEqual(Ordine.query.count(), 0)
            self.assertEqual(OrdineRiga.query.count(), 0)

    def test_quantities_and_untrusted_payload_shapes(self):
        for qty in [0, -1, 11, 1000, 1.5, True, '2', None]:
            with self.subTest(qty=qty):
                self.assertEqual(self.post_order([dict(id=self.p.id, qty=qty)]).status_code, 400)
        for raw in ['broken', '{}', 'null', '[]', '[null]', '[1]', '[{"name":"Stesso nome","qty":1}]']:
            with self.subTest(raw=raw):
                self.assertEqual(self.post_order(prodottiSelezionati=raw).status_code, 400)
        response = self.post_order([dict(id=self.p.id, qty=6), dict(id=self.p.id, qty=6)])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ordine.query.count(), 0)

    def test_position_name_and_closed_bar(self):
        for change in [dict(classe='99999'), dict(classe='Aula test'), dict(nome=''), dict(cognome='')]:
            self.assertEqual(self.post_order(**change).status_code, 400)
        Impostazione.query.one().valore = 'false'
        db.session.commit()
        self.assertEqual(self.post_order().status_code, 409)
        self.assertEqual(Ordine.query.count(), 0)

    def test_csrf_and_operational_permissions(self):
        self.assertEqual(self.post_order(csrf_token='wrong').status_code, 400)
        self.assertEqual(self.request('GET', '/admin').status_code, 302)
        for method, path in [('GET', '/queue/api/ordini'), ('POST', '/toggle/changeBarStatus'),
                             ('DELETE', '/queue/api/ordini/1')]:
            self.assertEqual(self.request(method, path).status_code, 401)
        self.login(self.prof)
        for path in ['/admin', '/queue/', '/toggle/']:
            self.assertEqual(self.request('GET', path).status_code, 403)
        self.login(self.operator)
        for path in ['/admin', '/queue/', '/toggle/']:
            self.assertEqual(self.request('GET', path).status_code, 200)
        self.assertEqual(self.request('POST', '/toggle/changeBarStatus').status_code, 400)
        response = self.request('POST', '/toggle/changeBarStatus', data={'csrf_token': self.csrf})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Impostazione.query.one().valore, 'false')

    def test_queue_states_errors_and_delete(self):
        self.post_order()
        order = Ordine.query.one()
        self.login(self.operator)
        headers = {'X-CSRF-Token': self.csrf}
        for state in [None, '', 'INVALID', [], {}]:
            response = self.request('POST', f'/queue/api/ordini/{order.id}/stato',
                                    json={'stato': state}, headers=headers)
            self.assertEqual(response.status_code, 400)
        for state in ['IN_PREPARAZIONE', 'PRONTO', 'PRONTO']:
            previous = order.stato_pronto_da
            response = self.request('POST', f'/queue/api/ordini/{order.id}/stato',
                                    json={'stato': state}, headers=headers)
            self.assertEqual(response.status_code, 200)
            if previous:
                self.assertEqual(order.stato_pronto_da, previous)
        response = self.request('DELETE', f'/queue/api/ordini/{order.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ordine.query.count(), 0)
        self.assertEqual(OrdineRiga.query.count(), 0)

    def test_operator_login_can_be_disabled_without_disabling_csrf(self):
        self.assertEqual(self.post_order().status_code, 201)
        order_id = Ordine.query.one().id
        app.config['REQUIRE_OPERATOR_LOGIN'] = False
        for path in ['/admin', '/queue/', '/toggle/', '/queue/api/ordini']:
            self.assertEqual(self.request('GET', path).status_code, 200)
        for method, path in [('POST', '/toggle/changeBarStatus'),
                             ('POST', f'/queue/api/ordini/{order_id}/stato'),
                             ('DELETE', f'/queue/api/ordini/{order_id}')]:
            self.assertEqual(self.request(method, path).status_code, 400)
        headers = {'X-CSRF-Token': self.csrf}
        response = self.request('POST', f'/queue/api/ordini/{order_id}/stato',
                                json={'stato': 'PRONTO'}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ordine.query.one().stato, 'PRONTO')
        self.assertEqual(self.request('DELETE', f'/queue/api/ordini/{order_id}', headers=headers).status_code, 200)
        self.assertEqual(self.request('POST', '/toggle/changeBarStatus', headers=headers).status_code, 302)
        self.login(self.prof)
        self.assertEqual(self.request('GET', '/admin').status_code, 200)
        app.config['REQUIRE_OPERATOR_LOGIN'] = True
        self.assertEqual(self.request('GET', '/admin').status_code, 403)

    def test_operator_login_configuration_is_protected_by_default(self):
        config_path = Path(__file__).resolve().parents[1] / 'ordiniBarScuolaBorsa' / 'config.py'
        with patch.dict(os.environ):
            os.environ.pop('REQUIRE_OPERATOR_LOGIN', None)
            self.assertTrue(runpy.run_path(str(config_path))['REQUIRE_OPERATOR_LOGIN'])
            for value in ['true', 'TRUE', '', 'invalid', '0']:
                os.environ['REQUIRE_OPERATOR_LOGIN'] = value
                self.assertTrue(runpy.run_path(str(config_path))['REQUIRE_OPERATOR_LOGIN'])
            for value in ['false', ' FALSE ']:
                os.environ['REQUIRE_OPERATOR_LOGIN'] = value
                self.assertFalse(runpy.run_path(str(config_path))['REQUIRE_OPERATOR_LOGIN'])

    def test_storage_failure_is_reported_without_success(self):
        with patch('ordiniBarScuolaBorsa.order_service.db.session.commit', side_effect=RuntimeError('test')):
            response = self.post_order()
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertEqual(Ordine.query.count(), 0)

    def test_google_only_templates_and_missing_configuration(self):
        for path in ['/', '/menu', '/login']:
            response = self.request('GET', path)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('type="password"', response.text)
            self.assertNotIn('action="/register"', response.text)
            self.assertNotIn('action="/login"', response.text)
        app.config.update(GOOGLE_CLIENT_ID='', GOOGLE_CLIENT_SECRET='')
        response = self.request('GET', '/auth/login')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Accesso Google non disponibile', response.text)

    def test_google_callback_verified_email_and_domain(self):
        with self.client.session_transaction() as session:
            session['nonce'] = 'test-nonce'
        claims = dict(email='PERSON@SCUOLA-BORSA.IT', email_verified=True,
                      sub='test-google-sub', given_name='Test', family_name='Google')
        with patch('ordiniBarScuolaBorsa.auth.oauth') as oauth:
            oauth.google.authorize_access_token.return_value = {}
            oauth.google.parse_id_token.return_value = claims
            response = self.request('GET', '/auth/callback')
            oauth.google.parse_id_token.assert_called_once_with({}, nonce='test-nonce')
        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(google_id='test-google-sub').one()
        self.assertEqual(user.email, 'person@scuola-borsa.it')
        self.assertTrue(user.is_professor)

    def test_google_callback_rejects_unverified_email(self):
        with self.client.session_transaction() as session:
            session['nonce'] = 'test-nonce'
        claims = dict(email='unverified@example.test', email_verified=False, sub='unverified')
        with patch('ordiniBarScuolaBorsa.auth.oauth') as oauth:
            oauth.google.authorize_access_token.return_value = {}
            oauth.google.parse_id_token.return_value = claims
            self.request('GET', '/auth/callback')
        self.assertIsNone(User.query.filter_by(google_id='unverified').first())

    def test_google_login_starts_with_nonce_and_callback(self):
        from flask import redirect
        app.config.update(GOOGLE_CLIENT_ID='test', GOOGLE_CLIENT_SECRET='test')
        with patch('ordiniBarScuolaBorsa.auth.oauth') as oauth:
            oauth.google.authorize_redirect.return_value = redirect('https://accounts.google.com/test')
            response = self.request('GET', '/auth/login')
            self.assertEqual(response.status_code, 302)
            args, kwargs = oauth.google.authorize_redirect.call_args
            self.assertTrue(args[0].endswith('/auth/callback'))
            with self.client.session_transaction() as session:
                self.assertEqual(kwargs['nonce'], session['nonce'])
