from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    code = "(1,((b,1),(b,b),(b,b)),0)"
    tape = ['b'] * 17
    
    if request.method == 'POST':
        code = request.form['code']
        tape_values = request.form.getlist('tape_list')
        tape = ''.join(tape_values) + "\n"
        
        with open("3-Tapes_tapes/BinInc.txt", "r") as file:
            content = file.read() 

        with open("tape.txt", "w") as file:
            file.write(tape + content)
            
        try:
            result = subprocess.run(
                ["dotnet", "run", "--project", "../Interpreter_3_tape", "../3_Tape_programs/URTM.txt", "tape.txt"],
                capture_output=True,
                timeout=5
            )
            output = result.stdout or result.stderr
            print("Output")
            print(output)
            
        except Exception as e:
            output = str(e)
            print("Error")
            print(output)
            
        # print("Submitted code:\n", code)


    return render_template('Front_page.html', code = code, tape=tape)

if __name__ == "__main__":
    app.run(debug=True)
