from flask import Flask, render_template, request

app = Flask(__name__)

def improve_text(text, options):
    result = text

    # C：丁寧語に統一
    if "C" in options:
        result = result.replace("です。", "でございます。")
        result = result.replace("ます。", "ます。")

    # D：クッション言葉追加
    if "D" in options:
        if not result.startswith("恐れ入りますが"):
            result = "恐れ入りますが、\n" + result

    # E：結びを丁寧に
    if "E" in options:
        if "何卒よろしく" not in result:
            result += "\n\n何卒よろしくお願いいたします。"

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    original_text = ""
    improved_text = ""
    selected = []

    if request.method == "POST":
        original_text = request.form.get("text", "")
        selected = request.form.getlist("improve")

        if selected:
            improved_text = improve_text(original_text, selected)
        else:
            improved_text = original_text  # ←重要

    return render_template(
        "index.html",
        original_text=original_text,
        improved_text=improved_text,
        selected=selected
    )


if __name__ == "__main__":
    app.run(debug=True)
