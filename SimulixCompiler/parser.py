import re
import globals
from utils import Utils

class Parser:
    @staticmethod
    def process_include(line):
        words = line.split()
        if words[0] != "include":
            Utils.write_in_file('Error: Sintaxă "include" incorectă')
            exit(1)
        if words[1][0] != '"' or words[1][-1] != '"':
            Utils.write_in_file('Error: Included file name must be in double quotes (" ")')
            exit(1)
        
        # Extragem numele fișierului și apelăm recursiv pentru acel fișier
        included_file = words[1][1:-1]
        Parser.read_file(included_file)

    @staticmethod
    def process_write(line):
        pattern = r'^write \(([\w\s,]+)\)'
        match = re.match(pattern, line)
        if not match:
            Utils.write_in_file("Error: write syntax error")
            exit(1)
        Utils.write_in_file(f"{' ' * globals.spaces}cout" , end="")
        for variabel in match.group(1).replace(' ','').split(","):
            Utils.write_in_file(f" << {variabel}",end="")
        Utils.write_in_file(";")

    @staticmethod
    def process_read(line):
        pattern = r'^read \(([\w\s,]+)\)'
        match = re.match(pattern, line)
        if not match:
            Utils.write_in_file("Error: read syntax error")
            exit(1)
        Utils.write_in_file(f"{' ' * globals.spaces}cin" , end="")
        for variabel in match.group(1).replace(' ','').split(","):
            Utils.write_in_file(f" >> {variabel}",end="")
        Utils.write_in_file(";")

    @staticmethod
    def process_equation(equations):
        Utils.capture_print(" "*globals.spaces,"this->eq = new Equation[",len(globals.equations),"];",sep="")
        iteration=0
        times_prefix=[]
        diff_pattern = r'diff\(([^,]+),\s*([^)]+)\)'
        for line in globals.equations:
            if line[:9] != "equation ":
                Utils.write_in_file("Error: equation syntax error")
                exit(1)
            iteration+=1
            Utils.capture_print(" "*globals.spaces,"this->eq[",iteration,"] = \"",line[9:],"\";",sep="")

    @staticmethod
    def process_model(line, file):
        # Citirea fișierului într-o listă de linii
        lines = file.readlines()
        
        # Găsim linia curentă și o procesăm
        line = line.strip()

        # Pattern pentru a recunoaște declarația unui model
        pattern = r'^def model (\w+)\(([\w\s,]+)\)'
        match = re.match(pattern, line)

        if not match:
            Utils.write_in_file("Error: model syntax error")
            exit(1)

        # Extrage numele modelului și parametrii
        name = match.group(1)
        parameters = [param.strip() for param in match.group(2).split(',')]

        # Începe generarea clasei model în C++
        output = Utils.capture_print(f"{' ' * globals.spaces}class {name} : public Model {{")

        Utils.capture_print(f"{' ' * globals.spaces}public:")
        globals.spaces += 4

        # Citește declarațiile de variabile din model
        var_types = {}
        var_lines = []
        
        # Citim liniile din fișier
        i = 0  # Indice pentru iterarea prin lista de linii
        while i < len(lines):
            nested_line = lines[i].strip()
            
            if nested_line.startswith("var"):
                var_lines.append(nested_line)
                var_parts = nested_line.split(':')
                var_names = var_parts[0][3:].replace(" ", "").split(',')  # Împarte pentru variabile multiple
                var_type = var_parts[1].strip()
                for var_name in var_names:
                    var_types[var_name.strip()] = var_type  # Elimină spațiile pentru fiecare nume de variabilă
            elif nested_line.lower() == "end model":
                break
            
            i += 1  # Avansăm la următoarea linie

        # Generează constructorul cu tipurile de parametri
        Utils.capture_print(f"{' ' * globals.spaces}{name}(", end="")
        param_declarations = []
        for param in parameters:
            param_type = var_types.get(param, "auto")  # Utilizare "auto" pentru parametrii nedefiniți
            param_declarations.append(f"{param_type} {param}")
        Utils.capture_print(", ".join(param_declarations), ")")

        # Corpul constructorului
        Utils.capture_print(f"{' ' * globals.spaces}{{")
        for param in parameters:
            Utils.capture_print(f"{' ' * (globals.spaces + 4)}this->{param} = {param};")

        number_of_equations =0

        i=0
        # Continuăm cu citirea liniei următoare, folosind același indice `i`
        while i < len(lines):
            nested_line = lines[i].strip()
            if nested_line.lower() == "end model":
                break
            elif nested_line.startswith("equation"):
                globals.equations.append(nested_line)
                number_of_equations+=1
            elif not nested_line.startswith("var") and nested_line:
                Utils.capture_print(f"{' ' * (globals.spaces + 4)}{nested_line}")
        
            i += 1  # Avansăm la următoarea linie

        Parser.process_equation(globals.equations)

        Utils.capture_print(f"{' ' * globals.spaces}}}")
        globals.spaces -= 4
        Utils.capture_print(f"{' ' * globals.spaces}private:")
        globals.spaces += 4
        for variable in var_lines:
            Parser.process_var_model(variable)
        globals.spaces -= 4
        Utils.capture_print(f"{' ' * globals.spaces}}};")
        Utils.insert_before_of("int main()",output)

    @staticmethod
    def process_while(line, file):
        # Remove 'while' from the beginning of the line
        condition = line.replace('while', '', 1).strip()

        # Split the condition by comparison operators
        operators = ['<=', '>=', '<', '>', '==', '!=']
        operator = next((op for op in operators if op in condition), None)

        if operator:
            left, right = condition.split(operator)
            Utils.write_in_file(f"{' ' * globals.spaces}while ({left.strip()} {operator} {right.strip()})")
        else:
            Utils.write_in_file(f"{' ' * globals.spaces}while ({condition})")

        Utils.write_in_file(f"{' ' * globals.spaces}{{")
        globals.spaces += 4

        # Process the body of the while loop
        for nested_line in file:
            nested_line = nested_line.strip()
            if nested_line.lower() == "end while":
                break
            elif nested_line.startswith("for"):
                Parser.process_for(nested_line, file)
            elif nested_line.startswith("read"):
                Parser.process_read(line)
            elif nested_line.startswith("while"):
                Parser.process_while(nested_line, file)
            elif nested_line.startswith("var"):
                Parser.process_var(nested_line)
            elif '(' in nested_line and ')' in nested_line:  # Possible macro call
                Parser.process_macro_call(nested_line)
            elif nested_line:
                Utils.write_in_file(f"{' ' * globals.spaces}{nested_line}")

        globals.spaces -= 4
        Utils.write_in_file(f"{' ' * globals.spaces}}}")

    @staticmethod
    def process_for(line, file):
        # Împărțim linia în tokens, păstrând separatorii
        tokens = re.split(r'(\s+|=|,)', line)
        # Eliminăm spațiile și tokenurile goale
        tokens = [token for token in tokens if token.strip()]

        if len(tokens) < 5 or tokens[0] != 'for':
            Utils.write_in_file('Error: For loop syntax error')
            exit(1)

        var = tokens[1]
        start = tokens[3]
        end = tokens[5]
        step = "1"  # Pas implicit

        # Verificăm dacă există un pas specificat
        if len(tokens) > 6 and tokens[6] == ',':
            if len(tokens) > 7:
                step = tokens[7]
            else:
                Utils.write_in_file('Error: Step value missing after comma in for loop')
                exit(1)

        Utils.write_in_file(f"{' ' * globals.spaces}for (int {var} = {start}; {var} <= {end}; {var} += {step})")
        Utils.write_in_file(f"{' ' * globals.spaces}{{")
        globals.spaces += 4

        # Procesăm corpul buclei for
        for nested_line in file:
            nested_line = nested_line.strip()
            if nested_line.lower() == "end for":
                break
            elif nested_line.startswith("for"):
                Parser.process_for(nested_line, file)
            elif nested_line.startswith("while"):
                Parser.process_while(nested_line, file)
            elif nested_line.startswith("var"):
                Parser.process_var(nested_line)
            elif nested_line.startswith("read"):
                Parser.process_read(nested_line)
            elif nested_line.startswith("write"):  
                Parser.process_write(line)
            elif '(' in nested_line and ')' in nested_line:  # Posibil apel de macro
                Parser.process_macro_call(nested_line, file)
            elif nested_line:
                Utils.write_in_file(f"{' ' * globals.spaces}{nested_line};")

        globals.spaces -= 4
        Utils.write_in_file(f"{' ' * globals.spaces}}}")

    @staticmethod
    def process_vector(vector):
        pattern = r'^([A-Za-z0-9_-]+)((\[[A-Za-z0-9_]+\])*)$'
        match = re.match(pattern, vector)
        if match:
            name = match.group(1)  # Extragem numele
            # Extragem toate valorile alfanumerice între paranteze pătrate
            indices = re.findall(r'\[([A-Za-z0-9_]+)\]', vector)
            for i in indices:
                try:
                    if int(i)<1:
                        Utils.write_in_file("Error:  index cannot be below 1!")
                        exit(1)
                except ValueError:
                    continue
            return name, indices
        else:
            Utils.write_in_file("Error: array sintax error")
            exit(1)

    @staticmethod
    def process_var(line):
        # Expresie regulată pentru a potrivi tipuri cu sau fără paranteze și parametri
        pattern = r'^var\s+([\w\s,]+):\s*([\w]+)(\([^)]*\))?$'
        match = re.match(pattern, line)
        if match:
            # Capturăm numele variabilelor și tipul, inclusiv parametrii, dacă există
            variables = re.split(r'\s*,\s*', match.group(1).strip())
            type_of_variable = match.group(2)
            params = match.group(3) if match.group(3) else ""
            
            if type_of_variable == "Integer":
                Utils.write_in_file(" " * globals.spaces, "long int", end=" ", sep="")
            elif type_of_variable == "Real":
                Utils.write_in_file(" " * globals.spaces, "long double", end=" ", sep="")
            else:
                Utils.write_in_file(" " * globals.spaces, type_of_variable, params, end=" ", sep="")

            # Inițializează declarația cu prima variabilă, dacă există
            if len(variables) > 0:
                Utils.write_in_file(variables[0], end="")

            for i in range(1, len(variables)):
                if "[" in variables[i] and "]" in variables[i]:
                    name, indices = Parser.process_vector(variables[i])
                    is_dynamic = False
                    for j in range(len(indices)):
                        try:
                            indices[j] = int(indices[j])
                        except ValueError:
                            is_dynamic = True
                            break
                    if is_dynamic:
                        globals.vectors.append([name, indices])
                    else:
                        Utils.write_in_file(",", name, '[' + ']['.join(str(item) for item in indices) + ']', sep="", end="")
                else:
                    Utils.write_in_file(", ", variables[i], end="", sep="")
            Utils.write_in_file(";")

            Utils.process_print_vector()
        else:
            Utils.write_in_file("Syntax error")

    def process_var_model(line):
        # Expresie regulată pentru a potrivi tipuri cu sau fără paranteze și parametri
        pattern = r'^var\s+([\w\s,]+):\s*([\w]+)(\([^)]*\))?$'
        match = re.match(pattern, line)
        if match:
            # Capturăm numele variabilelor și tipul, inclusiv parametrii, dacă există
            variables = re.split(r'\s*,\s*', match.group(1).strip())
            type_of_variable = match.group(2)
            params = match.group(3) if match.group(3) else ""
            
            if type_of_variable == "Integer":
                Utils.capture_print(" " * globals.spaces, "long int", end=" ", sep="")
            elif type_of_variable == "Real":
                Utils.capture_print(" " * globals.spaces, "long double", end=" ", sep="")
            else:
                Utils.capture_print(" " * globals.spaces, type_of_variable, params, end=" ", sep="")

            # Inițializează declarația cu prima variabilă, dacă există
            if len(variables) > 0:
                Utils.capture_print(variables[0], end="")

            for i in range(1, len(variables)):
                if "[" in variables[i] and "]" in variables[i]:
                    name, indices = Parser.process_vector(variables[i])
                    is_dynamic = False
                    for j in range(len(indices)):
                        try:
                            indices[j] = int(indices[j])
                        except ValueError:
                            is_dynamic = True
                            break
                    if is_dynamic:
                        globals.vectors.append([name, indices])
                    else:
                        Utils.capture_print(",", name, '[' + ']['.join(str(item) for item in indices) + ']', sep="", end="")
                else:
                    Utils.capture_print(", ", variables[i], end="", sep="")
            Utils.capture_print(";")

            Utils.process_print_vector_model()
        else:
            Utils.write_in_file("Syntax error")

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as Simulix:
            if file_path in globals.opened_files:
                Utils.write_in_file(f"Error: {file_path} was already opened and it will create a loop")
                exit(1)
            globals.opened_files.add(file_path)

            for line in Simulix:
                line = line.strip()

                if "include" in line:
                    Parser.process_include(line)
                elif line.startswith("def model"):
                    Parser.process_model(line, Simulix)
                elif line.startswith("//"):
                    continue
                elif line.startswith("read"):
                    Parser.process_read(line)
                elif line.startswith("write"):  
                    Parser.process_write(line)
                elif line.startswith("for"):
                    Parser.process_for(line, Simulix)
                elif line.startswith("while"):
                    Parser.process_while(line, Simulix)
                elif line.startswith("var"):
                    Parser.process_var(line)
                elif "macro" in line:
                    Parser.process_macro(line, Simulix)
                elif '(' in line and ')' in line:
                    Parser.process_macro_call(line,Simulix)
                elif line:
                    Utils.write_in_file(" " * globals.spaces + line)
        globals.opened_files.discard(file_path)

    @staticmethod
    def process_macro(line, file):
        # Scoatem "macro" din linie și separăm numele și parametrii
        line = line.replace('macro', '').strip()

        if '(' not in line or ')' not in line:
            Utils.write_in_file('Error: Sintaxă "macro" incorectă')
            exit(1)

        # Extragem numele macro-ului și parametrii
        macro_name, params = line.split('(')
        params = params.rstrip(')')

        # Acumulăm codul macro-ului până la 'end macro'
        macro_body = []
        for line in file:
            line = line.strip()
            if line == "end macro":
                break
            macro_body.append(line)

        # Salvăm definiția macro-ului în dicționar
        globals.macro_definitions[macro_name.strip()] = (params.split(','), macro_body)

    @staticmethod
    def process_macro_call(line, file):
        # Extragem numele macro-ului și parametrii apelului
        macro_call = line.split('(')[0].strip()
        params = line.split('(')[1].rstrip(')').split(',')

        if macro_call in globals.currently_processing:
            Utils.write_in_file(f"Error: Recursive macro call detected for '{macro_call}'")
            exit(1)

        globals.currently_processing.add(macro_call)

        # Verificăm dacă macro-ul este definit
        if macro_call in globals.macro_definitions:
            macro_params, macro_body = globals.macro_definitions[macro_call]

            # Verificăm dacă numărul de parametri din apel corespunde cu cel din definiție
            if len(params) != len(macro_params):
                Utils.write_in_file(f"Error: Macro '{macro_call}' expects {len(macro_params)} parameters, but {len(params)} were provided.")
                exit(1)

            # Procesăm corpul macro-ului
            for body_line in macro_body:
                # Procesăm 'var' dacă există
                if body_line.strip().startswith('var'):
                    Parser.process_var(body_line)
                    continue
                elif body_line.startswith("read"):
                    Parser.process_read(body_line)
                    continue
                elif body_line.startswith("write"):  
                    Parser.process_write(body_line)
                    continue
                elif body_line.startswith("for"):
                    Parser.process_for(body_line, file)
                    continue
                elif body_line.startswith("while"):
                    Parser.process_while(body_line, file)
                    continue
                
                # Înlocuim parametrii cu valorile corespunzătoare
                for i in range(len(macro_params)):
                    body_line = re.sub(r'\b' + re.escape(macro_params[i].strip()) + r'\b', params[i].strip(), body_line)

                # Afișăm linia procesată
                if body_line.strip():
                    Utils.write_in_file(f"{' ' * globals.spaces}{body_line.strip()}")

        else:
            Utils.write_in_file(f"Error: Macro '{macro_call}' not defined.")

        globals.currently_processing.remove(macro_call)