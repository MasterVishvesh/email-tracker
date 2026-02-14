from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
import datetime
import os 

my_app = FastAPI()

LOG_FILE = "logs.txt"
# Example users with unique numeric IDs
user_db = {
    1: {"email": "shubhendray08@gmail.com", "opened": False},
    2: {"email": "saurabhjalendra@gmail.com", "opened": False},
    3: {"email": "sharmajay9982@gmail.com", "opened": False},
    4: {"email": "kalpitmathur96@gmail.com", "opened": False},

}



@my_app.get("/view/{id}")
async def track_click(id: int, request: Request):
    if id in user_db:
        user_db[id]["opened"] = True
        user_db[id]["opened_at"] = str(datetime.datetime.now())
        user_db[id]["ip"] = request.client.host

        # Append log to a file
        log_entry = f"{id} | {user_db[id]['email']} | {user_db[id]['opened_at']} | {user_db[id]['ip']}\n"
        with open("logs.txt", "a") as f:
            f.write(log_entry)
            
        print("OPENED:", log_entry)

    # Return a 1x1 transparent GIF as a tracking pixel
    pixel = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return Response(content=pixel, media_type="image/gif")


# ---------------- DASHBOARD ROUTE ----------------
@my_app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    logs_html = ""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                # Build HTML table
                logs_html += "<table border='1' style='border-collapse: collapse; width: 80%;'>"
                logs_html += "<tr><th>ID</th><th>Email</th><th>Opened At</th><th>IP</th></tr>"
                for line in lines[::-1]:  # newest first
                    parts = line.strip().split(" | ")
                    if len(parts) == 4:
                        logs_html += f"<tr><td>{parts[0]}</td><td>{parts[1]}</td><td>{parts[2]}</td><td>{parts[3]}</td></tr>"
                logs_html += "</table>"
            else:
                logs_html = "<p>No logs yet.</p>"
    else:
        logs_html = "<p>No logs file found.</p>"

    html_content = f"""
    <html>
        <head>
            <title>Tracking Dashboard</title>
        </head>
        <body>
            <h2>PDF / Email Tracking Dashboard</h2>
            {logs_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
