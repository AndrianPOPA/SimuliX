from parser import Parser
from generator import Generator
from utils import Utils
import globals

if __name__ == "__main__":
    # Pornim programul
    Utils.reset_file()
    Utils.write_in_file("# include \"simulix.h\"")
    Utils.write_in_file("int main()")
    Utils.write_in_file("{")
    Parser.read_file("main.smlx")
    Utils.write_in_file("}")

    Generator.process_equation_coefficients()
    Utils.write_in_file("\nVariabile principale:", globals.main_variables)
    Utils.write_in_file("\nToate variabilele:", sorted(list(globals.all_variables)))
    Utils.write_in_file("\nCoeficienți reorganizați:")
    Utils.write_in_file(globals.final_coefficients)
    Generator.floatA()
    Generator.floatgradA()
    Generator.hessgradA()
    Generator.floatB()
    Generator.floatgradB()
    Generator.floathessB()
