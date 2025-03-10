import globals
import re
from utils import Utils
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr

class Generator:
    @staticmethod
    def floatA():
        Utils.write_in_file("//Coeficientii lui t")
        Utils.write_in_file("float A(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")

        for iteration in range(len(globals.final_coefficients["t"])):
            Utils.write_in_file(" " * globals.spaces, "case ", iteration + 1, ": return ", "*".join(map(str, globals.final_coefficients["t"][iteration])), end=";\n", sep="")
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")
    
    @staticmethod
    def floatgradA():
        Utils.write_in_file("float gradA(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i,j)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")

        for iteration in range(len(globals.final_coefficients["t"])):
            S = symbols('S')
            f = parse_expr("*".join(map(str, globals.final_coefficients["t"][iteration])), local_dict={'S': S})
            Utils.write_in_file(" "*globals.spaces,"case ",iteration+1,":",sep="")
            globals.spaces+=4
            Utils.write_in_file(' ' * globals.spaces,"switch(j)\n",' ' * globals.spaces,"{",sep="")
            for iteration_2 in range(len(globals.main_variables)):
                deriv=parse_expr(globals.main_variables[iteration_2], local_dict={'S':S})
                Utils.write_in_file(' ' * (globals.spaces+4), "//Coeficientul: ",f,sep="")
                Utils.write_in_file(' ' * (globals.spaces+4), "//Derivata de: ",deriv,sep="")
                Utils.write_in_file(" "*(globals.spaces+4),"case ",iteration_2+1,": return ",diff(f,deriv),end=";\n",sep="")
                Utils.write_in_file()
            Utils.write_in_file(' '*globals.spaces,"}",sep="")
            globals.spaces-=4
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")

    @staticmethod
    def hessgradA():
        Utils.write_in_file("float hessA(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i,j,k)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")

        for iteration in range(len(globals.final_coefficients["t"])):
            S = symbols('S')
            f = parse_expr("*".join(map(str, globals.final_coefficients["t"][iteration])), local_dict={'S': S})
            Utils.write_in_file(" "*globals.spaces,"case ",iteration+1,":",sep="")
            globals.spaces+=4
            Utils.write_in_file(' ' * globals.spaces,"switch(j)\n",' ' * globals.spaces,"{",sep="")
            for iteration_2 in range(len(globals.main_variables)):
                deriv=parse_expr(globals.main_variables[iteration_2], local_dict={'S':S})
                first_diff=diff(f,deriv)
                Utils.write_in_file(" "*(globals.spaces+4),"case ",iteration_2+1,":",sep="")
                globals.spaces+=4
                Utils.write_in_file(' ' * (globals.spaces+4),"switch(k)\n",' ' * (globals.spaces+4),"{",sep="")
                globals.spaces+=4
                for iteration_3 in range(len(globals.main_variables)):
                    deriv_2=parse_expr(globals.main_variables[iteration_3], local_dict={'S':S})
                    Utils.write_in_file(' ' * (globals.spaces+4), "//Coeficientul: ",f,sep="")
                    Utils.write_in_file(' ' * (globals.spaces+4), "//Prima derivare de: ",deriv,sep="")
                    Utils.write_in_file(' ' * (globals.spaces+4), "//Prima derivare: ",first_diff,sep="")
                    Utils.write_in_file(' ' * (globals.spaces+4), "//A doua derivare de: ",deriv_2,sep="")
                    Utils.write_in_file(" "*(globals.spaces+4),"case ",iteration_3+1,": return ",diff(first_diff,deriv_2),end=";\n",sep="")
                    Utils.write_in_file()
                Utils.write_in_file(' '*globals.spaces,"}",sep="")
                globals.spaces-=8
            Utils.write_in_file(' '*globals.spaces,"}",sep="")
            globals.spaces-=4
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")

    @staticmethod
    def floatB():
        Utils.write_in_file("// Reestul coeficientilor: ")
        Utils.write_in_file("float B(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i,j)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")
        for iteration in range(len(globals.main_variables)):
            Utils.write_in_file(" "*(globals.spaces),"case ",iteration+1,":",sep="")
            Utils.write_in_file(' ' * (globals.spaces+4),"switch(j)\n",' ' * (globals.spaces+4),"{",sep="")
            for iteration_2 in range(len(globals.other_diff_coeffs)):
                Utils.write_in_file(" "*(globals.spaces+8),"case ",iteration_2+1,": return ","*".join(map(str, globals.other_diff_coeffs[iteration_2][iteration])),end=";\n",sep="")
            Utils.write_in_file(" "*(globals.spaces+4),"}",sep="")
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")
        
    @staticmethod
    def floatgradB():
        Utils.write_in_file("float gradB(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i,j,derivi)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")
        for iteration in range(len(globals.main_variables)):
            W1,S = symbols('W1 S')

            Utils.write_in_file(" "*(globals.spaces),"case ",iteration+1,":",sep="")
            Utils.write_in_file(' ' * (globals.spaces+4),"switch(j)\n",' ' * (globals.spaces+4),"{",sep="")
            for iteration_2 in range(len(globals.other_diff_coeffs)):
                f = parse_expr("*".join(map(str, globals.other_diff_coeffs[iteration_2][iteration])), local_dict={'S': S})
                Utils.write_in_file(" "*(globals.spaces+8),"case ",iteration_2+1,":",sep="")
                Utils.write_in_file(' ' * (globals.spaces+12),"switch(k)\n",' ' * (globals.spaces+12),"{",sep="")
                for iteration_3 in range(len(globals.main_variables)):
                    deriv=parse_expr(globals.main_variables[iteration_3], local_dict={'S':S})
                    Utils.write_in_file(' ' * (globals.spaces+16), "//Coeficientul: ",f,sep="")
                    Utils.write_in_file(' ' * (globals.spaces+16), "//Derivata de: ",deriv,sep="")
                    Utils.write_in_file(" "*(globals.spaces+16),"case ",iteration_3+1,": return ",diff(f,deriv),end=";\n",sep="")
                    Utils.write_in_file()
                Utils.write_in_file(" "*(globals.spaces+12),"}",sep="")
            Utils.write_in_file(" "*(globals.spaces+4),"}",sep="")
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")
    
    @staticmethod
    def floathessB():
        Utils.write_in_file("float hessB(",end="")
        for iteration in globals.main_variables:
            Utils.write_in_file(iteration,",",sep="",end="")
        Utils.write_in_file("i,j,k,l)")
        globals.spaces+=8
        Utils.write_in_file(' ' * (globals.spaces-8),"{\n",' ' * (globals.spaces-4),"switch(i)\n",' ' * (globals.spaces-4),"{",sep="")
        for iteration in range(len(globals.main_variables)):
            W1,S = symbols('W1 S')

            Utils.write_in_file(" "*(globals.spaces),"case ",iteration+1,":",sep="")
            Utils.write_in_file(' ' * (globals.spaces+4),"switch(j)\n",' ' * (globals.spaces+4),"{",sep="")
            for iteration_2 in range(len(globals.other_diff_coeffs)):
                f = parse_expr("*".join(map(str, globals.other_diff_coeffs[iteration_2][iteration])), local_dict={'S': S})
                Utils.write_in_file(" "*(globals.spaces+8),"case ",iteration_2+1,":",sep="")
                Utils.write_in_file(' ' * (globals.spaces+12),"switch(k)\n",' ' * (globals.spaces+12),"{",sep="")
                for iteration_3 in range(len(globals.main_variables)):
                    deriv=parse_expr(globals.main_variables[iteration_3], local_dict={'S':S})
                    first_diff=diff(f,deriv)
                    Utils.write_in_file(" "*(globals.spaces+16),"case ",iteration_3+1,end=";\n",sep="")
                    Utils.write_in_file(' ' * (globals.spaces+20),"switch(l)\n",' ' * (globals.spaces+20),"{",sep="")
                    globals.spaces+=4
                    for iteration_4 in range(len(globals.main_variables)):
                        deriv_2=parse_expr(globals.main_variables[iteration_4], local_dict={'S':S})
                        Utils.write_in_file(" "*(globals.spaces+20),"//Coeficient: ",f,sep="")
                        Utils.write_in_file(" "*(globals.spaces+20),"//Derivata de: ",deriv,sep="")
                        Utils.write_in_file(" "*(globals.spaces+20),"//Prima derivare: ",first_diff,sep="")
                        Utils.write_in_file(" "*(globals.spaces+20),"//Derivata de: ",deriv_2,sep="")
                        Utils.write_in_file(" "*(globals.spaces+20),"case ",iteration_4+1,": return ",diff(first_diff,deriv_2),end=";\n",sep="")
                        Utils.write_in_file()
                    Utils.write_in_file(" "*(globals.spaces+16),"}",sep="")
                    globals.spaces-=4
                Utils.write_in_file(" "*(globals.spaces+12),"}",sep="")
            Utils.write_in_file(" "*(globals.spaces+4),"}",sep="")
        globals.spaces-=8
        Utils.write_in_file(" "*(globals.spaces+4),"}\n"," "*globals.spaces,"}",sep="")

    
    def process_equation_coefficients():
        # Prima parcurgere pentru a colecta toate variabilele
        for equation in globals.equations:
            first_diff = re.search(r"diff\((.*?)\)\s*=", equation)
            if first_diff:
                globals.main_variables.append(first_diff.group(1))
            
            right_side = equation.split('=')[1]
            vars_in_diffs = re.findall(r'diff\(([a-zA-Z0-9]+)\)', right_side)
            globals.all_variables.update(vars_in_diffs)
        
        all_variables_list = sorted(list(globals.all_variables))
        
        # A doua parcurgere pentru a procesa coeficienții
        for equation in globals.equations:
            right_side = equation.split('=')[1].strip()
            terms = right_side.split('+')
            
            current_coefficients = {var: ['0'] for var in all_variables_list}
            
            for term in terms:
                # Găsește variabila din diff()
                diff_match = re.search(r'diff\(([a-zA-Z0-9]+)\)', term)
                if diff_match:
                    var = diff_match.group(1)
                    # Extrage coeficientul (tot ce e înaintea diff)
                    coef = term[:diff_match.start()].strip()
                    
                    # Curăță coeficientul
                    if coef:
                        if coef.startswith('+'):
                            coef = coef[1:]
                        coef = coef.strip()
                        if coef.endswith('*'):
                            coef = coef[:-1]
                        if not coef:
                            coef = '1'
                    else:
                        coef = '1'
                    
                    current_coefficients[var] = [coef]
            
            globals.equations_coefficients.append(current_coefficients)
        
        # Reorganizează coeficienții
        for var in all_variables_list:
            globals.final_coefficients[var] = []
            for eq_coef in globals.equations_coefficients:
                globals.final_coefficients[var].append(eq_coef[var])
        
        # Separă coeficienții pentru diferite variabile decât 't'
        for key in globals.final_coefficients:
            if key == "t":
                continue
            globals.other_diff_coeffs.append(globals.final_coefficients[key])
