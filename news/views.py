"""
Front-end web views for authentication, dashboards,
and role-based workflows.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import Article, Publisher, CustomUser
from .forms import UserRegisterForm, PublisherForm
from .decorators import role_required

# Create your views here.


def register_view(request):
    """Handles new user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form})


@login_required
def dashboard_redirect(request):
    """Routes users to their role-specific dashboard."""
    if request.user.role == 'editor':
        return redirect('editor_dashboard')
    elif request.user.role == 'journalist':
        return redirect('journalist_dashboard')
    else:
        return redirect('reader_subscriptions')


@login_required
@role_required(['editor'])
def editor_dashbaord(request):
    """Displays pending articles for editor review and approval."""
    articles = Article.objects.filter(approved=False)
    return render(request, 'news/editor_dashboard.html', {'articles': articles})  # noqa: E501


@login_required
@role_required(['editor'])
def approve_article(request, pk):
    """Approves an article from the editor dashboard."""
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.approved = True
        article.save()
    return redirect('editor_dashboard')


@login_required
@role_required(['journalist'])
def journalist_dashboard(request):
    """Displays articles authored by the logged-in
    journalist."""
    articles = Article.objects.filter(journalist=request.user)
    return render(request, 'news/journalist_dashboard.html', {'articles': articles})  # noqa: E501


@login_required
@role_required(['reader'])
def manage_subscriptions(request):
    """Allows readers to toggle publisher and journalist subscriptions."""
    publishers = Publisher.objects.all()
    journalists = CustomUser.objects.filter(role='journalist')

    if request.method == 'POST':
        request.user.subscriptions_publishers.set(request.POST.getlist('publishers'))  # noqa: E501
        request.user.subscriptions_journalists.set(request.POST.getlist('journalists'))  # noqa: E501
        return redirect('reader_subscriptions')

    return render(request, 'news/subscriptions.html', {
        'publishers': publishers,
        'journalists': journalists,
    })


@login_required
def manage_publishers(request):
    """Allows creation and management of publishers."""
    if request.user.role not in ['editor', 'journalist']:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_publishers')
    else:
        form = PublisherForm()

    publishers = Publisher.objects.all()
    return render(request, 'news/publisher_management.html', {
        'form': form,
        'publishers': publishers
    })
