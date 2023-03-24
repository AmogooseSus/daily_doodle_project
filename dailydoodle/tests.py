from django.test import TestCase, Client
from .views import *
from datetime import date
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import os


class TestClient(TestCase):
    def setUp(self):
        # Create a fake user for login tests
        self.user = User.objects.create_user(username='test', password='testPassword')
        self.details = {
            'username': 'test',
            'password': 'testPassword'
        }

    def testAuthenticatedPages(self):
        response2 = self.client.get('/dailydoodle/collections/')
        response3 = self.client.get('/dailydoodle/submissions/dave')
        response4 = self.client.get('/dailydoodle/profile/')
        response5 = self.client.get('/dailydoodle/leaderboard/')
        response6 = self.client.get('/dailydoodle/draw/')
        response7 = self.client.get('/dailydoodle/drawing/')
                                                      # 200= success, 404notfound, 302/301redirects
        self.assertEqual(response2.status_code, 302)  # test to make sure it redirects before logging in
        self.assertEqual(response3.status_code, 301)
        self.assertEqual(response4.status_code, 302)
        self.assertEqual(response5.status_code, 302)
        self.assertEqual(response6.status_code, 302)
        self.assertEqual(response7.status_code, 404)  # page shouldnt display without a drawing id

        self.client.login(**self.details)  # login

        # Make requests to authenticated URLs
        response1 = self.client.get('/dailydoodle/')
        response2 = self.client.get('/dailydoodle/collections/')
        response3 = self.client.get('/dailydoodle/submissions/')
        response4 = self.client.get('/dailydoodle/profile/')
        response5 = self.client.get('/dailydoodle/leaderboard/')
        response6 = self.client.get('/dailydoodle/draw/')
        response7 = self.client.get('/dailydoodle/drawing/')

        # Check that the responses are successful
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 404)  # shouldnt exist without a username
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response7.status_code, 404)  # shouldnt exist without a drawing id


class SubmissionsPageURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:submissions', kwargs={'username': 'tester'})
        expected_url = '/dailydoodle/submissions/tester/'
        self.assertEquals(expected_url, url, f"Your URL mapping for submissions is either missing or mistyped.")


class HomepagePageURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:index')
        expected_url = '/dailydoodle/'
        self.assertEquals(expected_url, url, f"Your URL mapping for homepage is either missing or mistyped.")


class CollectionsPageURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:collections')
        expected_url = '/dailydoodle/collections/'
        self.assertEquals(expected_url, url, f"Your URL mapping for collections is either missing or mistyped.")


class ProfilePageURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:profile')
        expected_url = '/dailydoodle/profile/'
        self.assertEquals(expected_url, url, f"Your URL mapping for profile is either missing or mistyped.")


class DrawingURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:drawing', kwargs={'drawing_id': 'testDrawing'})
        expected_url = '/dailydoodle/drawing/testDrawing'
        self.assertEquals(expected_url, url, f"Your URL mapping for a drawing is either missing or mistyped.")


class DrawURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:draw')
        expected_url = '/dailydoodle/draw/'
        self.assertEquals(expected_url, url, f"Your URL mapping for draw is either missing or mistyped.")


class LeaderboardURLTest(TestCase):
    def testURLexists(self):
        url = reverse('dailydoodle:leaderboard')
        expected_url = '/dailydoodle/leaderboard/'
        self.assertEquals(expected_url, url, f"Your URL mapping for leaderboard is either missing or mistyped.")


class IndexViewTest(TestCase):
    url = reverse("dailydoodle:index")

    def setUp(self):
        # create objects needed to run each test
        self.user = User.objects.create_user(username="testuser2", email="testuser@test.com", password="testpassword")
        self.prompt = Prompt.objects.create(prompt="TestPrompt", prompt_date=date.today())
        self.drawing = Drawing.objects.create(drawing_id="testdrawing", drawing="submissions/testdrawing.jpeg",
                                              user=self.user, prompt=self.prompt)
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.profile_picture = "profile_images/testuser2.jpg"
        self.user_profile.save()

    # test homepage returns correct data when logged in, and then not logged in
    def testHomepageAuthenticated(self):
        self.client.login(username='testuser2', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['prompt'], 'TestPrompt')
        self.assertEqual(response.context['top_drawings']['amount'], 1)
        self.assertEqual(response.context['MEDIA_URL'], '/media/')

    def testHomepageNotAuth(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['prompt'], 'TestPrompt')
        self.assertEqual(response.context['top_drawings']['amount'], 1)
        self.assertNotIn('user_drawing', response.context)
        self.assertEqual(response.context['MEDIA_URL'], '/media/')

        # test the correct buttons appear on nav

    def testHomepageButtonDisplay(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # if not logged in we can still see this page
        self.assertContains(response,
                            '<a class="block text-main_gray text-bold w-full h-full" href="/accounts/register/">Register</a>',
                            html=True)
        self.assertContains(response,
                            '<a class="block text-main_gray text-bold w-full h-full" href="/accounts/login/">Login</a>',
                            html=True)


# helper function for user creation test - called automatically
# when a user object is created don't delete or you'll have a bad time
@receiver(post_save, sender=User)  # when a User model is saved,
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Call function above when User profile is crated
post_save.connect(createUserProfile, sender=User)


# some models tests, creation mainly
class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='pass'
        )

        self.prompt = Prompt.objects.create(
            prompt='testprom',
            prompt_date=date.today()
        )
        self.drawing = Drawing.objects.create(
            drawing_id='testdraw',
            user=self.user,
            prompt=self.prompt
        )
        self.comment = Comment.objects.create(
            user=self.user,
            date=date.today(),
            comment='testcomm',
            drawing=self.drawing
        )

    def test_prompt_str(self):
        self.assertEqual(str(self.prompt), 'testprom')

    def test_drawing_str(self):
        self.assertEqual(str(self.drawing), 'testdraw')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'testcomm')

    def testUpvote(self):
        rating = Rating.objects.create(
            user=self.user,
            drawing=self.drawing
        )
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.upvotes_recieved, 1)
        self.assertEqual(self.drawing.total_upvotes, 1)


class UserAccountFuncs(TestCase):
    def setUp(self):
        # create a doomed user
        self.user = User.objects.create_user(username="Killme", password="please")
        self.client = Client()  # simulate an actual client login
        self.client.login(username="Killme", password="please")

    def nameChangeTest(self):
        response = self.client.post('/profile/', {'username_change': 'ShinyNewName'})
        self.assertRedirects(response, '/profile/')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'ShinyNewName')

    def testUserDelete(self):
        response = self.client.post(reverse("dailydoodle:profile"), {"delete_account": "true"})
        # check neither the old or new name survived
        self.assertFalse(User.objects.filter(username="Killme").exists())
        self.assertFalse(User.objects.filter(username="ShinyNewName").exists())


class SubmissionsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1000 = User.objects.create_user(username='testuser500', password='testpassword1')
        self.user1001 = User.objects.create_user(username='testuser600', password='testpassword2')
        self.prompt1 = Prompt.objects.create(prompt='Prompt 1', prompt_date='2024-6-12')
        self.prompt2 = Prompt.objects.create(prompt='Prompt 2', prompt_date='2022-12-02')
        self.drawing = Drawing.objects.create(drawing_id="testdrawing69", drawing="submissions/testdrawing.jpeg", prompt=self.prompt1, user_id=self.user1000.id)
        self.drawing2 = Drawing.objects.create(drawing_id="testdrawing420", drawing="submissions/testdrawing2.jpeg", prompt=self.prompt2, user_id=self.user1000.id)
    #
    def testDisplayedPicIsUsers(self):
        self.client.login(username='testuser500', password='testpassword1')
        response = self.client.get(reverse('dailydoodle:submissions', args=['testuser500'])) #does the pic belong to user
        self.assertEqual(len(response.context['drawings']), 2) #and how many pics they have

