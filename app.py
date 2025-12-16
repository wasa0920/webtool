from flask import Flask, render_template, request

app = Flask(__name__)

NG_WORDS = {
    "了解です": "「承知いたしました」が推奨です",
    "すみません": "「申し訳ございません」が丁寧です",
    "了解しました": "目上の方には「承知いたしました」",
    "ご苦労様": "目上の方には「お疲れ様です」"
}

SOFT_REPLACE = {
    "お願いします": "お願いできますでしょうか",
    "確認してください": "ご確認いただけますと幸いです",
}

HARD_REPLACE = {
    "お願いします": "お願い申し上げます",
    "確認してください": "ご確認のほど何卒よろしくお願い申し上げます",
}


def rewrite_text(text, level):
    for k, v in NG_WORDS.items():
        text = text.replace(k, v.split("」")[0])

    if level == "soft":
        for k, v in SOFT_REPLACE.items():
            text = text.replace(k, v)
    elif level == "hard":
        for k, v in HARD_REPLACE.items():
            text = text.replace(k, v)

    return text


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = ""
    warnings = []
    level = "normal"

    if request.method == "POST":
        text = request.form.get("text", "")
        level = request.form.get("level", "normal")

        for word, msg in NG_WORDS.items():
            if word in text:
                warnings.append(f"⚠ {msg}")

        body = rewrite_text(text, level)

        head = "お世話になっております。\n\n"
        tail = "\n\n何卒よろしくお願いいたします。"

        result = head + body + tail

    return render_template(
        "index.html",
        text=text,
        result=result,
        warnings=warnings,
        level=level
    )


if __name__ == "__main__":
    app.run(debug=True)
