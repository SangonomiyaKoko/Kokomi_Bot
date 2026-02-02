import csv
from datetime import datetime

from ..core import STORAGE_DIR


HEADER = [
    "timestamp",   # 时间戳
    "user_id",     # 用户ID
    "platform_id", # 平台ID
    "message"      # 用户消息
]

def csv_writer(user_id: str, platform_id: str, message: str):
    now_iso = datetime.now().isoformat(timespec="seconds")
    path = STORAGE_DIR / f'msg/{now_iso[:10]}.csv'
    if not path.exists():
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            writer.writerow([now_iso, user_id, platform_id, message])
            f.flush()
    else:
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([now_iso, user_id, platform_id, message])
            f.flush()
