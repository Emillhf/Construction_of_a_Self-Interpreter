from flask import Flask, render_template, request, redirect, url_for
import subprocess
app = Flask(__name__)

app.config['Start_state'] = "1"
app.config['Final_state'] = "0"
app.config['Examples'] = ['Binary Increment', 'FLIP','URTM - BinInc', 'URTM - FLIP', 'URTM - Not Compiled']
app.config['selected_example'] = None
app.config['Is_1-tape'] = False
app.config['Interpreter'] = "Interpreter_3_tape/"
app.config['Tape_folder'] = "Website/3-Tapes_tapes/"
app.config['Example_folder'] = "Website/3-Tape-examples/"
app.config['Code_path'] = "Website/CODE.txt"
app.config['Tape_path'] = "Website/TAPE.txt"

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
            rules[idx] = f"({rule[0]},({move_inverted[0]},{move_inverted[1]},{move_inverted[2]}),{rule[-1]})"
        else:
            rule[1], rule[2] = rule[2], rule[1]
            rule[3], rule[4] = rule[4], rule[3]
            rule[5], rule[6] = rule[6], rule[5]
            rules[idx] = f"({rule[0]},(({rule[1]},{rule[2]}),({rule[3]},{rule[4]}),({rule[5]},{rule[6]})),{rule[-1]})".replace("'", '')
    return rules

@app.route("/", methods=['GET', 'POST'])
def home():
    code = "(1,((alfa,1),(b,b),(b,b)),0)"
    work = 'b'
    program = 'b'
    state = 'b'
    output = ''
    return render_template('Front_page.html', 
                           work=work, program=program, state=state,
                           code = code, 
                           output=output, 
                           Examples=app.config['Examples'], 
                           selected_example=app.config['selected_example'])
    

@app.route("/run", methods=['GET', 'POST'])
def run():
    if request.method == 'GET':
        return redirect(url_for('home'))
    if request.method == 'POST':
        code = request.form['code']
        work = request.form['work']        
        program = request.form['program']        
        state = request.form['state']  
        output = ''

        error = 0
        
        with open(app.config['Tape_path'], "w") as file:
            file.write(work + "\n!\n"+ program + "\n$\n" + "bbbb" + state + "b"*10)
            
        with open(app.config['Code_path'], "w") as file:
            file.write(code)
        
        try:
            result = subprocess.run(
                #["dotnet", "run", "--project", "../Interpreter_3_tape", "../3_Tape_programs/URTM.txt", app.config['Tape_path']],
                ["dotnet", "run", "--project", app.config['Interpreter'], app.config['Code_path'], app.config['Tape_path'], 
                                            app.config["Start_state"], app.config["Final_state"]],
                capture_output=True,
                timeout=5
            )
            output = result.stdout or result.stderr
            
            if (output.decode("utf-8").find("exception") != -1):
                print("Output")
                print(output)
                error = 1
            elif output.decode("utf-8").find("Current state") != -1:
                print(output)
                error = 2
                
        except Exception as e:
            output = str(e)
            print("Error")
            print(output)
            error = 3
            
        if error == 0:
            cleaned_output = (output.decode("utf-8").replace('"','').strip() + "\n\n" 
                            + program + "\n\n" + state)
        elif error == 2:
            cleaned_output = output.decode("utf-8")
        else:
            cleaned_output = "Error"

    return render_template('Front_page.html',
                           work=work, program=program, state=state, 
                           code = code, output = cleaned_output, 
                           Examples=app.config['Examples'], 
                           selected_example=app.config['selected_example'])
    
@app.route("/Compile", methods=['GET', 'POST'])
def Compile():
    if request.method == 'GET':
        return redirect(url_for('home'))    
    
    if request.method == 'POST':
        work = request.form['work']        
        program = request.form['program']        
        state = request.form['state'] 
        output = request.form['output']
        
        code = request.form['code']
        with open(app.config['Code_path'], "w") as file:
            file.write(app.config['Start_state'] + "\n" + app.config['Final_state'] + "\n" + code)
            
        try:
            subprocess.run(
                #["dotnet", "run", "--project", "../Interpreter_3_tape", "../3_Tape_programs/URTM.txt", app.config['Tape_path']],
                ["Python3", "Compilers/Dunja_to_3_tape.py", app.config['Code_path'], app.config['Code_path']],
                timeout=5
            )
            error = False
        except Exception as e:
            error = True

        if error:
            compiled_code = "Error when compiling"
        else:
            with open(app.config['Code_path'], "r") as file:
                lines = file.readlines()
                compiled_code = ''.join(lines)
    
    return render_template('Front_page.html',
                        work=work, program=program, state=state, 
                        code = compiled_code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example'])
@app.route("/invert", methods=['GET', 'POST'])
def invert():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        work = request.form['work']        
        program = request.form['program']        
        state = request.form['state'] 
        output = request.form['output']
        
        code = request.form['code']
        code = '\n'.join(Invert(code.strip().replace('\r','').split('\n')))
        app.config["Start_state"], app.config["Final_state"] = app.config["Final_state"], app.config["Start_state"]
        
    return render_template('Front_page.html',
                        work=work, program=program, state=state, 
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example'])        
    
@app.route('/Example', methods=['GET','POST'])
def load_Example():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        example = request.form['Examples']
        output = request.form['output']
        app.config["Start_state"], app.config["Final_state"] = "1", "0"
        if example == "Binary Increment":
            with open(app.config['Tape_folder'] + "BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]

            with open(app.config['Example_folder'] + "BinInc.txt", "r") as file:
                code = file.read() 
                
        elif example == "FLIP":
            with open(app.config['Tape_folder'] + "FLIP.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]

            with open(app.config['Example_folder'] + "FLIP.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - BinInc":
            with open(app.config['Tape_folder'] + "URTM_BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open(app.config['Example_folder'] + "URTM.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - FLIP":
            with open(app.config['Tape_folder'] + "URTM_FLIP.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open(app.config['Example_folder'] + "URTM.txt", "r") as file:
                code = file.read()  
                
        elif example == "URTM - Not Compiled":
            with open(app.config['Tape_folder'] + "URTM_BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open(app.config['Example_folder'] + "Dunja_URTM.txt", "r") as file:
                code = file.read()  
                
    return render_template('Front_page.html',
                        work=work, program=program, state=state, 
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example']) 

# @app.route('/Interpreter', methods=['GET','POST'])
# def Interpreter():
#     if request.method == 'POST':
#         print("Hi")
#         print(request.form['Interpreter'])
    
#     return render_template('Front_page.html', code = code, tape=tape, output=output, 
#                         Examples=app.config['Examples'], 
#                         selected_example=app.config['selected_example'], interpreter="1-Tape")
    
if __name__ == "__main__":
    app.run(debug=True)
