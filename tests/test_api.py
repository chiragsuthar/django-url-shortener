import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from shortlinks.models import ShortLink


@pytest.mark.django_db
class TestShortLinkAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_create_short_link_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('shortlink-list-create')
        data = {'original_url': 'https://example.com'}
        
        response = self.client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'slug' in response.data
        assert response.data['original_url'] == 'https://example.com'
        assert response.data['clicks'] == 0

    def test_create_short_link_unauthenticated(self):
        url = reverse('shortlink-list-create')
        data = {'original_url': 'https://example.com'}
        
        response = self.client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_user_links(self):
        self.client.force_authenticate(user=self.user)
        # Create a link for this user
        ShortLink.objects.create(
            user=self.user,
            original_url='https://example.com'
        )
        # Create a link for another user
        other_user = User.objects.create_user(username='other', password='pass')
        ShortLink.objects.create(
            user=other_user,
            original_url='https://google.com'
        )
        
        url = reverse('shortlink-list-create')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['original_url'] == 'https://example.com'

    def test_get_link_detail(self):
        self.client.force_authenticate(user=self.user)
        link = ShortLink.objects.create(
            user=self.user,
            original_url='https://example.com'
        )
        
        url = reverse('shortlink-detail', kwargs={'slug': link.slug})
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['slug'] == link.slug
        assert response.data['original_url'] == 'https://example.com'