import pytest
import os
from webapp_ci.app import app, db, Feedback

@pytest.fixture
def client(tmp_path):
    # use a temporary sqlite db for tests
    db_file = tmp_path / "test.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    app.config['TESTING'] = True
    with app.test_client() as client:
        # create tables before tests
        with app.app_context():
            db.create_all()
        yield client
        # drop tables after tests
        with app.app_context():
            db.drop_all()

def test_index_empty(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'no feedback yet' in resp.data

def test_submit_and_persist(client):
    # submit two comments
    client.post('/submit', data={'comment': 'first'}, follow_redirects=True)
    client.post('/submit', data={'comment': 'second'}, follow_redirects=True)
    # index should list both
    resp = client.get('/')
    assert b'first' in resp.data
    assert b'second' in resp.data

def test_submit_empty_ignored(client):
    # submitting empty should do nothing
    client.post('/submit', data={'comment': ''}, follow_redirects=True)
    resp = client.get('/')
    assert b'no feedback yet' in resp.data

def test_static_css_served(client):
    # ensure css file is served
    resp = client.get('/static/css/style.css')
    assert resp.status_code == 200
    assert b'body' in resp.data  # style.css contains 'body {'
