from django.test import TestCase

from blog.models import Writer, Article


class WriterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Writer.objects.create(username="TestWriter1", name="TestWriter1")

    def test_default_is_editor_false(self):
        writer = Writer.objects.get(pk=1)
        self.assertEqual(writer.is_editor, False)

    def test_name_max_length(self):
        writer = Writer.objects.get(pk=1)
        max_length = writer._meta.get_field("name").max_length
        self.assertEqual(max_length, 24)


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        writer = Writer.objects.create(
                                    username="TestWriter1",
                                    name="TestWriter1")
        Article.objects.create(
                            title="TestArticle1",
                            content="TestArticle1",
                            written_by=writer)

    def test_title_max_length(self):
        article = Article.objects.get(pk=1)
        max_length = article._meta.get_field("title").max_length
        self.assertEqual(max_length, 64)
