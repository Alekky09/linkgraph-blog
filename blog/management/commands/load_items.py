from django.core.management.base import BaseCommand
from blog.models import Writer, Article


class Command(BaseCommand):
    """
    This command is for bulk filling up the database with
    5 Writers and 100 Articles (20 for each Writer).
    Articles will be assigned to Writers randomly.
    """

    def handle(self, *args, **options):
        Article.objects.all().delete()
        # Writer.objects.all().delete()

        # Create 5 writers
        writers = [Writer(
                        name=f"Writer{index}",
                        username=f"Writer{index}") for index in range(1, 6)]
        Writer.objects.bulk_create(writers)

        # Create 20 articles for each writer
        counter = 0
        articles = []
        for writer in Writer.objects.all():
            for i in range(20):
                counter += 1
                articles.append(
                    Article(
                        title=f"Article{counter}",
                        content=f"Article{counter}",
                        written_by=Writer.objects.order_by('?').first()
                    )
                )

        Article.objects.bulk_create(articles)
