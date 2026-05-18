import os
import sys
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from supabase import create_client, Client

load_dotenv(find_dotenv(usecwd=True))


@lru_cache(maxsize=1)
def client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        sys.exit("SUPABASE_URL and SUPABASE_KEY must be set (see .env.example)")
    return create_client(url, key)
