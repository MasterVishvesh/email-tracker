from fastapi import FastAPI, Request
from fastapi.responses import Response
import datetime

my_app = FastAPI()

LOG_FILE = "logs.txt"

user_db = {
    1: {"email": "shubhendray08@gmail.com"},
    2: {"email": "saurabhjalendra@gmail.com"},
    3: {"email": "sharmajay9982@gmail.com"},
    4: {"email": "kalpitmathur96@gmail.com"},
}

@my_app.get("/view/{id}")
async def track_open(id: int, request: Request):

    if id in user_db:

        timestamp = datetime.datetime.now()
        ip = request.client.host
        email = user_db[id]["email"]

        log_entry = f"{id} | {email} | {timestamp} | {ip}\n"

        with open(LOG_FILE, "a") as f:
            f.write(log_entry)

        print("OPENED:", log_entry)

    # Proper transparent GIF
    pixel = (
        b"GIF89a"
        b"\x01\x00\x01\x00"
        b"\x80\x00\x00"
        b"\x00\x00\x00"
        b"\xff\xff\xff"
        b"!\xf9\x04\x01\x00\x00\x00\x00"
        b",\x00\x00\x00\x00\x01\x00\x01\x00\x00"
        b"\x02\x02D\x01\x00;"
    )

    return Response(
        content=pixel,
        media_type="image/gif",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
