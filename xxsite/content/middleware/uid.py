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
        uid = self.generate_uid(request)
        self.handle_visited(request, uid)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            # 这是老用户
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            # 这是新用户
            uid = uuid.uuid4().hex
        return uid

    def handle_visited(self, request, uid):
        rd = redis.Redis(host='localhost', port=6379, db=0)
        uv_key = 'uv:' + request.path
        # 如果 flag 存在，则表明当前为重复访问，访问量不增加
        uv_flag = '.'.join([uv_key, str(date.today()), uid])

        if not rd.exists(uv_flag):
            rd.set(uv_flag, 1, 3600*24)  # set ttl to 24h
            if rd.exists(uv_key):
                rd.incr(uv_key)
            else:
                rd.set(uv_key, 1)
        return
