from rest_framework import serializers
from .models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ['slug', 'original_url', 'clicks', 'created_at']
        read_only_fields = ['slug', 'clicks', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ShortLinkDetailSerializer(ShortLinkSerializer):
    class Meta(ShortLinkSerializer.Meta):
        fields = ShortLinkSerializer.Meta.fields + ['user']
        read_only_fields = ShortLinkSerializer.Meta.read_only_fields + ['user']