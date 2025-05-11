# app.py  ───────────────
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 업로드 파일을 저장 폴더
UPLOAD_DIR = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 3명의 데이터 보관 리스트
members = []         

# ──────────────────────────────────────────────────────────────
@app.route("/")
def input_page():
 
    order = len(members) + 1         
    return render_template("input.html", order=order)

@app.route("/submit", methods=["POST"])
def submit():
    
    member = {
        "Name":     request.form.get("name", "").strip(),
        "Dept":     request.form.get("Major", "").strip(),
        "Email":    request.form.get("email", "").strip(),
        "Role":     request.form.get("role", "").strip(),
        "Phone":    request.form.get("phone", "").strip(),
        "MBTI":     request.form.get("mbti", "").upper(),
        "Comment":  request.form.get("comment", "").strip(),
        "Languages": ", ".join(request.form.getlist("languages"))
    }

    #이미지 파일 저장
    img_now   = request.files.get("img_now")
    img_future= request.files.get("img_future")
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

@app.route("/result")
def result():
    
    global members
    data = members.copy()  
    members = []           
    return render_template("main.html", members=data)  #수정

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
