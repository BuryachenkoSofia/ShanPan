from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Article
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
      a = Article.objects.get(id = article_id)
    except:
      raise Http404("Не знайдено")

    # a.comment_set.create(request.user.username, comment_text = request.POST['text'])
    # return HttpResponseRedirect(reverse('detail', args = (a.id,)))

    author_name = request.user.username
    comment_text = request.POST.get('text', '')
    a.comment_set.create(author_name=author_name, comment_text=comment_text)
    return HttpResponseRedirect(reverse('detail', args=(a.id,)))


@login_required
def about(request):
    return render(request, 'app/about.html')


@login_required
def sect(request):
    return render(request, 'app/sect.html')


@login_required
def profile(request):
  return render(request, 'app/profile.html')