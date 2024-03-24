from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Article, Comment
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



@login_required
def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')
    return render(request, 'app/index.html', {'latest_article_list': latest_article_list})


@login_required
def detail(request, article_id):
    try:
      a = Article.objects.get(id = article_id)
    except:
      raise Http404("Не знайдено")

    latest_comments_list = a.comment_set.order_by('-id')
    return render(request, 'app/detail.html', {'article': a, 'latest_comments_list':latest_comments_list})


@login_required
def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404("Стаття не знайдена")

    if request.method == 'POST':
        comment_text = request.POST.get('text', '')
        Comment.objects.create(article=a, author=request.user, comment_text=comment_text)
        return HttpResponseRedirect(reverse('detail', args=(a.id,)))
    else:
        pass


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        raise Http404("Ви не маєте права редагувати цей коментар")

    if request.method == 'POST':
        comment_text = request.POST.get('text', '')
        comment.comment_text = comment_text
        comment.save()
        return HttpResponseRedirect(reverse('detail', args=(comment.article.id,)))
    return render(request, 'app/edit_comment.html', {'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        raise Http404("Ви не маєте права видалити цей коментар")

    if request.method == 'POST':
        article_id = comment.article.id
        comment.delete()
        return HttpResponseRedirect(reverse('detail', args=(article_id,)))
    return render(request, 'app/delete_confirm.html', {'comment': comment})


@login_required
def about(request):
    return render(request, 'app/about.html')


@login_required
def sect(request):
    return render(request, 'app/sect.html')


@login_required
def profile(request):
  return render(request, 'app/profile.html')