from flask import Flask, render_template, request
import re
import math

app = Flask(__name__)

# NGワード（差別化用・今後増やせる）
NG_WORDS = [
    "恐れ入りますが",
    "お手数ですが",
    "ご確認ください",
    "念のため",
    "一応",
    "とりあえず"
]

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    total_count = 0
    line_count = 0
    paragraph_count = 0
    read_time = 0
    found_ng_words = []

    types = {
        "kanji": 0,
        "hiragana": 0,
        "katakana": 0,
        "alphabet": 0,
        "number": 0,
        "symbol": 0,
        "zenkaku": 0,
        "hankaku": 0
    }

    if request.method == "POST":
        text = request.form.get("text", "")

        # 文字数
        total_count = len(text)

        # 行数
        line_count = text.count("\n") + 1 if text else 0

        # 段落数（空行区切り）
        paragraph_count = len([p for p in text.split("\n\n") if p.strip()])

        # 読み時間（日本語400文字/分想定）
        read_time = math.ceil(total_count / 400) if total_count else 0

        # 文字種別カウント
        for c in text:
            code = ord(c)

            if code <= 127:
                types["hankaku"] += 1
            else:
                types["zenkaku"] += 1

            if re.match(r"[一-龯]", c):
                types["kanji"] += 1
            elif re.match(r"[ぁ-ん]", c):
                types["hiragana"] += 1
            elif re.match(r"[ァ-ヶー]", c):
                types["katakana"] += 1
            elif re.match(r"[A-Za-z]", c):
                types["alphabet"] += 1
            elif re.match(r"[0-9]", c):
                types["number"] += 1
            else:
                types["symbol"] += 1

        # NGワード検出
        for word in NG_WORDS:
            if word in text:
                found_ng_words.append(word)

    return render_template(
        "index.html",
        text=text,
        total_count=total_count,
        line_count=line_count,
        paragraph_count=paragraph_count,
        read_time=read_time,
        types=types,
        found_ng_words=found_ng_words
    )


if __name__ == "__main__":
    app.run(debug=True)
