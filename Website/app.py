from flask import Flask, render_template, request, redirect, url_for
import subprocess
app = Flask(__name__)

app.config['Start_state'] = "1"
app.config['Final_state'] = "0"
app.config['Examples'] = ['Binary Increment', 'FLIP','URTM - BinInc', 'URTM - FLIP', 'URTM - Not Compiled']
app.config['selected_example'] = None
app.config['Is_3_Tape'] = True
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

def Invert_1Tape_move(move):
    if move == "(RIGHT)":
        return ("(LEFT)")
    elif move == "(LEFT)":
        return ("(RIGHT)")
    else:
        return ("(STAY)")
def Invert1Tape(rules):
    for idx, rule in enumerate(rules):
        if (rule == ""):
            continue
        rule = rule.split(",")
        rule[0] = rule[0].replace("(","")
        rule[-1] = rule[-1].replace(")","")
        
        rule[0], rule[-1] = rule[-1], rule[0]
        if len(rule) == 3:
            # rule[1] = rule[1][1:-1]
            move_inverted = Invert_1Tape_move(rule[1])
            rules[idx] = f'({rule[0]},{move_inverted},{rule[-1]})'
        else:
            rule[1] = rule[1][1::]
            rule[2] = rule[2][:-1]

            rule[1], rule[2] = rule[2], rule[1]
            rules[idx] = f"({rule[0]},({rule[1]},{rule[2]}),{rule[-1]})".replace("'", '')
    return rules
@app.route("/", methods=['GET', 'POST'])
def home():
    app.config['Start_State'] = '1'
    app.config['Final_State'] = '0'
    app.config['Is_3_Tape'] = True
    code = "(1,((b,1),(b,b),(b,b)),0)"
    work = 'b'
    program = 'b'
    state = 'b'
    output = ''
    return render_template("3-Tape_page.html", 
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
            file.write(code.replace("\n", ''))
        
        try:
            result = subprocess.run(
                ["dotnet", "run", "--project", "Interpreter_3_tape", app.config['Code_path'], app.config['Tape_path'], 
                                            app.config["Start_state"], app.config["Final_state"]],
                capture_output=True,
                timeout=50
            )
            output = result.stdout or result.stderr
            print(output)
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

    return render_template("3-Tape_page.html",
                           work=work, program=program, state=state, 
                           code = code, output = cleaned_output, 
                           Examples=app.config['Examples'], 
                           selected_example=app.config['selected_example'])
    
@app.route("/1-tape/run", methods=['GET', 'POST'])
def one_tape_run():
    if request.method == 'GET':
        return redirect(url_for('home'))
    if request.method == 'POST':
        code = request.form['code']
        work = request.form['work']            
        output = ''

        error = 0
        
        with open(app.config['Tape_path'], "w") as file:
            file.write('b'*5 + "$" + work + "$" + 'b'*5) 
            
        with open(app.config['Code_path'], "w") as file:
            file.write(code.replace("\n", ''))
        
        try:
            result = subprocess.run(
                ["dotnet", "run", "--project", "Interpreter_1_tape", app.config['Code_path'], app.config['Tape_path'], 
                                            app.config["Start_state"], app.config["Final_state"], "6"],
                capture_output=True,
                timeout=50
            )
            output = result.stdout or result.stderr
            print(output)
            if (output.decode("utf-8").find("Symbol") != -1) or (output.decode("utf-8").find("Symbol") != -1):
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
            cleaned_output = (output.decode("utf-8").replace('"','').strip())
            cleaned_output = '$'.join(cleaned_output.split('$')[1:-1])
        elif error == 2:
            cleaned_output = output.decode("utf-8")
        else:
            cleaned_output = "Error"

    return render_template("1-Tape_page.html",
                           work=work,
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
            
        try:
            with open(app.config['Code_path'], "w") as file:
                file.write(app.config['Start_state'] + "\n" + app.config['Final_state'] + "\n" + code)
            result = subprocess.run(
                ["python3", "Compilers/Dunja_to_3_tape.py", app.config['Code_path'], app.config['Code_path']],
                capture_output=True,
                timeout=50
            )
            output = result.stdout or result.stderr
            print(output)
            if output.decode("utf-8").find("Traceback") == -1:
                error = False 
            else: 
                error = True
        except Exception as e:
            error = True

        if error:
            compiled_code = "Error when compiling"
        else:
            with open(app.config['Code_path'], "r") as file:
                lines = file.readlines()
                compiled_code = ''.join(lines)
    
    return render_template("3-Tape_page.html",
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
        try:
            code = '\n'.join(Invert(code.strip().replace('\r','').split('\n')))
        except:
            code = "Unable to Invert"
        app.config["Start_state"], app.config["Final_state"] = app.config["Final_state"], app.config["Start_state"]
        
    return render_template("3-Tape_page.html",
                        work=work, program=program, state=state, 
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example']) 
           
@app.route("/1-tape/invert", methods=['GET', 'POST'])
def one_tape_invert():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        work = request.form['work']        
        output = request.form['output']
        
        code = request.form['code']
        try:
            code = '\n'.join(Invert1Tape(code.strip().replace('\r','').split('\n')))
        except:
            code = "Unable to Invert"
        app.config["Start_state"], app.config["Final_state"] = app.config["Final_state"], app.config["Start_state"]
        
    return render_template("1-Tape_page.html",
                        work=work,
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example'])        
    
@app.route('/Example', methods=['GET','POST'])
def load_Example():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            example = request.form['Examples']
        except:
            return redirect(url_for('home'))
        output = request.form['output']
        app.config["Start_state"], app.config["Final_state"] = "1", "0"
        if example == "Binary Increment":
            with open("Website/3-Tapes_tapes/" + "BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]

            with open("Website/3-Tape-examples/" + "BinInc.txt", "r") as file:
                code = file.read() 
                
        elif example == "FLIP":
            with open("Website/3-Tapes_tapes/" + "FLIP.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]

            with open("Website/3-Tape-examples/" + "FLIP.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - BinInc":
            with open("Website/3-Tapes_tapes/" + "URTM_BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open("Website/3-Tape-examples/" + "URTM.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - FLIP":
            with open("Website/3-Tapes_tapes/" + "URTM_FLIP.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open("Website/3-Tape-examples/" + "URTM.txt", "r") as file:
                code = file.read()  
                
        elif example == "URTM - Not Compiled":
            with open("Website/3-Tapes_tapes/" + "URTM_BinInc.txt","r") as file:
                lines = file.readlines()
                work,program,state = lines[0], lines[2], lines[4]
                
            with open("Website/3-Tape-examples/" + "Dunja_URTM.txt", "r") as file:
                code = file.read()  
                
    return render_template("3-Tape_page.html",
                        work=work, program=program, state=state, 
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example']) 
    
@app.route('/1-tape/Example', methods=['GET','POST'])
def one_tape_load_Example():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            example = request.form['Examples']
        except:
            return redirect(url_for('home'))
        output = request.form['output']
        app.config["Start_state"], app.config["Final_state"] = "1", "0"
        if example == "Binary Increment":
            with open("Website/1-Tapes_tapes/" + "BinInc.txt","r") as file:
                lines = file.readlines()
                work = lines[0]

            with open("Website/1-Tape-examples/" + "BinInc.txt", "r") as file:
                code = file.read() 
                
        elif example == "FLIP":
            with open("Website/1-Tapes_tapes/" + "FLIP.txt","r") as file:
                lines = file.readlines()
                work = lines[0]

            with open("Website/1-Tape-examples/" + "FLIP.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - BinInc":
            with open("Website/1-Tapes_tapes/" + "URTM_BinInc.txt","r") as file:
                lines = file.readlines()
                work = lines[0]
                
            with open("Website/1-Tape-examples/" + "URTM.txt", "r") as file:
                code = file.read() 
                
        elif example == "URTM - FLIP":
            with open("Website/1-Tapes_tapes/" + "URTM_FLIP.txt","r") as file:
                lines = file.readlines()
                work = lines[0]
                
            with open("Website/1-Tape-examples/" + "URTM.txt", "r") as file:
                code = file.read()  
                
    return render_template("1-Tape_page.html",
                        work=work,
                        code = code, output = output, 
                        Examples=app.config['Examples'], 
                        selected_example=app.config['selected_example']) 

@app.route('/Swap', methods=['GET','POST'])
def Interpreter():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        output = ''
        if app.config['Is_3_Tape']:
            app.config['Examples'] = ['Binary Increment', 'FLIP','URTM - BinInc', 'URTM - FLIP']
            app.config['Is_3_Tape'] = False
            code = "(1,(p,1),0)"
            work = 'p$p$p'
            return render_template('1-Tape_page.html',
                                work=work,
                                code = code, output = output, 
                                Examples=app.config['Examples'], 
                                selected_example=app.config['selected_example']) 
        else:
            app.config['Examples'] = ['Binary Increment', 'FLIP','URTM - BinInc', 'URTM - FLIP', 'URTM - Not Compiled']
            app.config['Is_3_Tape'] = True
            code = "(1,((b,1),(b,b),(b,b)),0)"
            work = 'b'
            program = 'b'
            state = 'bbbbb'
            output = ''
            return render_template('3-Tape_page.html',
                                work=work, program=program, state=state,
                                code = code, output = output, 
                                Examples=app.config['Examples'], 
                                selected_example=app.config['selected_example']) 

@app.route('/invert_program', methods=['GET','POST'])
def invert_program():
    if request.method == 'GET':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        code = request.form['code']        
        work = request.form['work']        
        program = request.form['program'].strip()[::-1]
        if ('#0#' in program) and ("#1#" in program):
            idx = program.index('#0#')
            program = program.replace('#1#','#0#')
            program = program[:idx] + '#1#' + program[idx + 3:]
        state = request.form['state'] 
        output = request.form['output']
        
    return render_template("3-Tape_page.html",
                work=work, program=program, state=state, 
                code = code, output = output, 
                Examples=app.config['Examples'], 
                selected_example=app.config['selected_example']) 
if __name__ == "__main__":
    app.run(debug=True)
