from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html')


@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        result=dict()
        result['Name'] = request.form.get('name')
        result['StudentNumber']=request.form.get('StudentNumber')
        result['Gender'] = request.form.get('gender')
        result['Major'] = request.form.get('major')
        #복수 체크 항목
        result['languages'] = request.form.getlist('languages') #리스트로 받아와서
        result['languages'] =  ','.join(result['languages']) #쉼표로 구분-> 하나의 문자열로 합쳐서 dictionary에 저장
        
        return render_template('result.html',result=result)
        
if __name__ == '__main__':
    app.run(debug=True)