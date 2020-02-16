import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog


def get_seven_days_hot_bogs():
  today = timezone.now().date()
  date = today - datetime.timedelta(days=7)
  blogs = Blog.objects\
              .filter(read_details__date__lt=today, read_details__date__gte=date)\
              .values('id', 'title')\
              .annotate(read_num_sum=Sum('read_details__read_num'))\
              .order_by('-read_num_sum')
  return blogs[:7]

def home(request):
  context = {}
  blog_content_type = ContentType.objects.get_for_model(Blog)
  read_nums, dates = get_seven_days_read_data(blog_content_type)
  today_hot_data = get_today_hot_data(blog_content_type)
  yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
  # seven_days_hot_data = get_seven_days_hot_data(blog_content_type)

  # 获取7天热门博客的缓存数据
  seven_days_hot_bogs = cache.get('seven_days_hot_bogs')
  if seven_days_hot_bogs is None:
    seven_days_hot_bogs = get_seven_days_hot_bogs()
    cache.set('seven_days_hot_bogs', seven_days_hot_bogs, 3600)
  #   print('cal')
  # else:
  #   print('cache')

  context['read_nums'] = read_nums
  context['dates'] = dates
  context['today_hot_data'] = today_hot_data
  context['yesterday_hot_data'] = yesterday_hot_data
  context['seven_days_hot_blog'] = seven_days_hot_bogs
  return render(request, 'home.html', context)

# def login(request):
#   # username = request.POST.get('username', '')
#   # password = request.POST.get('password', '')
#   # user = auth.authenticate(request, username=username, password=password)
#   # # referer = request.META.get('HTTP_REFERER', '/')
#   # referer = request.META.get('HTTP_REFERER', reverse('home'))
#   # if user is not None:
#   #   auth.login(request, user)
#   #   return redirect(referer)
#   # else:
#   #   return render(request, 'error.html', {'message':'用户名或密码不正确！'})
#   if request.method == 'POST':
#     login_form = LoginForm(request.POST)
#     if login_form.is_valid():
#       # username = login_form.cleaned_data['username']
#       # password = login_form.cleaned_data['password']
#       # user = auth.authenticate(request, username=username, password=password)
#       # if user is not None:
#         user = login_form.cleaned_data['user']
#         auth.login(request, user)
#         return redirect(request.GET.get('from', reverse('home')))
#       # else:
#       #   login_form.add_error(None, '用户名或密码不正确')
#       #   context = {}
#       #   context['login_form'] = login_form
#       #   return render(request, 'login.html', context)
#     # else:
#     #   context = {}
#     #   context['login_form'] = login_form
#     #   return render(request, 'login.html', context)
#   else:
#     login_form = LoginForm()
#   context = {}
#   context['login_form'] = login_form
#   return render(request, 'login.html', context)

# def login_for_modal(request):
#   login_form = LoginForm(request.POST)
#   data = {}
#   if login_form.is_valid():
#     user = login_form.cleaned_data['user']
#     auth.login(request, user)
#     data['status'] = 'SUCCESS'
#   else:
#     data['status'] = 'ERROR'
#   return JsonResponse(data)
    
# def register(request):
#   if request.method == 'POST':
#     reg_form = RegForm(request.POST)
#     if reg_form.is_valid():
#       username = reg_form.cleaned_data['username']
#       email = reg_form.cleaned_data['email']
#       password = reg_form.cleaned_data['password']
#       # 创建用户
#       user = User.objects.create_user(username, email, password)
#       user.save()
    
#       # user = User()
#       # user.username = username
#       # user.email = email
#       # user.set_password(password)
#       # user.save()
#       # 登录用户
#       user = auth.authenticate(username=username, password=password)
#       auth.login(request, user)
#       return redirect(request.GET.get('from', reverse('home')))
#   else:
#     reg_form = RegForm()
#   context = {}
#   context['reg_form'] = reg_form
#   return render(request, 'register.html', context)

# def logout(request):
#   auth.logout(request)
#   return redirect(request.GET.get('from', reverse('home')))

# def user_info(request):
  # context = {}
  # return render(request, 'user_info.html', context)