from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from album_rater.models import Album, UserProfile, Comment

class AlbumModelTest(TestCase):
    def setUp(self):
    # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user)
        # Create a test album
        self.album = Album.objects.create(
            title="Test Album",
            uploader=self.user_profile,
            genre="rock",
        )

    def test_album_slug_generation(self):
        """
        When uploading an album, its slug should be automatically generated
        based on the title.
        """
        expected_slug = slugify(self.album.title)
        self.assertEqual(self.album.slug, expected_slug)

    def test_album_str(self):
        """
        The __str__ method of the Album model must return the album name.
        """
        self.assertEqual(str(self.album), self.album.title)


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='testpass')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_userprofile_str(self):
        """
        The __str__ method of the UserProfile model must return the username.
        """
        self.assertEqual(str(self.user_profile), self.user.username)


class CommentModelTest(TestCase):
    def setUp(self):
        # Create two users and their profiles
        self.user1 = User.objects.create_user(username='commenter1', password='pass')
        self.user2 = User.objects.create_user(username='commenter2', password='pass')
        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)
        # Create an album from the first user
        self.album = Album.objects.create(
            title="Commented Album",
            uploader=self.profile1,
            genre="pop"
        )
        # Create a comment from the second user with a rating
        self.comment = Comment.objects.create(
            text="Nice album!",
            user_profile=self.profile2,
            album=self.album,
            rating_value=8
        )

    def test_comment_str_with_rating(self):
        """
        The __str__ method of a comment should return the comment text with a rating,
        if a rating is specified.
        """
        expected = f"{self.comment.text} (Rating: {self.comment.rating_value})"
        self.assertEqual(str(self.comment), expected)

    def test_comment_str_without_rating(self):
        """
        If no rating is specified, the __str__ method should return just the comment text.
        """
        comment_no_rating = Comment.objects.create(
            text="No rating provided",
            user_profile=self.profile2,
            album=self.album
        )
        self.assertEqual(str(comment_no_rating), comment_no_rating.text)


class AlbumViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user, profile and album to test views
        self.user = User.objects.create_user(username='viewuser', password='testpass')
        self.profile = UserProfile.objects.create(user=self.user)
        self.album = Album.objects.create(
            title="View Album",
            uploader=self.profile,
            genre="jazz"
        )

    def test_index_view(self):
        """
        The main page (index) should return a 200 status and contain the text
        'Top Rated Albums' (or other key text).
        """
        response = self.client.get(reverse('album_rater:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top Rated Albums")

    def test_album_detail_view(self):
        """
        The album details page should return a 200 status and display the album title.
        """
        url = reverse('album_rater:album_detail', args=[self.album.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.album.title)

    def test_album_create_view_requires_login(self):
        """
        The album creation page requires authorization.
        Without logging in, the user should be redirected (without receiving a 200 status).
        After logging in, access should be granted.
        """
        url = reverse('album_rater:album_create')
        response = self.client.get(url)
        # If the user is not authorized, the page can redirect to login
        self.assertNotEqual(response.status_code, 200)

        # Log in and check access
        self.client.login(username='viewuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_album_view_authorization(self):
        """
        Check that the album editing page is only accessible to the user who is the album uploader.
        """
        # Create another user
        other_user = User.objects.create_user(username='otheruser', password='pass')
        UserProfile.objects.create(user=other_user)
        # Login as another user - access should be denied
        self.client.login(username='otheruser', password='pass')
        url = reverse('album_rater:edit_album', args=[self.album.slug])
        response = self.client.get(url)
        # If access is denied, there may be a redirect or an error message (not 200)
        self.assertNotEqual(response.status_code, 200)

        # Login as the album uploader
        self.client.login(username='viewuser', password='testpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_comment_addition(self):
        """
        Check that an authorized user other than the uploader can add a comment.
        Test via AJAX post (with X-Requested-With header).
        """
        # Create a new user for commenting
        commenter = User.objects.create_user(username='commentuser', password='pass')
        commenter_profile = UserProfile.objects.create(user=commenter)
        self.client.login(username='commentuser', password='pass')
        url = reverse('album_rater:album_detail', args=[self.album.slug])
        data = {
            'text': "This is a test comment.",
            'rating_value': 7,
            'submit_comment': "Submit Comment",
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        # Check that the comment has been created
        self.assertTrue(Comment.objects.filter(
            text="This is a test comment.",
            album=self.album,
            user_profile=commenter_profile
        ).exists())

    def test_prevent_comment_on_own_album(self):
        """
        The user should not be able to leave a comment under his own album.
        """
        self.client.login(username='viewuser', password='testpass')
        url = reverse('album_rater:album_detail', args=[self.album.slug])
        data = {
            'text': "I cannot comment on my own album.",
            'rating_value': 5,
            'submit_comment': "Submit Comment",
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        # In response via AJAX we expect an error message
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn("error", json_response.get("status", "").lower())
        self.assertNotIn("Comment added successfully", json_response.get("message", ""))
