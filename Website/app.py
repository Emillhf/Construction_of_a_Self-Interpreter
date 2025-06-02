from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)
swap = {"1":"0", "0":"1"}
def Invert_Move(rule):
    result = []
    for elm in rule:
        if elm == "RIGHT":
            result.append("(LEFT)")
        elif elm == "LEFT":
            result.append("(RIGHT)")
        else:
            result.append("(STAY)")
    return result
def Invert(rules):
    for idx, rule in enumerate(rules):
        rule = rule.split(",")
        rule = [(elm.replace('(', '')).replace(')','') for elm in rule]
        rule[0], rule[-1] = rule[-1], rule[0]
        if len(rule) == 5:
            move_inverted = Invert_Move(rule[1:-1])
            rules[idx] = f"({swap.get(rule[0],rule[0])},({move_inverted[0]},{move_inverted[1]},{move_inverted[2]}),{swap.get(rule[-1],rule[-1])})"
        else:
            rule[1], rule[2] = rule[2], rule[1]
            rule[3], rule[4] = rule[4], rule[3]
            rule[5], rule[6] = rule[6], rule[5]
            rules[idx] = f"({swap.get(rule[0],rule[0])},(({rule[1]},{rule[2]}),({rule[3]},{rule[4]}),({rule[5]},{rule[6]})),{swap.get(rule[-1],rule[-1])})".replace("'", '')
    return rules

@app.route("/", methods=['GET', 'POST'])
def home():
    code = "(1,((b,1),(b,b),(b,b)),0)"
    tape = ['b'] * 17
    output = ['b'] * 18
    return render_template('Front_page.html', code = code, tape=tape, output=output)

@app.route("/run", methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        code = request.form['code']
        tape_values = request.form.getlist('tape_list')
        output = ['b'] * 17
        tape = ''.join(tape_values) + '\n'
        
        with open("3-Tapes_tapes/program_state_tape.txt", "r") as file:
            content = file.read() 

        with open("tape.txt", "w") as file:
            file.write(tape + content)
            
        with open("CODE.txt", "w") as file:
            file.write(code)
            
        try:
            result = subprocess.run(
                #["dotnet", "run", "--project", "../Interpreter_3_tape", "../3_Tape_programs/URTM.txt", "tape.txt"],
                ["dotnet", "run", "--project", "../Interpreter_3_tape", "CODE.txt", "tape.txt"],
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
            
        # print("Submitted code:\n", code
    cleaned_output = output.decode("utf-8").replace('"','')
    return render_template('Front_page.html', code = code, tape=tape_values, output = cleaned_output)

@app.route("/invert", methods=['GET', 'POST'])
def invert():
    if request.method == 'POST':
        code = request.form['code']
        tape = request.form.getlist('tape_list')
        output = request.form.getlist('output_list')
        code = '\n'.join(Invert(code.strip().replace('\r','').split('\n')))
    return render_template('Front_page.html', code = code, tape = tape, output=output)
        
@app.route('/BinInc', methods=['POST'])
def load_BinInc():
    if request.method == 'POST':
        tape = ['b', '1', '1', '0', '1', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
        output = request.form.getlist('output_list')
        with open("3-Tape-examples/BinInc.txt", "r") as file:
            code = file.read() 
    
    return render_template('Front_page.html', code=code, tape=tape, output = output)

if __name__ == "__main__":
    app.run(debug=True)
