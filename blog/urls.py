from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="blog-dashboard"),
    path(
        "article/<int:article_id>",
        views.article_detail,
        name="blog-article-detail"
        ),
    path(
        "article-approval",
        views.article_approval,
        name="blog-article-approval"
        ),
    path(
        "articles-reviewed",
        views.articles_reviewed,
        name="blog-articles-reviewed"
        ),
    path(
        "create-article",
        views.create_article,
        name="blog-create-article"
        )
]
