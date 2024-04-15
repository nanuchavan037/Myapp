import pytest
from flask import url_for
from flask_testing import TestCase
from app import app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_status_code(self):
        response = self.client.get(url_for('index'), follow_redirects=True)
        self.assert200(response)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    with app.app_context():
        response = client.get(url_for('index'), follow_redirects=True)
    assert response.status_code == 200