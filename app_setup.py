from django import conf


def kingadmin_auto_discover():
    """导入app.kingadmin 模块文件，即为kingadmin.py"""
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.kingadmin'%app_name)
            print(mod.kingadmin)
        except ImportError:
            pass





