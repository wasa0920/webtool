from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    count = 0
    ignore_space = False
    line_count = 0
    zenkaku = 0
    hankaku = 0
    only_zenkaku = False

    if request.method == "POST":
        text = request.form["text"]
        ignore_space = "ignore_space" in request.form
        only_zenkaku = "only_zenkaku" in request.form

        if ignore_space:
            # 空白・改行を除外
            target = text.replace(" ", "").replace("\n", "")
            count = len(target)
        else:
            count = len(text)
    for c in text:
        if ord(c) <= 127:
            hankaku += 1
        else:
            zenkaku += 1

    # 「全角だけ数える」がONなら、文字数を全角に合わせる
    if only_zenkaku:
        count = zenkaku

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
