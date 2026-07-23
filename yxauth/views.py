from django.http import JsonResponse
from django.shortcuts import render, redirect,reverse
import random
import string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model,login,logout
from yxauth.forms import RegisterForm,LoginForm
from yxauth.models import CaptchaModel
from django.views.decorators.http import require_http_methods
# Create your views here.
User = get_user_model()
@require_http_methods(['POST','GET'])
def zllogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user=User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request,user)

                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('账号和密码错误！')
                form.add_error('email','邮箱或密码错误！')
                return render(request,'login.html',context={'form':form})
        else:
            # ✅ 补上这个！表单验证失败时显示错误
            return render(request, 'login.html', {'form': form})

def yxlogout(request):
    logout(request)
    return redirect('/')
@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("===== 表单验证通过，准备创建用户 =====")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create_user(username=username, email=email, password=password)
            print("===== 用户创建成功，准备跳转登录 =====")
            return redirect(reverse('yxauth:login'))
        else:
            print("===== 表单验证失败 =====")
            print(form.errors)  # 关键：看终端输出什么错误
            return redirect(reverse('yxauth:register'))
def send_email_captcha(request):
    email=request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,'message':"必须传递邮箱！"})
    captcha=''.join(random.sample(string.digits, 6))
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail(subject='知了博客注册验证注册码',message=f'邮箱验证码发送成功，你的验证码是：{captcha}',recipient_list=[email],from_email=None)
    return JsonResponse({'code':200,'message':"邮箱验证码发送成功!"})