from flask import Flask, render_template, request
import math

app = Flask(__name__)

def count_types(text):
    counts = {
        "kanji": 0,
        "hiragana": 0,
        "katakana": 0,
        "alphabet": 0,
        "number": 0,
        "symbol": 0,
        "zenkaku": 0,
        "hankaku": 0
    }

    for c in text:
        code = ord(c)
        if 0x4E00 <= code <= 0x9FAF:  # 漢字
            counts["kanji"] += 1
        elif 0x3040 <= code <= 0x309F:  # ひらがな
            counts["hiragana"] += 1
        elif 0x30A0 <= code <= 0x30FF:  # カタカナ
            counts["katakana"] += 1
        elif c.isalpha():  # 英字
            counts["alphabet"] += 1
        elif c.isdigit():  # 数字
            counts["number"] += 1
        elif code > 127:
            counts["zenkaku"] += 1
            counts["symbol"] += 1
        else:
            counts["hankaku"] += 1
            counts["symbol"] += 1

    return counts

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    total_count = 0
    line_count = 0
    paragraph_count = 0
    types = {
        "kanji":0,"hiragana":0,"katakana":0,"alphabet":0,
        "number":0,"symbol":0,"zenkaku":0,"hankaku":0
    }
    read_time = 0

    if request.method == "POST":
        text = request.form.get("text","")
        line_count = text.count("\n") + 1 if text else 0
        paragraph_count = text.count("\n\n") + 1 if text else 0
        types = count_types(text)
        total_count = len(text)
        read_time = math.ceil(total_count / 400)

    return render_template(
        "index.html",
        text=text,
        total_count=total_count,
        line_count=line_count,
        paragraph_count=paragraph_count,
        types=types,
        read_time=read_time
    )

if __name__ == "__main__":
    app.run(debug=True)
