import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from shortlinks.models import ShortLink


@pytest.mark.django_db
class TestShortLinkModel:
    def test_create_short_link(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        link = ShortLink.objects.create(
            user=user,
            original_url='https://example.com'
        )
        assert link.slug is not None
        assert len(link.slug) == 6
        assert link.clicks == 0
        assert link.user == user

    def test_slug_uniqueness(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        link1 = ShortLink.objects.create(
            user=user,
            original_url='https://example.com'
        )
        link2 = ShortLink.objects.create(
            user=user,
            original_url='https://google.com'
        )
        assert link1.slug != link2.slug

    def test_invalid_url_validation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        with pytest.raises(ValidationError):
            link = ShortLink(user=user, original_url='not-a-valid-url')
            link.full_clean()

    def test_url_scheme_validation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        with pytest.raises(ValidationError):
            link = ShortLink(user=user, original_url='ftp://example.com')
            link.full_clean()

    def test_increment_clicks(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        link = ShortLink.objects.create(
            user=user,
            original_url='https://example.com'
        )
        assert link.clicks == 0
        link.increment_clicks()
        assert link.clicks == 1