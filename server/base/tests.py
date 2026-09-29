from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestLandingPage:
    def test_home_returns_200(self, client):
        response = client.get(reverse("home"))
        assert response.status_code == 200

    def test_home_uses_welcome_template(self, client):
        response = client.get(reverse("home"))
        assert b"Responsive left-aligned hero" in response.content

    def test_home_content_type_is_html(self, client):
        response = client.get(reverse("home"))
        assert "text/html" in response["Content-Type"]


@pytest.mark.django_db
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get(reverse("health"))
        assert response.status_code == 200

    def test_health_payload(self, client):
        response = client.get(reverse("health"))
        assert response.json() == {"status": "ok"}

    def test_health_content_type_is_json(self, client):
        response = client.get(reverse("health"))
        assert "application/json" in response["Content-Type"]

    def test_unknown_api_path_returns_404(self, client):
        response = client.get("/api/does-not-exist/")
        assert response.status_code == 404


class TestAdmin:
    def test_admin_redirects_to_login(self, client):
        response = client.get("/admin/")
        assert response.status_code in {301, 302}
