import uuid
import redis

from datetime import date


USER_KEY = 'uid'
TEN_YEARS = 3600 * 24 * 365 * 10


class UidMiddleware:
    """
    用来为所有用户生成 uid，用于统计 pv 和 uv
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200:
            uid, is_new_user = self.generate_uid(request)
            self.handle_visited(request, uid, is_new_user)
            response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            # 这是老用户
            uid = request.COOKIES[USER_KEY]
            is_new_user = False
        except KeyError:
            # 这是新用户
            uid = uuid.uuid4().hex
            is_new_user = True
        return uid, is_new_user

    def handle_visited(self, request, uid, is_new_user):
        rd = redis.Redis(host='localhost', port=6379, db=0)
        today_str = str(date.today())
        uv_key_day = 'uv:' + today_str
        uv_key_all = 'uv_all'
        pv_key_page = 'pv:' + request.path
        pv_key_day = 'pv:' + today_str
        pv_key_all = 'pv_all'
        # 如果 flag 存在，则表明当前为重复访问，访问量不增加
        pv_flag = '.'.join([pv_key_page, uid])
        uv_flag = '.'.join([uv_key_day, uid])

        # 处理 pv 统计
        if not rd.exists(pv_flag):
            rd.set(pv_flag, 1, 60) # 60s
            # 页面pv
            if rd.exists(pv_key_page):
                rd.incr(pv_key_page)
            else:
                rd.set(pv_key_page, 1)
            # 日pv
            if rd.exists(pv_key_day):
                rd.incr(pv_key_day)
            else:
                rd.set(pv_key_day, 1)
            # 总pv
            if rd.exists(pv_key_all):
                rd.incr(pv_key_all)
            else:
                rd.set(pv_key_all, 1)
        
        # 处理 日uv 统计
        if not rd.exists(uv_flag):
            rd.set(uv_flag, 1, 3600*24)  # set ttl to 24h
            if rd.exists(uv_key_day):
                rd.incr(uv_key_day)
            else:
                rd.set(uv_key_day, 1)
        # 处理 总uv 统计
        if is_new_user:
            if rd.exists(uv_key_all):
                rd.incr(uv_key_all)
            else:
                rd.set(uv_key_all, 1)
        return
