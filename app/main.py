from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta

app = FastAPI()

def get_weekend_dates(start_date: datetime, end_date: datetime):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 5:  # Saturday
            dates.append(current_date.strftime("%A, %d %B %Y"))
        elif current_date.weekday() == 6:  # Sunday
            dates.append(current_date.strftime("%A, %d %B %Y"))
        current_date += timedelta(days=1)
    return dates

@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <html>
        <head>
            <title>Identify Weekends</title>
            <script>
                async function submitForm(event) {
                    event.preventDefault();
                    const start_date = document.getElementById('start_date').value;
                    const end_date = document.getElementById('end_date').value;

                    const response = await fetch("/submit", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        body: `start_date=${start_date}&end_date=${end_date}`,
                    });

                    const result = await response.text();
                    document.getElementById('result').innerHTML = result;
                }
            </script>

        </head>
        <body>
            <h2>Input:</h2>
            <form onsubmit="submitForm(event)">
                <label for="start_date">Tanggal Awal:</label>
                <input type="date" id="start_date" name="start_date"><br><br>
                <label for="end_date">Tanggal Akhir:</label>
                <input type="date" id="end_date" name="end_date"><br><br>
                <input type="submit" value="Submit">
            </form>
            <div id="result"></div>
        </body>
    </html>
    """

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(start_date: str = Form(...), end_date: str = Form(...)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    weekend_dates = get_weekend_dates(start_date, end_date)
    
    result = "<h2>Output:</h2>"
    result += f"<p>Hari Sabtu dan Minggu antara {start_date.strftime('%d %B %Y')} dan {end_date.strftime('%d %B %Y')}:</p>"
    result += "<ul>"
    for date in weekend_dates:
        result += f"<li>{date}</li>"
    result += "</ul>"
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

