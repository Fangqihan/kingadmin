from django.conf.urls import url
from king_admin import views

urlpatterns = [
    url(r'^$', views.home_page, name='king_admin_homepage'),  # kingadmin主页面
    url(r'^admin_login/$', views.admin_login, name='king_admin_login'),
    url(r'^admin_logout/$', views.admin_logout, name='king_admin_logout'),

    url(r'^(\w+)/$', views.app_page, name='kingadmin_app_page'),  # app的model页面

    url(r'^(\w+)/(\w+)/$', views.model_obj_list, name='model_obj_list'),  #　model对象列表页
    url(r'^(\w+)/(\w+)/(\d+)/change$', views.change_obj, name='change_obj'),  # 修改对象数据页面
    url(r'^(\w+)/(\w+)/(\d+)/delete$', views.delete_obj, name='delete_obj'),  # 删除对象
    url(r'^(\w+)/(\w+)/add$', views.add_obj, name='add_obj'),  # 新增对象
]





