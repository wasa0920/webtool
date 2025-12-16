from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    count = 0
    line_count = 0
    zenkaku = 0
    hankaku = 0
    ignore_space = False
    only_zenkaku = False

    if request.method == "POST":
        text = request.form.get("text", "")
        ignore_space = "ignore_space" in request.form
        only_zenkaku = "only_zenkaku" in request.form

        # 全角・半角カウント
        for c in text:
            if ord(c) <= 127:
                hankaku += 1
            else:
                zenkaku += 1

        # 文字数計算
        target = text
        if ignore_space:
            target = target.replace(" ", "").replace("\n", "")

        count = zenkaku if only_zenkaku else len(target)
        line_count = text.count("\n") + 1 if text else 0

    return render_template(
        "index.html",
        text=text,
        count=count,
        line_count=line_count,
        zenkaku=zenkaku,
        hankaku=hankaku,
        ignore_space=ignore_space,
        only_zenkaku=only_zenkaku
    )

if __name__ == "__main__":
    app.run(debug=True)
