from django.forms import ModelForm


def create_model_form(admin_class,add=False):

    class Meta:
        model = admin_class.model  # 指定类
        fields = '__all__'  # 指定字段
        exclude = admin_class.readonly_fields  # 排除指定的字段，也不会生成form对象
        if add:
            exclude=[]

    def __new__(cls,*args,**kwargs):
        # 方法2：在实例化类对象（model_form()）的时候给input框增加样式
        print(cls.base_fields)  # 当地类的所有字段
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs.update({'class':'form-control'})  #　给当前字段对象增加样式

            if field_obj.label=='Content':
                # 设置textarea样式
                field_obj.widget.attrs.update({'cols':'100','rows':'10','class':'form-control'})

            # 筛选出教师角色为教师的对象
            if field_name == 'teachers':
                field_obj._queryset = field_obj._queryset.filter(role__title='讲师')

            if field_name == 'consultant':
                field_obj._queryset = field_obj._queryset.filter(role__title='销售')
                pass

            if field_name in admin_class.readonly_fields:
                # 但是设置为disabled后，form表单不会提交数据
                if add:
                    pass
                else:
                    field_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta,'__new__':__new__})
    return dynamic_form



