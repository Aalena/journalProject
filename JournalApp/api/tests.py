from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings

payload_hanlder = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER
# automated
# new / blank db
from JournalApp.models import Journal
User = get_user_model()
class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User.objects.create(username="testUser",email='test@test.com')
        user_obj.set_password("!@345678")
        user_obj.save()
        journal_post = Journal.objects.create(owner=user_obj,
                                              title = "29th March",
                                              quote="Progress is vital"
                                              )


    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_journal(self):
        journal_count = Journal.objects.count()
        self.assertEqual(journal_count, 1)

    def test_get_list(self):
        # tested the get list
        data = {}
        url = api_reverse("api:api-view")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_item(self):
        data = {"title":"30th March","quote":"Just do it","grateful_for":"Fresh Air","today_view":"Love yourself"}
        url = api_reverse("api:api-view")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        journal_post = Journal.objects.first()
        data = {}
        url = journal_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        journal_post = Journal.objects.first()
        url = journal_post.get_api_url()
        data = {"title":"30th March","quote":"Just do it","grateful_for":"Fresh Air","today_view":"Love yourself"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_item_with_user(self):
        journal_post = Journal.objects.first()
        url = journal_post.get_api_url()
        data = {"title":"30th March","quote":"Just do it","grateful_for":"Fresh Air","today_view":"Love yourself"}
        user_obj = User.objects.first()
        payload = payload_hanlder(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_rsp) # JWT <token
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)