import datetime

from django.shortcuts import render, redirect
from django.db.models import Count, Case, When, IntegerField
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Writer, Article
from .forms import NewArticleForm, EditArticleForm


def editor_required(login_url="blog-dashboard"):
    """
    Custom decorator for requiring editor access
    """
    return user_passes_test(lambda u: u.is_editor, login_url=login_url)


def dashboard(request):
    """
    Dashboard view, shows a list of all writers,
    along with a number of their articles,
    and a number of their articles in the last 30 days.
    """
    # A time delta, used to determine how many last
    # days worth of articles are we quering for
    timedelta = datetime.datetime.today()-datetime.timedelta(days=30)

    # The single query we're returning to the view
    queryset = Writer.objects.all().\
        annotate(count_written=Count("written")).\
        order_by("count_written").\
        annotate(
            last_30=Count(
                Case(
                    When(
                        written__created_at__gte=timedelta, then=1
                    ),
                    output_field=IntegerField()
                )
            )
        )

    context = {
        "queryset": queryset
    }
    return render(request, "blog/dashboard.html", context)


@login_required(login_url="blog-dashboard")
def article_detail(request, article_id):
    """
    Article detailed view, allows editing of the articles
    for any logged in writer.
    """
    article = Article.objects.select_related('written_by').get(pk=article_id)
    form = EditArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        edited_article = form.save(commit=False)
        edited_article.edited_by.add(request.user)
        edited_article.save()

        return redirect("blog-article-detail", article_id=article_id)

    context = {
        "article": article,
        "form": form
    }
    return render(request, "blog/article_detail.html", context)


@login_required(login_url="blog-dashboard")
def create_article(request):
    """
    Simple form view for creating a new Article.
    Requires a logged in user.
    """
    form = NewArticleForm(request.POST or None)
    if form.is_valid():
        new_article = form.save(commit=False)
        new_article.written_by = request.user
        new_article.save()

        return redirect("blog-create-article")

    context = {
        "form": form
    }
    return render(request, "blog/create_article.html", context)


@login_required(login_url="blog-dashboard")
@editor_required()
def article_approval(request):
    """
    A view that allows editors to approve/reject
    new articles.
    """
    fresh_articles = Article.objects.select_related("written_by").\
                    filter(status=None)

    if request.method == "POST":
        article_id = request.POST["article_id"]
        article = Article.objects.get(pk=article_id)
        if "approve" in request.POST:
            article.status = True
        elif "reject" in request.POST:
            article.status = False
        article.reviewed_by = request.user
        article.save()

    context = {
        "fresh_articles": fresh_articles
    }
    return render(request, "blog/article_approval.html", context)


@login_required(login_url="blog-dashboard")
@editor_required()
def articles_reviewed(request):
    """
    A view that shows editors the articles
    they reviewed.
    """
    reviewed_articles = Article.objects.select_related("written_by")\
                        .filter(reviewed_by=request.user)

    context = {
        "reviewed_articles": reviewed_articles
    }
    return render(request, "blog/articles_reviewed.html", context)
