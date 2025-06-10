import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from shortlinks.models import ShortLink


@pytest.mark.django_db
class TestRedirectView:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_redirect_increments_clicks(self):
        link = ShortLink.objects.create(
            user=self.user,
            original_url='https://example.com'
        )
        
        url = reverse('redirect', kwargs={'slug': link.slug})
        response = self.client.get(url)
        
        assert response.status_code == 302
        assert response.url == 'https://example.com'
        
        link.refresh_from_db()
        assert link.clicks == 1

    def test_redirect_nonexistent_slug(self):
        url = reverse('redirect', kwargs={'slug': 'nonexistent'})
        response = self.client.get(url)
        
        assert response.status_code == 404