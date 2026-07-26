import urllib.request


def test_ai_health():

    url = "http://localhost:8100/health"

    response = urllib.request.urlopen(url)

    assert response.status == 200
