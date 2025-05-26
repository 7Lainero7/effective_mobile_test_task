from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Ad, ExchangeProposal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image_url = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Ad
        fields = ['id', 'user', 'title', 'description', 'image_url', 'category', 'condition', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class AdCreateSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    sender_ad_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        source='ad_sender',
        write_only=True
    )
    receiver_ad_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        source='ad_receiver',
        write_only=True
    )

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver',
            'sender_ad_id', 'receiver_ad_id',
            'comment', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'ad_sender', 'ad_receiver', 'status', 'created_at']


class ExchangeProposalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['status']
