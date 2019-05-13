from redis import StrictRedis

sr = StrictRedis()
for i in sr.lrange('number', 0, -1):  # 遍历列表
    print(i.decode(), end=' ')

print()
for i in sr.keys():  # 遍历所有键
    print(i.decode(), end=' ')

print()
sr.sadd('sport', '篮球', '足球', '击剑')  # 集合添加
for i in sr.smembers('sport'):
    print(i.decode(), end=' ')

print()

sr.zadd('hobby', 4, '语文', 5, '数学', 6, '英语')  # 有序集合
for i in sr.zrange('hobby', 0, -1):
    print(i.decode(), end=' ')


'''

def __init__(self, host='localhost', port=6379,
             db=0, password=None, socket_timeout=None,
             socket_connect_timeout=None,
             socket_keepalive=None, socket_keepalive_options=None,
             connection_pool=None, unix_socket_path=None,
             encoding='utf-8', encoding_errors='strict',
             charset=None, errors=None,
             decode_responses=False, retry_on_timeout=False,
             ssl=False, ssl_keyfile=None, ssl_certfile=None,
             ssl_cert_reqs=None, ssl_ca_certs=None,
             max_connections=None):

kwargs = {
    'db': db,
    'password': password,
    'socket_timeout': socket_timeout,
    'encoding': encoding,
    'encoding_errors': encoding_errors,
    'decode_responses': decode_responses,
    'retry_on_timeout': retry_on_timeout,
    'max_connections': max_connections
}

'''