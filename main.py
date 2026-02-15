from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
import datetime
import pytz
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
        
        # UTC time
        utc_time = datetime.datetime.now(pytz.utc)

        # Convert to IST
        ist = pytz.timezone("Asia/Kolkata")
        ist_time = utc_time.astimezone(ist)

        # Format without microseconds
        utc_formatted = utc_time.strftime("%Y-%m-%d %H:%M:%S")
        ist_formatted = ist_time.strftime("%Y-%m-%d %H:%M:%S")
        
        
        
        
        ip = request.client.host
        email = user_db[id]["email"]

        log_entry = f"{id} | {email} | {utc_formatted} | {ist_formatted} | {ip}\n"

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

                    id, email, utc_formatted, ist_formatted, ip = parts

                    rows += f"""
                    <tr>
                        <td>{id}</td>
                        <td>{email}</td>
                        <td>{utc_formatted}</td>
                        <td>{ist_formatted}</td>
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
