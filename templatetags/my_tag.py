from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def get_obj_rows(obj, admin_class):
    """根据传入的对象生成一行记录"""
    ele = ''
    if admin_class.list_display:
        #  生成第一列的单选框，设置value为对象id
        ele += '<th><input type="checkbox" name="_selected_action" value="%s"></th>' % obj.id

        for index, column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)  # 获取字段对象

            if column_obj.choices:  # 判断当前字段是否有choices选项
                column_data = getattr(obj, 'get_%s_display' % column_name)()  # 显示当前字段信息
            else:
                column_data = getattr(obj, column_name)

            # 首个字段列设置为超链接格式
            if index == 0:
                td_ele = "<td><a href='%d/change'>%s</a></td>" % (obj.id, column_data)
            else:
                td_ele = "<td>%s</td>" % column_data

            ele += td_ele

        # 生成当前对象的一行记录
        ele = "<tr>%s</tr>" % ele

    else:
        # 默认显示对象列
        ele = "<tr><td><input type='checkbox' name='_selected_action' " \
              "value='%s'></th><td><a href='%s/change'>%s</a></td></tr>" % (obj.id, obj.id, obj)

    return mark_safe(ele)


@register.simple_tag
def bulid_filter_ele(field_name, admin_class):
    """根据传入的字段名生成过滤标签"""
    filter_ele = '<select name=%s class="form-control input_control" ' \
                 'style="width:100px;display:inline;margin-right:10px">' % field_name
    column_obj = admin_class.model._meta.get_field(field_name)

    try:
        for choice in column_obj.get_choices():
            selected = ''
            if field_name in admin_class.filter_conditions:  # 当前字段被过滤了
                if str(choice[0]) == admin_class.filter_conditions.get(field_name):  # 当前值被选中了
                    selected = 'selected'

            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option

    except AttributeError as e:
        #   由于有设置date字段过滤，所以使用.get_choices()会报错
        #   关键点是这是name='%s__get'表示大于或等于
        filter_ele = "<select name='%s__gte' class='form-control' " \
                     "style='width:100px;display:inline;margin-top:20px;margin-button:20px'>" % field_name
        #   判断是否是日期字段
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            #   自定义日期选项
            import datetime
            time_obj = datetime.datetime.today()

            time_list = [
                ['', '-----------------'],
                [time_obj, '今天'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), '一年内'],
                ['', '所有'],
            ]

            for i in time_list:
                selected = ''
                # 生成 value="2018-7-23"
                time_to_str = '' if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % field_name in admin_class.filter_conditions:  # 当前字段被过滤了
                    print('-------------gte')
                    if time_to_str == admin_class.filter_conditions.get("%s__gte" % field_name):  # 当前值被选中了
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % \
                         (time_to_str, selected, i[1])
                filter_ele += option

    filter_ele += '</select>'
    return mark_safe(filter_ele)


@register.simple_tag
def pager_list(contacts):
    pager_str = ''
    for i in range(contacts.paginator.num_pages): # 获取总页数
        active = ''

        # 若为当前页面页码，则高亮显示
        if contacts.number == i + 1:
            active = 'active'

        li_str = '<li class=%s><a href="?page=%s">%s</a></li>' \
                 % (active, i + 1, i + 1)

        pager_str += li_str
    return mark_safe(pager_str)


@register.simple_tag
def arrow(field_name, order_column):
    '''例如：name,{name:1},1'''
    symbol = ''
    if field_name in order_column:
        if str(order_column[field_name]).startswith('-'):
            symbol = 'glyphicon glyphicon-arrow-down'
        else:
            symbol = 'glyphicon glyphicon-arrow-up'
    arrow_str = '<span class="%s"></span>' % symbol
    return mark_safe(arrow_str)


@register.simple_tag
def get_sorted_column(order_column, counter, field_name):
    """判断当前字段是否是之前的排序字段，若是则取反"""
    if field_name in order_column:
        # 判断上次排列是什么顺序，本次取反 {name:-1}
        last_sort_index = order_column[field_name]
        if str(last_sort_index).startswith('-'):
            this_time_sort_index = str(last_sort_index).strip('-')
        else:
            this_time_sort_index = '-%s' % last_sort_index

        return this_time_sort_index
    else:
        return counter


@register.simple_tag
def get_filter_args(admin_class):
    """考虑到在过滤的基础上进行排序"""
    if admin_class and admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += '&%s=%s' % (k, v)
        print(ele)
        return mark_safe(ele)

    return ''


@register.simple_tag
def show_search_str(admin_class, search_str):
    """显示可以搜索的字段"""
    str = ''
    if not search_str:
        # 上一次进入后台没有进行搜索操作
        search_fields = admin_class.search_fields
        for f in search_fields:
            str += f + ', '
        return str
    return search_str  # 返回上一次搜索的数据


@register.simple_tag
def show_error_tips(input_obj, errors):
    """根据当前input对象和errors取出当前的input对应的错误信息"""
    name_attr = input_obj.name
    if name_attr in errors:
        error_msg = errors[name_attr][0]
        return mark_safe('<span class="error_msg">%s</span>' % error_msg)
    else:
        return ''


@register.simple_tag
def get_names(admin_class):
    model_class = admin_class.model
    if model_class._meta.verbose_name:
        return model_class._meta.verbose_name
    return model_class._meta.model_name


@register.simple_tag
def readonly_fields_display(admin_class, id):
    readonly_fields = admin_class.readonly_fields
    ele = ''
    obj = admin_class.model.objects.filter(id=int(id)).first()
    for field_name in readonly_fields:
        # ele += ''' <div class="form-group">
        #         <label for="inputEmail3" class="col-sm-2 control-label">%s</label>
        #         <div class="col-sm-10">
        #           <p style="height: 34px;line-height: 34px">%s</p>
        #         </div>
        #       </div>''' % (field_name, obj.__dict__.get(field_name, ''))  # 获取当前对象的字段值
        ele += ''' <div class="form-group">
                <label for="inputEmail3" class="control-label">%s</label>
                <div class="">
                  <p style="height: 34px;line-height: 34px">%s</p>
                </div>
              </div>''' % (field_name, obj.__dict__.get(field_name, ''))  # 获取当前对象的字段值

    return mark_safe(ele)


@register.simple_tag
def get_available_fields(admin_class, field_name, id, left=True):
    """获取客户的咨询课程"""
    model_class = admin_class.model
    html_str = ''
    if id:
        obj = admin_class.model.objects.filter(id=int(id)).first()  # 获取客户对象
        right_set = set(getattr(obj, field_name).all())  # 右侧为客户已咨询课程集合
    else:
        right_set = set()

    # 1、获取字段对象
    f_obj = model_class._meta.get_field(field_name)
    # 2、取出当前字段关联的 表 的所有对象信息（包含关联和不关联的）,最关键的一步,通过.rel.to获取关联的表model
    total_obj_set = set(f_obj.rel.to.objects.all())
    # 3、通过集合set取出对应表不关联的对象的集合
    left_set = total_obj_set - right_set

    # 根据传入的left参数确定要返回的是左侧还是右侧多选菜单
    if left:
        for course_obj in left_set:
            html_str += '<option value=%s >%s</option>' % (course_obj.id, course_obj)
    else:
        for course_obj in right_set:
            html_str += '<option value=%s >%s</option>' % (course_obj.id, course_obj)

    return mark_safe(html_str)


@register.simple_tag
def display_all_related_objs(obj):
    """显示要被删除对象的所有关联对象"""

    ele = "<ul>"
    for reversed_fk_obj in obj._meta.related_objects:
        # 显示与对象有关的表
        related_table_name = reversed_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name  # 查询关键字

        # 子结构开始
        ele += "<li>%s<ul> " % related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label, i._meta.model_name, i.id, i, obj)

        elif reversed_fk_obj.get_internal_type() == "OneToOneField":  # 不需要深入查找
            related_obj = getattr(obj, related_table_name, '')  # 反向查所有关联的数据
            if related_obj:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (related_obj._meta.app_label, related_obj._meta.model_name, related_obj.id, related_obj, obj)

        elif reversed_fk_obj.get_internal_type() == "ForeignKey":
            #  例如通过删除客户，那么就会删除 与此客户相关的客户跟踪记录 和 student_enroll信息
            related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change'>%s</a></li>" % (i._meta.app_label,
                                                                                 i._meta.model_name,
                                                                                 i.id, i)
                ele += display_all_related_objs(i)
        ele += "</ul></li>"

    ele += "</ul>"
    return mark_safe(ele)


@register.simple_tag
def get_label_name(admin_class,field_name):
    """获取字段名称"""
    column_obj = admin_class.model._meta.get_field(field_name)
    return column_obj.verbose_name





