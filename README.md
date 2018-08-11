# kingadmin
自开发admin后台

将文件下载并放在项目路径下即可。

## 配置步骤
#### 1、setting.py

```python
# step1：添加app
INSTALLED_APPS = [
    ...
    'king_admin',
]


# step2：添加模板路径
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # 手动添加此路径
            os.path.join(BASE_DIR, 'king_admin','templates'),
        ]
        ...
        

# step3：添加静态文件路径
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'king_admin/static'),
]
```

---


#### 2、kingadmin.py
在每个app下创建`kingadmin.py`文件，注册model：

```python
from king_admin.sites import site
from app01 import models
from king_admin.base_king_admin import BaseKingAdmin


class PubliserAdmin(BaseKingAdmin):
    
    list_display = []
    
    # 1、无法搜索外键字段，确定外键显示字段过程比较繁琐
    # 2、不能搜索 Int 等非Char类型字段
    search_fields = ['title'] 
    
    # 只能搜索外键字段
    list_filter = ['publisher','authors']
    
    readonly_fields=[]


site.register(models.Book,BookAdmin)
```

---


## 版本限制
只适用于 django1.x 版本，由于路由匹配的原因。

