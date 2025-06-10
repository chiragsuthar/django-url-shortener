from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ShortLink
from .serializers import ShortLinkSerializer, ShortLinkDetailSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ShortLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = ShortLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShortLink.objects.filter(user=self.request.user)


class ShortLinkDetailView(generics.RetrieveAPIView):
    serializer_class = ShortLinkDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return ShortLink.objects.filter(user=self.request.user)


def redirect_view(request, slug):
    """Redirect endpoint that increments clicks and redirects to original URL"""
    try:
        short_link = ShortLink.objects.get(slug=slug)
        short_link.increment_clicks()
        return redirect(short_link.original_url, permanent=False)
    except ShortLink.DoesNotExist:
        raise Http404("Short link not found")