from bot.states.redis_client import redis_client

class BasicStateManager:
    def __init__(self, name):
        self.name = name

    async def set(self, id, data):
        await redis_client.hset(f"{self.name}:::{id}", mapping=data)

    async def get(self, id):
        return await redis_client.hgetall(f"{self.name}:::{id}")

    async def hincrby(self, id, field: str, num: int):
        return await redis_client.hincrby(f"{self.name}:::{id}", field, num)

    async def delete(self, id):
        await redis_client.delete(f"{self.name}:::{id}")

    async def exists(self, id):
            await redis_client.exists(f"{self.name}:::{id}")