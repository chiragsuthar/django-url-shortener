import secrets
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_url_scheme(value):
    """Validate that URL starts with http:// or https://"""
    if not (value.startswith('http://') or value.startswith('https://')):
        raise ValidationError('URL must start with http:// or https://')


class ShortLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_links')
    original_url = models.URLField(validators=[URLValidator(), validate_url_scheme])
    slug = models.CharField(max_length=10, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'slug']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.slug} -> {self.original_url}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """Generate a unique 6-character slug"""
        while True:
            slug = secrets.token_urlsafe(6)[:6]
            if not ShortLink.objects.filter(slug=slug).exists():
                return slug

    def increment_clicks(self):
        """Safely increment the click counter"""
        ShortLink.objects.filter(pk=self.pk).update(clicks=models.F('clicks') + 1)
        self.refresh_from_db()