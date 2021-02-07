from django.test import TestCase
from django.urls import reverse

from blog.models import Writer, Article


class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Writer.objects.create(username="TestWriter1", name="TestWriter1")
        Writer.objects.create(username="TestWriter2", name="TestWriter2")

        articles = []
        for i in range(10):
            articles.append(
                Article(
                    title=f"Article{i}",
                    content=f"Article{i}",
                    written_by=Writer.objects.get(pk=1)
                )
            )
        for i in range(20):
            articles.append(
                Article(
                    title=f"Article{i}",
                    content=f"Article{i}",
                    written_by=Writer.objects.get(pk=2)
                )
            )
        Article.objects.bulk_create(articles)

    def test_view_url_exists(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse("blog-dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("blog-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/dashboard.html')

    def test_queryset_correct_size(self):
        response = self.client.get(reverse("blog-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("queryset" in response.context)
        self.assertTrue(len(response.context["queryset"]) == 2)

    def test_queryset_returns_correct_amount_of_articles(self):
        response = self.client.get(reverse("blog-dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("queryset" in response.context)

        author1 = response.context["queryset"][0]
        author2 = response.context["queryset"][1]
        self.assertEqual(author1.count_written, 10)
        self.assertEqual(author2.count_written, 20)
        self.assertEqual(author1.last_30, 10)
        self.assertEqual(author2.last_30, 20)
