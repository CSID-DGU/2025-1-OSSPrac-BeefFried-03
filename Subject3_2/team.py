from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import random

app = Flask(__name__)

UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 전역 데이터 저장
members = []

# ------------------- 새 홈 페이지 -------------------
@app.route("/")
def home():
    return render_template("home.html")

# ------------------- 입력 화면 -------------------
@app.route("/input")
def input_page():
    order = len(members) + 1
    return render_template("input.html", order=order)

@app.route("/submit", methods=["POST"])
def submit():
    member = {
        "Name":     request.form.get("name", "").strip(),
        "Dept":     request.form.get("dept", "").strip(),
        "Email":    request.form.get("email", "").strip(),
        "Role":     request.form.get("role", "").strip(),
        "Phone":    request.form.get("phone", "").strip(),
        "MBTI":     request.form.get("mbti", "").upper(),
        "Comment":  request.form.get("comment", "").strip(),
        "Languages": ", ".join(request.form.getlist("languages")),
        "FutureOrg": request.form.get("future_org", "").strip(),  
        "Motto":     request.form.get("motto", "").strip()        
    }

    # 이미지 저장
    img_now = request.files.get("img_now")
    img_future = request.files.get("img_future")

    if img_now and img_now.filename:
        fname = secure_filename(img_now.filename)
        img_now.save(os.path.join(UPLOAD_DIR, fname))
        member["ImgNow"] = f"uploads/{fname}"

    if img_future and img_future.filename:
        fname = secure_filename(img_future.filename)
        img_future.save(os.path.join(UPLOAD_DIR, fname))
        member["ImgFuture"] = f"uploads/{fname}"

    members.append(member)

    if len(members) >= 3:
        return redirect(url_for("result"))
    return redirect(url_for("input_page"))

# ------------------- 결과 보기 -------------------
@app.route("/result")
def result():
    return render_template("result.html", members=members)

# ------------------- Contact -------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

people = [
    {
        "name": "수빈",
        "tmis": ["밥보다 빵을 좋아함", "고양이, 강아지 두 마리 키움"]
    },
    {
        "name": "원",
        "tmis": ["고등학교 때 밴드부", "고기를 못 먹음"]
    },
    {
        "name": "시은",
        "tmis": ["MBTI는 INFP", "비 오는 날 노래 듣기 좋아함"]
    }
]

fake_tmis = [
    "외계인과 연락한 적 있음",
    "한 달 동안 말 안 하고 살기 성공",
    "잠든 채로 시험 만점",
    "자장면을 수저로 먹음"
]

def generate_quiz():
    person = random.choice(people)
    is_real = random.choice([True, False])

    if is_real:
        tmi = random.choice(person["tmis"])
    else:
        tmi = random.choice(fake_tmis)

    return {
        "name": person["name"],
        "tmi": tmi,
        "is_true": is_real,
        "question": f"'{tmi}' 이 TMI는 {person['name']}의 진짜 정보일까요?"
    }

@app.route("/game", methods=["GET", "POST"])
def game():
    result = None
    quiz = generate_quiz()

    if request.method == "POST":
        user_answer = request.form["answer"] == "true"
        correct = request.form["is_true"] == "True"
        result = "정답입니다!" if user_answer == correct else "오답입니다!"

    return render_template("game.html", quiz=quiz, result=result)

# -------------------
if __name__ == "__main__":
    app.run(debug=True)
