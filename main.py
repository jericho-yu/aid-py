from redisPool.redis_pool import RedisPool
from filesystem.filesystem import FileSystem

# 示例使用
if __name__ == "__main__":
    redis_pool = RedisPool("./redisPool/redis.yaml")
    redis_pool.get_connection("auth").set("key1","value1")
    print(redis_pool.get_connection("auth").get("key1"))

    # 关闭单个连接
    redis_pool.close("auth")

    # 清理所有连接
    redis_pool.clean()
