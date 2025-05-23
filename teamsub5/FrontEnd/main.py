from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import random

app = Flask(__name__)

UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 전역 데이터 저장
members = []

# ------------------- 홈 페이지 -------------------
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
        "Name": request.form.get("name", "").strip(),
        "Dept": request.form.get("dept", "").strip() or request.form.get("Major", "").strip(),
        "Email": request.form.get("email", "").strip(),
        "Role": request.form.get("role", "").strip(),
        "Phone": request.form.get("phone", "").strip(),
        "MBTI": request.form.get("mbti", "").upper(),
        "Comment": request.form.get("comment", "").strip(),
        "Languages": ", ".join(request.form.getlist("languages")),
        "FutureOrg": request.form.get("future_org", "").strip(),
        "Motto": request.form.get("motto", "").strip()
    }

    #이미지 파일 저장
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

# ------------------- 교수님 게임 -------------------
people = [
    {
        "name": "수빈",
        "tmis": ["돈까스가 소울푸드", "리트리버 키움, 고양이 키움"]
    },
    {
        "name": "원",
        "tmis": ["검정 옷 입는 걸 좋아함", "추위 많이 타서 여름에도 핫팩들고 다님", "삼각김밥 안 데워먹음"]
    },
    {
        "name": "시은",
        "tmis": ["케찹을 싫어해서 감자튀김만 먹음", "웰시코기를 키움", "눈썹 탈색을 주기적으로 함"]
    }
]

fake_tmis = [
    "외계인과 연락한 적 있음",
    "한 달 동안 말 안 하고 살기 성공",
    "잠든 채로 시험 만점",
    "라면을 수저로 먹음"
]

def generate_quiz():
    person = random.choice(people)
    is_real = random.choice([True, False])
    tmi = random.choice(person["tmis"] if is_real else fake_tmis)
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

@app.route("/professor_page")
def professor_page():
    return render_template("professor.html")

@app.route("/professor/mission", methods=["POST"])
def professor_mission():
    missions = [
        "☕ 오늘은 꼭 커피 한 잔의 여유를 가지세요.",
        "🎓 강의 시작 전에 충분한 휴식을 취해주세요.",
        "📢 학생의 발표에 박수를 보내주세요!",
        "🌿 캠퍼스를 10분 산책해보시는 건 어떨까요?",
    ]
    result = random.choice(missions)
    return render_template("professor.html", result=result)

@app.route("/professor/cheer", methods=["POST"])
def professor_cheer():
    cheers = [
        "오늘도 교수님의 강의는 명강의입니다! 👏",
        "교수님 덕분에 오픈소스가 즐거워졌어요 😊",
        "학생들은 언제나 이길섭 교수님을 응원하고 있어요 💪",
        "교수님, 정말 멋지십니다! 🌟",
    ]
    result = random.choice(cheers)
    return render_template("professor.html", result=result)


# ------------------- 서버 실행 -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)