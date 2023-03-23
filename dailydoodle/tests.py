
from django.urls import reverse, resolve
from django.test import TestCase, Client
from .views import *
from datetime import date
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# c = Client() #test client used for some functions
# # Create your tests here.
#
# # URL TESTS
#
# class testClient(TestCase):
#     print(c.get('/dailydoodle/'))               #should result in a 200 response since it works
#     print(c.get('/dailydoodle/collections/')) #should result in a 302 redirect


# class TestClient(TestCase):
#     def setUp(self):
#         #Create a fake user
#         self.user = User.objects.create_user(username='test', password='testPassword')
#         self.details = {
#             'username': 'test',
#             'password': 'testPassword'
#         }
#
#     def test_authenticated_pages(self):
#
#         #response2 = self.client.get('/dailydoodle/collections/')
#         # response3 = self.client.get('/dailydoodle/submissions/dave')
#         # #response4 = self.client.get('/dailydoodle/profile/')
#         # #response5 = self.client.get('/dailydoodle/leaderboard/')
#         # response6 = self.client.get('/dailydoodle/draw/')
#         # response7 = self.client.get('/dailydoodle/drawing/')
#         #
#         #self.assertEqual(response2.status_code, 302) #test to make sure it redirects before logging in
#         # self.assertEqual(response3.status_code, 302)
#         # #self.assertEqual(response4.status_code, 302)
#         # #self.assertEqual(response5.status_code, 302)
#         # self.assertEqual(response6.status_code, 302)
#         # self.assertEqual(response7.status_code, 302)
#
#
#         self.client.login(**self.details) #login
#
#         # Make requests to authenticated URLs
#         response1 = self.client.get('/dailydoodle/')
#         response2 = self.client.get('/dailydoodle/collections/')
#         response3 = self.client.get('/dailydoodle/submissions/')
#         response4 = self.client.get('/dailydoodle/profile/')
#         response5 = self.client.get('/dailydoodle/leaderboard/')
#         response6 = self.client.get('/dailydoodle/draw/')
#         response7 = self.client.get('/dailydoodle/drawing/')
#
#         # Check that the responses are successful (status code 200)
#         self.assertEqual(response1.status_code, 200)
#         self.assertEqual(response2.status_code, 200)
#         self.assertEqual(response3.status_code, 200)
#         self.assertEqual(response4.status_code, 200)
#         self.assertEqual(response5.status_code, 200)
#         self.assertEqual(response6.status_code, 200)
#         self.assertEqual(response7.status_code, 200)




class SubmissionsPageURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:submissions', kwargs={'username': 'testuser'})
        expected_url = '/dailydoodle/submissions/testuser/'
        self.assertEquals(expected_url, url, f"Your URL mapping for submissions is either missing or mistyped.")


class HomepagePageURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:index')
        expected_url = '/dailydoodle/'
        self.assertEquals(expected_url, url, f"Your URL mapping for homepage is either missing or mistyped.")

class CollectionsPageURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:collections')
        expected_url = '/dailydoodle/collections/'
        self.assertEquals(expected_url, url, f"Your URL mapping for collections is either missing or mistyped.")

class ProfilePageURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:profile')
        expected_url = '/dailydoodle/profile/'
        self.assertEquals(expected_url, url, f"Your URL mapping for profile is either missing or mistyped.")

class DrawingURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:drawing', kwargs={'drawing_id': 'testDrawing'})
        expected_url = '/dailydoodle/drawing/testDrawing'
        self.assertEquals(expected_url, url, f"Your URL mapping for a drawing is either missing or mistyped.")

class DrawURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:draw')
        expected_url = '/dailydoodle/draw/'
        self.assertEquals(expected_url, url, f"Your URL mapping for draw is either missing or mistyped.")

class LeaderboardURLTest(TestCase):
    def test_mapping_exists(self):
        url = reverse('dailydoodle:leaderboard')
        expected_url = '/dailydoodle/leaderboard/'
        self.assertEquals(expected_url, url, f"Your URL mapping for leaderboard is either missing or mistyped.")

# class LoginURLTest(TestCase):  #these views dont exist as urls yet
#     def test_mapping_exists(self):
#         print(reverse('dailydoodle:loginview'))
#         url = reverse('dailydoodle:loginview')
#         expected_url = '/dailydoodle/login/'
#         self.assertEquals(expected_url, url, f"Your login mapping for leaderboard is either missing or mistyped.")

# class RegisterURLTest(TestCase):
#     def test_mapping_exists(self):
#         print(reverse('dailydoodle:register'))
#         url = reverse('dailydoodle:register')
#         expected_url = '/dailydoodle/accounts/register/'
#         self.assertEquals(expected_url, url, f"Your login mapping for register is either missing or mistyped.")


class IndexViewPageTest(TestCase):
    url = reverse("dailydoodle:index")

    def setUp(self):
        #create objects needed to
        self.user = User.objects.create_user(username="testuser2", email="testuser@test.com", password="testpassword")
        self.prompt = Prompt.objects.create(prompt="Test Prompt", prompt_date=date.today())
        self.drawing = Drawing.objects.create(drawing_id="testdrawing", drawing="submissions/testdrawing.jpeg", user=self.user, prompt=self.prompt)
        # create a test user profile
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.profile_picture = "profile_images/testuser2.jpg"
        self.user_profile.save()

    def test_index_loggedIn(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dailydoodle/index.html')
        self.assertEqual(response.context['current_link'], 'Homepage')
        self.assertEqual(response.context['prompt'], 'Test Prompt')
        self.assertEqual(response.context['top_drawings']['amount'], 1)
        self.assertEqual(response.context['MEDIA_URL'], '/media/')

    def test_index_notLogginedIn(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dailydoodle/index.html')
        self.assertEqual(response.context['current_link'], 'Homepage')
        self.assertEqual(response.context['prompt'], 'Test Prompt')
        self.assertEqual(response.context['top_drawings']['amount'], 1)
        self.assertNotIn('user_drawing', response.context)
        self.assertEqual(response.context['MEDIA_URL'], '/media/')




# test to ensure user creation actually works
class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_userCreation_works(self):# Check that a UserProfile object is created with the User object as its 'user' attribute
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.user, self.user)

#helper function for user creation test
@receiver(post_save, sender=User) #when a User model is saved,
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Call function above when User profile is crated
post_save.connect(create_user_profile, sender=User)
