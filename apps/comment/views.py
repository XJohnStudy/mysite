from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType 
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def update_comment(request):
  # referer = request.META.get('HTTP_REFERER', reverse('home'))

  # # 数据检查
  # user = request.user
  # if not user.is_authenticated:
  #   return render(request, 'error.html', {'message':'用户未登录', 'redict_to':referer})

  # text = request.POST.get('text', '').strip()
  # if text == '':
  #   return render(request, 'error.html', {'message':'评论内容为空', 'redict_to':referer})

  # try:
  #   content_type = request.POST.get('content_type', '')
  #   object_id = (request.POST.get('object_id', ''))
  #   model_class = ContentType.objects.get(model=content_type).model_class()
  #   model_obj = model_class.objects.get(pk=object_id)
  # except Exception as e:
  #   return render(request, 'error.html', {'message':'评论对象不存在', 'redict_to':referer})
  
  # # 保存数据
  # comment = Comment()
  # comment.user = user
  # comment.text = text
  # comment.content_object = model_obj

  # comment.save()
  # return redirect(referer)
  referer = request.META.get('HTTP_REFERER', reverse('home'))
  comment_form = CommentForm(request.POST, user=request.user)
  data = {}
  if comment_form.is_valid():
    comment = Comment()
    comment.user = comment_form.cleaned_data['user']
    comment.text = comment_form.cleaned_data['text']
    comment.content_object = comment_form.cleaned_data['content_object']

    parent = comment_form.cleaned_data['parent']
    if not parent is None:
      comment.root = parent.root if not parent.root is None else parent
      comment.parent = parent
      comment.replay_to = parent.user

    comment.save()

    # 返回数据
    data['status'] = 'SUCCESS'
    data['username'] = comment.user.get_nickname_or_name()
    data['comment_time'] = comment.comment_time.timestamp()
    data['text'] = comment.text
    data['content_type'] = ContentType.objects.get_for_model(comment).model
    if not parent is None:
      data['reply_to'] = comment.replay_to.get_nickname_or_name()
    else:
      data['reply_to'] = ''
    data['pk'] = comment.pk
    data['root_pk'] = comment.root.pk if not comment.root is None else ''
  else:
    # return render(request, 'error.html', {'message':comment_form.errors, 'redict_to':referer})
    data['status'] = 'ERROR'
    data['message'] = list(comment_form.errors.values())[0][0]
  return JsonResponse(data)