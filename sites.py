from king_admin.base_king_admin import BaseKingAdmin


class AdminSite(object):
    def __init__(self):
        # 启动则生成全局字典,只是实例化一次
        self.enable_admins = {}

    def register(self, model_class, admin_class=BaseKingAdmin):
        # 获取注册表的 app名（字符串）
        app_name = model_class._meta.app_label

        # 获取注册表的 model名(字符串)
        model_name = model_class._meta.model_name

        if not admin_class:
            # 为了避免多个model共享同一个BaseKingAdmin内存对象
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()

        # 将 admin_class 与 model_class 关联起来
        admin_class.model = model_class

        if app_name not in self.enable_admins:
            self.enable_admins[app_name] = {}

        self.enable_admins[app_name][model_name] = admin_class


# 实例化，就可以调用register方法
site = AdminSite()
