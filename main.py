from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="World Tour Agent")

client = OpenAI()


class AgentRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>World Tour Agent</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
                padding: 20px;
            }

            .container {
                max-width: 700px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
            }

            textarea {
                width: 100%;
                height: 130px;
                padding: 12px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
            }

            button {
                width: 100%;
                margin-top: 12px;
                padding: 14px;
                border: none;
                border-radius: 10px;
                background: #222;
                color: white;
                font-size: 17px;
                cursor: pointer;
            }

            #answer {
                margin-top: 20px;
                padding: 15px;
                background: #f0f0f0;
                border-radius: 10px;
                white-space: pre-wrap;
                line-height: 1.8;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🤖 World Tour Agent</h1>

            <p>درخواست خودت را برای Agent بنویس:</p>

            <textarea id="message"
                placeholder="مثلاً: آخرین آمار جمعیت ژاپن را با منبع پیدا کن..."></textarea>

            <button onclick="sendMessage()">ارسال درخواست 🚀</button>

            <div id="answer">پاسخ Agent اینجا نمایش داده می‌شود...</div>

        </div>

        <script>
            async function sendMessage() {

                const message = document.getElementById("message").value;
                const answer = document.getElementById("answer");

                if (!message.trim()) {
                    answer.textContent = "لطفاً ابتدا درخواستت را بنویس.";
                    return;
                }

                answer.textContent = "⏳ Agent در حال تحقیق است...";

                try {

                    const response = await fetch("/agent", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    if (data.response) {
                        answer.textContent = data.response;
                    } else {
                        answer.textContent = "خطایی رخ داد.";
                    }

                } catch (error) {

                    answer.textContent =
                        "❌ ارتباط با Agent برقرار نشد.";

                }
            }
        </script>

    </body>
    </html>
    """


@app.post("/agent")
def run_agent(request: AgentRequest):

    response = client.responses.create(
        model="gpt-5.6-luna",
        tools=[
            {
                "type": "web_search"
            }
        ],
        input=request.message
    )

    return {
        "status": "success",
        "response": response.output_text
    }                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
            }

            textarea {
                width: 100%;
                height: 130px;
                padding: 12px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
            }

            button {
                width: 100%;
                margin-top: 12px;
                padding: 14px;
                border: none;
                border-radius: 10px;
                background: #222;
                color: white;
                font-size: 17px;
                cursor: pointer;
            }

            #answer {
                margin-top: 20px;
                padding: 15px;
                background: #f0f0f0;
                border-radius: 10px;
                white-space: pre-wrap;
                line-height: 1.8;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🤖 World Tour Agent</h1>

            <p>درخواست خودت را برای Agent بنویس:</p>

            <textarea id="message"
                placeholder="مثلاً: برای کشور ژاپن یک سناریوی ۲۰ دقیقه‌ای بساز..."></textarea>

            <button onclick="sendMessage()">ارسال درخواست 🚀</button>

            <div id="answer">پاسخ Agent اینجا نمایش داده می‌شود...</div>

        </div>

        <script>
            async function sendMessage() {

                const message = document.getElementById("message").value;
                const answer = document.getElementById("answer");

                if (!message.trim()) {
                    answer.textContent = "لطفاً ابتدا درخواستت را بنویس.";
                    return;
                }

                answer.textContent = "⏳ Agent در حال فکر کردن است...";

                try {

                    const response = await fetch("/agent", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    if (data.response) {
                        answer.textContent = data.response;
                    } else {
                        answer.textContent = "خطایی رخ داد.";
                    }

                } catch (error) {

                    answer.textContent =
                        "❌ ارتباط با Agent برقرار نشد.";

                }
            }
        </script>

    </body>
    </html>
    """


@app.post("/agent")
def run_agent(request: AgentRequest):

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=request.message
    )

    return {
        "status": "success",
        "response": response.output_text
    }
