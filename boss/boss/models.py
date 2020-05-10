class ProxyModel(object):   # 将代理分解，有端口号，有过期时间
    def  __init__(self,data):   # 这个就是将其中的ip提取出来，形成一个ip地址
        self.ip=data['ip']     # ip地址
        self.port=data['port']   # 端口
        self.expire_time=data['expire_time']
        self.proxy="https://{}:{}".format(self.ip,self.port)


