import uuid
import time
import random
import json
import logging
import aiohttp
import asyncio
import string
from datetime import datetime


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_widget_data():
    return json.dumps({
        "jvqtrgQngn": {
            "oq": f"{random.randint(1000, 4000)}:{random.randint(500, 2000)}:{random.randint(1000, 4000)}:{random.randint(500, 2000)}:{random.randint(1000, 4000)}:{random.randint(500, 2000)}",
            "wfi": "flap-1",
            "ji": "2.3.1",
            "oc": random_string(16),
            "fe": f"{random.randint(1080, 2160)}x{random.randint(1920, 3840)} 24",
            "qvqgm": str(random.randint(-500, 500)),
            "jxe": random.randint(100000, 999999),
            "syi": "snyfr",
            "si": "si,btt,zc4,jroz",
            "sn": "sn,zcrt,btt,jni",
            "us": random_string(16),
            "cy": "IR",
            "sg": json.dumps({"zgc": 0, "gf": "snyfr", "gr": "snyfr"}),
            "sp": json.dumps({"gp": "gehr", "ap": "gehr"}),
            "sf": "gehr",
            "jt": random_string(20),
            "sz": random_string(20),
            "vce": f"apvc,0,{random_string(6)},2,1;fb,0;fg,1,login,12,button,0,,0;zz,n5q,429,2on,;zp,349,3pn,2r8,button;",
            "vp": "",
            "ns": "",
            "qvg": ""
        }
    })


def generate_fake_json():
    session_id = f"{uuid.uuid4()}_{int(time.time() * 1000)}"
    duid = ''.join(random.choices(string.hexdigits.lower(), k=64))
    client_id = str(uuid.uuid4())
    
    return {
        "authentication_type": "password",
        "username": "esi.gamer@yahoo.com",
        "password": "Esi8551843#@",
        "dfp_data": [
            {
                "metadata": {"profiling_completed": True},
                "session_id": session_id,
                "vendor_id": "V001"
            }
        ],
        "widget_data": generate_widget_data(),
        "session_id": str(uuid.uuid4()),
        "duid": duid,
        "client_id": client_id
    }
