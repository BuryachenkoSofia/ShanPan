from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Article, Comment, User, UserMessage
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    user_messages = UserMessage.objects.filter(user=request.user).order_by('-created_at')
    users = User.objects.all()
    return render(request, 'app/profile.html', {'users': users, 'user_messages': user_messages})


@login_required
def add_respan(request):
    users = User.objects.all()  # Отримати всіх користувачів
    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        respan_amount = request.POST.get('respan_amount')
        try:
            selected_user = User.objects.get(id=selected_user_id)
        except ObjectDoesNotExist:
            messages.error(request, f'Користувача з id {selected_user_id} не існує.')
            return redirect('profile')
        
        respan_amount = int(respan_amount)
    
        selected_user.money += respan_amount
        selected_user.save()
        comment = request.POST.get('comment', '').strip()  
        message = f'Вам нараховано {respan_amount} респанів.'
        if comment: 
            message += f' Коментар: {comment}'
        UserMessage.objects.create(user=selected_user, message=message)
        return redirect('profile')
    
    return render(request, 'app/profile.html', {'users': users})


@login_required
def remove_respan(request):
    users = User.objects.all()  # Отримати всіх користувачів
    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        respan_amount = request.POST.get('respan_amount')
        try:
            selected_user = User.objects.get(id=selected_user_id)
        except ObjectDoesNotExist:
            messages.error(request, f'Користувача з id {selected_user_id} не існує.')
            return redirect('profile')
        
        respan_amount = int(respan_amount)
        if selected_user.money - respan_amount < 0:
            messages.error(request, 'Недостатньо респанів для видалення.')
            return redirect('profile')
        
        selected_user.money -= respan_amount
        selected_user.save()
        comment = request.POST.get('comment', '').strip()  
        message = f'Вам нараховано {respan_amount} респанів.'
        if comment: 
            message += f' Коментар: {comment}'
        UserMessage.objects.create(user=selected_user, message=message)
        return redirect('profile')
    
    return render(request, 'app/profile.html', {'users': users})