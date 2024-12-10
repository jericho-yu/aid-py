import redis
from collections import defaultdict

class RedisPool:
    def __init__(self):
        self.connections = defaultdict(lambda: None)

    def get_connection(self, key):
        if self.connections[key] is None:
            self.connections[key] = redis.StrictRedis(host='localhost', port=6379, db=0)
        return self.connections[key]

    def close(self, key):
        if key in self.connections and self.connections[key] is not None:
            self.connections[key].close()
            self.connections[key] = None

    def clean(self):
        for key, conn in self.connections.items():
            if conn is not None:
                conn.close()
                self.connections[key] = None

# 示例使用
if __name__ == "__main__":
    pool = RedisPool()
    conn1 = pool.get_connection("conn1")
    conn2 = pool.get_connection("conn2")

    # 执行一些 Redis 操作
    conn1.set("key1", "value1")
    print(conn1.get("key1"))

    # 关闭单个连接
    pool.close("conn1")

    # 清理所有连接
    pool.clean()