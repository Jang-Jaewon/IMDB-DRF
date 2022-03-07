from django.contrib.auth.models import User
from django.urls                import reverse

from rest_framework                  import status
from rest_framework.test             import APITestCase
from rest_framework.authtoken.models import Token

from contents.api import serializers
from contents     import models


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user  = User.objects.create_user(username="example", password="password!@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
        
    def test_streamplatform_create(self):
        data = {
            "name"    : "Netflix",
            "about"   : "#1 Streaming Plarform",
            "website" : "https://netflix.com" 
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class ContentListTestCase(APITestCase):
    
    def setUp(self):
        self.user  = User.objects.create_user(username="example", password="password!@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream  = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
        self.content = models.Content.objects.create(title="Example Movie", storyline="Example Movie is...", platform=self.stream, active=True) 
        
    def test_contentlist_create(self):
        data = {
            "title" : "Example Movie",
            "storyline" : "Example Movie is...",
            "platform" : self.stream,
            "active" : True
        }
        response = self.client.post(reverse('content-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_contentlist_list(self):
        response = self.client.get(reverse('content-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_contentlist_detail(self):
        response = self.client.get(reverse('content-detail', args=(self.content.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Content.objects.count(), 1)
        self.assertEqual(models.Content.objects.get().title, 'Example Movie')
        
    