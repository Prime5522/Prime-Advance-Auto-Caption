from os import environ, getenv
import re
import os

id_pattern = re.compile(r"^.\d+$")


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


ADMIN = int(getenv("ADMIN", "5926160191"))
SILICON_PIC = os.environ.get("SILICON_PIC", "https://telegra.ph/file/21a8e96b45cd6ac4d3da6.jpg")
API_ID = int(getenv("API_ID", "27148454"))
API_HASH = str(getenv("API_HASH", "f668c20d77d1a8feee31afdc810f8ac4"))
BOT_TOKEN = str(getenv("BOT_TOKEN", "7685426065:AAE5z1ahKLkfRyMxXo3x_AiBUXu_WqHuw3M"))
FORCE_SUB = os.environ.get("FORCE_SUB", "-1002245813234") 
MONGO_DB = str(getenv("MONGO_DB", "mongodb+srv://vogaje4812:zSXRd584CxoK8wEQ@cluster0.tnwxw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",))
DEF_CAP = str(
    getenv(
        "DEF_CAP",
        "<b>File Name:- `{file_name}`\n\n{file_size}</b>",
    )
)
