from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from ..utils import populate_initial_data


class PostViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_get_post_by_id_when_post_exists_returns_post(self):
        response: Response = self.client.get("/api/posts/2/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 2)

    def test_get_post_by_id_when_post_not_exists_returns_not_found(self):
        response: Response = self.client.get("/api/posts/666/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_by_id_when_id_is_not_int_returns_bad_request(self):
        response: Response = self.client.get("/api/posts/django/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_post_by_date_slug_when_post_exists_returns_post(self):
        response: Response = self.client.get("/api/posts/2024/5/6/post-b/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 2)

    def test_get_post_by_date_slug_when_post_not_exists_returns_not_found(self):
        response: Response = self.client.get("/api/posts/2077/7/7/cyber-post/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_posts_when_any_posts_returns_without_body_attr(self):
        response: Response = self.client.get("/api/posts/")
        posts: list[dict] = response.json()["results"]

        self.assertEqual({"body" in post for post in posts}, {False})

    def test_get_latest_posts_when_limit_is_int_returns_posts(self):
        response: Response = self.client.get("/api/posts/latest/?limit=1")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 1)

    def test_get_latest_posts_when_limit_is_not_int_returns_bad_request(self):
        response: Response = self.client.get("/api/posts/latest/?limit=one")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_posts_when_query_is_empty_returns_empty_collection(self):
        response: Response = self.client.get("/api/posts/search/?query=")

        self.assertEqual(response.json()["results"], [])

    def test_search_posts_when_query_matches_returns_posts(self):
        response: Response = self.client.get("/api/posts/search/?query=a")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 2)

    def test_get_similar_posts_when_no_similar_returns_empty_collection(self):
        response: Response = self.client.get("/api/posts/3/similar/")

        self.assertEqual(response.json()["results"], [])

    def test_get_similar_posts_when_any_similar_returns_posts(self):
        response: Response = self.client.get("/api/posts/1/similar/")
        data = response.json()["results"]
        post_count = len(data)

        self.assertEqual(post_count, 2)
        self.assertEqual(data[0]["slug"], "post-aaa")

    def test_get_similar_posts_when_limit_is_int_returns_posts(self):
        response: Response = self.client.get("/api/posts/1/similar/?limit=1")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 1)

    def test_get_similar_posts_when_limit_is_not_int_returns_bad_request(self):
        response: Response = self.client.get("/api/posts/1/similar/?limit=one")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TagViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_get_posts_by_tag_when_any_posts_returns_posts(self):
        response: Response = self.client.get("/api/tags/testing/posts/")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 3)


class CommentViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        populate_initial_data()

    def test_get_comments_by_post_id_when_any_comments_returns_comments(self):
        response: Response = self.client.get("/api/comments/?post_id=1")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 2)

    def test_get_comments_by_post_id_when_post_id_is_not_int_returns_bad_request(self):
        response: Response = self.client.get("/api/comments/?post_id=one")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comments_when_no_filter_returns_all(self):
        response: Response = self.client.get("/api/comments/")
        post_count = len(response.json()["results"])

        self.assertEqual(post_count, 3)
