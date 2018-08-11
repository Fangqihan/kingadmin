class BaseKingAdmin(object):
    list_display = []
    list_filter = []
    search_fields=[]
    readonly_fields=[]  # 只读字段
    filter_horizontal =[]  #
    default_actions = ['delete_selected']  # 默认action下拉框
    actions=[]

    def delete_selected(self,request,query_set):
        """删除选中的对象set"""
        query_set.delete()




