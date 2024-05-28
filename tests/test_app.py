from .. import app

def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.data.decode() == "Hello from Daniel Tsoref"
