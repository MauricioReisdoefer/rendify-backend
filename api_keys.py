import os
from dotenv import load_dotenv

load_dotenv()  
API_KEYS = [
    os.getenv("TWELVEDATA_API_KEY"),
    os.getenv("TWELVEDATA_API_KEY2"),
    os.getenv("TWELVEDATA_API_KEY3"),
    os.getenv("TWELVEDATA_API_KEY4"),
    os.getenv("TWELVEDATA_API_KEY5"),
    os.getenv("TWELVEDATA_API_KEY6"),
    os.getenv("TWELVEDATA_API_KEY7"),
    os.getenv("TWELVEDATA_API_KEY8")
]

API_KEYS = [k for k in API_KEYS if k]

import itertools
from twelvedata import TDClient

api_cycle = itertools.cycle(API_KEYS)

def get_td_client():
    """Retorna um TDClient com a próxima API key da lista"""
    api_key = next(api_cycle)
    return TDClient(apikey=api_key)