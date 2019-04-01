from django.core.cache import cache

from lib.sms import send_sms
from lib.http import render_json
from common import keys
from common import errors
from user.models import User
# Create your views here.


def submit_phone(request):
    """先提交手机号码"""
    phonenum = request.POST.get('phone')
    # 拿到手机号码应该去发短信.
    send_sms(phonenum)
    return render_json(data=None)


def submit_vcode(request):
    """获取验证登录注册"""
    phonenum = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    # 判断发送的短信验证和获取的短信验证码是否一致.
    # 从缓存中取出验证码
    cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
    print(cached_vcode)
    if vcode == cached_vcode:
        # 登录或注册
        # 得判断是登录还是注册.
        # 如果能从数据库中查询到这个用户,那么就说明注册过.说明操作是 登录操作.
        # try:
        #     user = User.objects.get(phonenum=phonenum)
        # except User.DoesNotExist:
        #     # 注册
        #     user = User.objects.create(phonenum=phonenum)

        # 简化一下
        user, created = User.objects.get_or_create(phonenum=phonenum, nickname=phonenum)
        # 登录
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(data='验证码错误', code=errors.VCODE_ERR)


def get_profile(request):
    """"获取个人资料"""
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render_json(user.profile.to_dict())


def edit_profile(request):
    """修改个人资料"""
    return


def upload_avatar(request):
    """头像上传"""
    return
