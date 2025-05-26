from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Ad, ExchangeProposal


User = get_user_model()

class AdAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.ad_data = {
            'title': 'Test Ad',
            'description': 'Test Description',
            'category': 'Books',
            'condition': 'new'
        }

    def test_create_ad(self):
        url = reverse('ad-list')
        response = self.client.post(url, self.ad_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 1)

    def test_edit_ad(self):
        ad = Ad.objects.create(user=self.user, **self.ad_data)
        url = reverse('ad-detail', args=[ad.id])
        response = self.client.patch(url, {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ad.refresh_from_db()
        self.assertEqual(ad.title, 'Updated Title')

    def test_delete_ad(self):
        ad = Ad.objects.create(user=self.user, **self.ad_data)
        url = reverse('ad-detail', args=[ad.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_search_ad(self):
        Ad.objects.create(user=self.user, **self.ad_data)
        url = reverse('ad-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

class ExchangeProposalAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.ad1 = Ad.objects.create(user=self.user1, title='Ad1', description='desc', category='Books', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ad2', description='desc', category='Books', condition='used')
        self.client.login(username='user1', password='pass1')

    def test_create_proposal(self):
        url = reverse('exchangeproposal-list')
        data = {
            'sender_ad_id': self.ad1.id,
            'receiver_ad_id': self.ad2.id,
            'comment': 'Want to exchange'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_update_proposal_status(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='test')
        url = reverse('exchangeproposal-detail', args=[proposal.id])
        self.client.login(username='user2', password='pass2')
        response = self.client.patch(url, {'status': 'accepted'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')
