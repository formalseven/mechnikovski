from dotenv import dotenv_values
import os
from supabase import acreate_client

config = {
    **dotenv_values(),
    **os.environ
}

if not config.get("SUPABASE_HOST"):
    raise Exception("SUPABASE_HOST wasn't loaded!")

if not config.get("SUPABASE_KEY"):
    raise Exception("SUPABASE_KEY wasn't loaded!")

class Database:
    db = None

    @staticmethod
    async def query(query_chain):
        response = await query_chain
        return response.data
        #try:
          #  response = await query_chain
         #   return response.data
        #except Exception as err:
          #  print("ERROR | Database error")
         #   print(err)
        #    raise Exception("Database error")

    @classmethod
    async def init(cls):
        cls.db = await acreate_client(config.get("SUPABASE_HOST"), config.get("SUPABASE_KEY"))
        print("Info | Database was successfully connected")