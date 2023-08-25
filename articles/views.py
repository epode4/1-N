from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles
    }

    return render(request, 'index.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    comment_form = CommentForm()
    
    # comment 목록 조회
    # 첫번째 방법
    # comment_list = Comment.objects.filter(article=article)

    # 두번째 방법
    # comment_list = article.comment_set.all()


    # 세번째 방법 : comment_list 없음 + detail.html 에서 직접 article.comment_set.all 사용
    context = {
        'article': article,
        'comment_form': comment_form,
        # 'comment_list': comment_list
    }

    return render(request, 'detail.html', context)

def comment_create(request, article_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)

        # 첫번째 방법
        # article = Article.objects.get(id=article_id)
        # comment.article = article

        # 두번째 방법
        comment.article_id = article_id

        comment.save()

        return redirect('articles:detail', id=article_id)


def comment_delete(request, article_id, id):
    comment = Comment.objects.get(id=id)

    comment.delete()

    return redirect('articles:detail', id=article_id)