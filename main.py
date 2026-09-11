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
    </head>

    <body>
        <h1>World Tour Agent</h1>

        <textarea id="message"
            rows="6"
            style="width:100%;"
            placeholder="درخواست خودت را بنویس..."></textarea>

        <br><br>

        <button onclick="sendMessage()">ارسال</button>

        <pre id="answer"></pre>

        <script>
            async function sendMessage() {

                const message =
                    document.getElementById("message").value;

                const answer =
                    document.getElementById("answer");

                answer.textContent =
                    "در حال تحقیق...";

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

                    answer.textContent =
                        data.response || "خطایی رخ داد.";

                } catch (error) {

                    answer.textContent =
                        "ارتباط با Agent برقرار نشد.";

                }
            }
        </script>

    </body>
    </html>
    """


@app.post("/agent")
def run_agent(request: AgentRequest):

    system_prompt = """
تو دستیار تحقیق و تولید محتوای کانال یوتیوب World Tour Farsi هستی.

وظیفه تو این است که برای موضوعی که کاربر می‌دهد:

1. اطلاعات به‌روز را از منابع معتبر وب بررسی کنی.
2. برای آمار و اطلاعات مهم، منبع را مشخص کنی.
3. اگر اطلاعاتی قطعی نیست، آن را به‌عنوان واقعیت قطعی بیان نکنی.
4. اطلاعات را به زبان فارسی و به شکل مرتب ارائه کنی.
5. برای موضوعات مربوط به کشورها، این موارد را در صورت مرتبط بودن بررسی کنی:
   - جمعیت
   - مساحت
   - پایتخت
   - شهرهای مهم
   - تاریخ
   - فرهنگ
   - اقتصاد
   - آب‌وهوا
   - گردشگری
   - غذا
   - ورزش
   - شرکت‌ها و برندهای معروف
   - روابط با ایران
   - نکات جالب و غیرمعمول

اگر کاربر درخواست تولید محتوای ویدیویی داشت، خروجی را به این شکل تنظیم کن:

بخش ۱: عنوان بخش
نریشن:
متن پیشنهادی گوینده

تصاویر پیشنهادی:
- تصویر اول
- تصویر دوم

ویدیوهای پیشنهادی:
- نوع ویدیوی مناسب
- نوع نمای مناسب

منابع:
- نام منبع
- لینک منبع در صورت امکان

مدت پیشنهادی:
زمان تقریبی این بخش

در پایان، یک Shot List مرتب و قابل استفاده برای تدوین ارائه کن.

لحن فارسی باید خودمانی، روان و مناسب یوتیوب باشد.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        tools=[
            {
                "type": "web_search"
            }
        ],
        instructions=system_prompt,
        input=request.message
    )

    return {
        "status": "success",
        "response": response.output_text
    }
