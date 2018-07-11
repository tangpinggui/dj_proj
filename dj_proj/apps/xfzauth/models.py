from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
# AbstractBaseUser封装了密码加密存储, PermissionsMixin封装了各种n对n关系,ex:user and permission


class UserManager(BaseUserManager):
    """
    实现User的 object功能
    """
    def _create_user(self, telephone, username, password, **kwargs):
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    # AbstractBaseUser封装了密码加密存储, PermissionsMixin封装了各种n对n关系,ex:user and permission
    重写User模型
    """
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    gender = models.IntegerField(default=0)  # 0: 未知 1：男 2：女
    data_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'  # authenticate进行验证的字段
    REQUIRED_FIELDS = ['username']  # createsuperuser命令输入的字段，django默认要求输入密码，所以不需要指定password
    EMAIL_FILED = 'email'  # 指定发送邮箱

    objects = UserManager()  # 存入model中

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username