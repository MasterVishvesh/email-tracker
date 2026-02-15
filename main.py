from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
import datetime, pytz
import os

my_app = FastAPI()

LOG_FILE = "logs.txt"

user_db = {
    1: {"email": "shubhendray08@gmail.com"},
    2: {"email": "saurabhjalendra@gmail.com"},
    3: {"email": "sharmajay9982@gmail.com"},
    4: {"email": "kalpitmathur96@gmail.com"},
    5: {"email": "mathurvishvesh243@gmai.com"},
    
}

# TRACKING PIXEL ROUTE
@my_app.get("/view/{id}")
async def track_open(id: int, request: Request):

    if id in user_db:

        timestamp = datetime.datetime.now()
        
        
        ist = pytz.timezone("Asia/Kolkata")
        IST_timestamp = datetime.now(ist)
        
        
        ip = request.client.host
        email = user_db[id]["email"]

        log_entry = f"{id} | {email} | {timestamp} | {IST_timestamp} | {ip}\n"

        with open(LOG_FILE, "a") as f:
            f.write(log_entry)

        print("OPENED:", log_entry)

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


# DASHBOARD ROUTE
@my_app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():

    rows = ""

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:

            lines = f.readlines()

            for line in reversed(lines):

                parts = line.strip().split(" | ")

                if len(parts) == 5:

                    id, email, timestamp, IST_timestamp, ip = parts

                    rows += f"""
                    <tr>
                        <td>{id}</td>
                        <td>{email}</td>
                        <td>{timestamp}</td>
                        <td>{IST_timestamp}</td>
                        <td>{ip}</td>
                    </tr>
                    """

    html = f"""
    <html>
    <head>
        <title>Email Tracker Dashboard</title>
    </head>
    <body>

    <h2>Email Tracking Dashboard</h2>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Opened At(UST)</th>
            <th>Opened At(IST)</th>
            <th>IP</th>
        </tr>

        {rows}

    </table>

    </body>
    </html>
    """

    return HTMLResponse(content=html)
