from typing import Any
import redis
import yaml
from dict.any_dict import AnyDict


class RedisPool:
    def __init__(self, filename: str):
        """
        初始化 Redis 连接池。
        参数:
        filename (str): 配置文件的路径。
        功能:
        从指定的配置文件中加载 Redis 连接池的配置，并创建相应的 Redis 连接实例。
        配置文件格式:
        配置文件应为 YAML 格式，包含以下字段:
        - host: Redis 服务器的主机名或 IP 地址。
        - port: Redis 服务器的端口号。
        - password: Redis 服务器的密码。
        - pool: 一个包含多个连接配置的列表，每个连接配置应包含以下字段:
            - key: 连接的键名。
            - dbNum: 连接的数据库编号。
        """
        with open(filename, "r") as file:
            self.config = yaml.safe_load(file)

        self.connections = AnyDict.make()

        for c in self.config["pool"]:
            self.connections.set(
                c["key"],
                redis.StrictRedis(
                    host=self.config["host"],
                    port=self.config["port"],
                    db=c["dbNum"],
                    password=self.config["password"],
                ),
            )

    def _get_key(self, conn_name: str, key: str) -> str:
        return f'{self.config["prefix"]}:{key}'

    def get_connection(self, conn_name: str) -> redis.StrictRedis:
        """
        获取指定连接名称的 Redis 连接实例。
        参数:
            conn_name (str): 连接名称。
        返回:
            redis.StrictRedis: 与给定连接名称关联的 Redis 连接实例。
        """
        return self.connections.get(conn_name)

    def close(self, conn_name:str):
        """
        关闭指定名称的连接。

        参数:
        conn_name (str): 要关闭的连接名称。

        如果连接存在，则关闭连接并从连接池中移除。
        """
        if self.connections.get(conn_name) is not None:
            self.connections.get(conn_name).close()
            self.connections.destroy_by_key(conn_name)

    def clean(self):
        """
        清理连接池中的所有连接。

        遍历连接池中的所有键，关闭每个键对应的连接。
        """
        for k in self.connections.get_keys():
            self.connections.get(k).close()

    def set(self, conn_name: str, key: str, value: Any) -> "RedisPool":
        """
        设置指定连接名称的键值对。
        参数:
            conn_name (str): 连接名称。
            key (str): 键。
            value (Any): 值。
        返回:
            RedisPool: 返回当前的 RedisPool 实例。
        """
        connection = self.connections.get(conn_name)
        if connection is not None:
            connection.set(self._get_key(key), value)

        return self

    def get(self,conn_name:str, key: str) -> Any:
        """
        从Redis连接池中检索值。
        参数:
            conn_name (str): 要使用的连接名称。
            key (str): 要检索值的键。
        返回:
            Any: 与给定键关联的值，如果连接不存在则返回None。
        """
        connection = self.connections.get(conn_name)
        if connection is not None:
            return connection.get(self._get_key(key))
        
        return None


# 示例使用
if __name__ == "__main__":
    redis_pool = RedisPool("./redisPool/redis.yaml")
    redis_pool.get_connection("auth").set("key1","value1")
    print(redis_pool.get_connection("auth").get("key1"))

    # 关闭单个连接
    redis_pool.close("auth")

    # 清理所有连接
    redis_pool.clean()