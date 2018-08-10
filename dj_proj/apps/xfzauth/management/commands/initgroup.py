# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType

from apps.news.models import News, NewsCategory, Comment
from apps.cms.models import Banners
from apps.course.models import Course, CourseOrder, Category
from django.utils.decorators import method_decorator

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 编辑组/财务组/管理员组/超级管理员
        # python manage.py initgroup
        # 编辑人员权限：编辑文章/轮播图/付费资讯/课程

        # 创建编辑组
        # model对应的app名字   !!!get_for_model not is get_for_models
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banners),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Category),
        ]
        # 添加权限
        # 查找出这些models需要的权限
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)

        # 创建权限组的名字
        editGroup = Group.objects.create(name='编辑')
        # 添加权限
        editGroup.permissions.set(edit_permissions)

        # 2.创建财务组
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder)
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        finance_group = Group.objects.create(name='财务组')
        finance_group.permissions.set(finance_permissions)

        # 3.创建管理员，拥有财务和编辑权限
        admin_permissions = edit_permissions.union(finance_permissions)
        admin_group = Group.objects.create(name='管理员')
        admin_group.permissions.set(admin_permissions)

        self.stdout.write(self.style.SUCCESS("初始化分组成功"))

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         # 编辑组/财务组/管理员组/超级管理员
#         # python manage.py initgroup
#         # 编辑人员权限：编辑文章/轮播图/付费资讯/课程
#         edit_content_types = [
#             ContentType.objects.get_for_model(News),
#             ContentType.objects.get_for_model(NewsCategory),
#             ContentType.objects.get_for_model(Banners),
#             ContentType.objects.get_for_model(Comment),
#             ContentType.objects.get_for_model(Course),
#             ContentType.objects.get_for_model(Category),
#         ]
#         edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
#         editGroup = Group.objects.create(name='编辑')
#         editGroup.permissions.set(edit_permissions)
#
#         # 2. 创建财务组：查看所有订单的权限
#         finance_content_types = [
#             ContentType.objects.get_for_model(CourseOrder),
#         ]
#         finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
#         financeGroup = Group.objects.create(name='财务')
#         financeGroup.permissions.set(finance_permissions)
#
#         # 3.创建管理员的分组：拥有财务和编辑人员的权限
#         admin_permissions = edit_permissions.union(finance_permissions)
#         adminGroup = Group.objects.create(name='管理员')
#         adminGroup.permissions.set(admin_permissions)
#
#         self.stdout.write(self.style.SUCCESS("初始化分组已经添加成功！"))

