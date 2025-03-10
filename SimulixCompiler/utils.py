import globals

class OutputBuffer:
    """O clasă simplă pentru a stoca și manipula output-ul capturat"""
    def __init__(self):
        self.content = ""
    
    def __str__(self):
        return self.content

# Creăm un singur obiect buffer care va fi refolosit
output_buffer = OutputBuffer()

class Utils:
    @staticmethod
    def write_in_file(*args, sep=" ", end="\n", file_name="output.txt"):
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(sep.join(map(str, args)) + end)
    
    @staticmethod
    def read_file_model(file_name="output.txt"):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                return f.readlines()
        except FileNotFoundError:
            return []
        
    @staticmethod
    def insert_before_of(before_of, *args, sep=" ", end="\n", file_name="output.txt"):
        linii = Utils.read_file_model(file_name)
        text_formatat = sep.join(map(str, args)) + (end if end != "" else "")  # Creează textul de adăugat
        gasit = False

        with open(file_name, "w", encoding="utf-8") as f:
            for linie in linii:
                if linie.strip() == before_of.strip():
                    f.write(text_formatat)  # Scriem textul înainte de linia găsită
                    gasit = True
                f.write(linie)  # Scriem linia curentă

        if not gasit:
            Utils.write_in_file(f"Atenție: '{before_of}' nu a fost găsit în {file_name}!")

    @staticmethod
    def reset_file(file_name="output.txt"):
        with open(file_name, "w", encoding="utf-8") as f:
            pass  # Deschide fișierul în mod write și îl golește

    @staticmethod
    def capture_print(*args, sep=' ', end='\n'):
        # Convertim argumentele la string-uri și le unim cu sep
        output_string = sep.join(str(arg) for arg in args)
        
        # Adăugăm la rezultatul existent
        output_buffer.content += output_string + end
        
        # Returnăm obiectul buffer (același de fiecare dată)
        return output_buffer
    
    @staticmethod
    def clear_captured_output():
        output_buffer.content = ""
        return output_buffer
    
    @staticmethod
    def process_print_vector():
        for vector in globals.vectors:
            number_of_indices=len(vector[1])
            Utils.write_in_file(" " * globals.spaces,"long int","*" * number_of_indices," ",vector[0]," = new long int","*" * (number_of_indices-1),
                "[",vector[1][0],"];",sep="")
            if number_of_indices>1:
                Utils.process_new_int_vector(vector[0],vector[1],1,number_of_indices)

    @staticmethod
    def process_print_vector_model():
        for vector in globals.vectors:
            number_of_indices=len(vector[1])
            Utils.capture_print(" " * globals.spaces,"long int","*" * number_of_indices," ",vector[0]," = new long int","*" * (number_of_indices-1),
                "[",vector[1][0],"];",sep="")
            if number_of_indices>1:
                Utils.process_new_int_vector_model(vector[0],vector[1],1,number_of_indices)

    @staticmethod
    def process_new_int_vector(name,indices,iteration,number_of_indices):
        Utils.write_in_file(" " * globals.spaces,"for ( int ","i"+str(iteration)," = 0; ","i"+str(iteration)," < ",indices[iteration-1],"; ++",
            "i"+str(iteration),")",sep="")
        Utils.write_in_file(" " * globals.spaces, "{",sep="")
        globals.spaces+=4
        Utils.write_in_file(" " * globals.spaces,name, ''.join(f'[{f"i{i+1}"}]' for i in range(iteration))," = new long int",
            "*" * (number_of_indices-iteration-1),"[",indices[iteration],"];",sep="")
        if number_of_indices-1!=iteration:
            Utils.process_new_int_vector(name,indices,iteration+1,number_of_indices)
        globals.spaces-=4
        Utils.write_in_file(" " * globals.spaces,"}",sep="")

    @staticmethod
    def process_new_int_vector_model(name,indices,iteration,number_of_indices):
        Utils.capture_print(" " * globals.spaces,"for ( int ","i"+str(iteration)," = 0; ","i"+str(iteration)," < ",indices[iteration-1],"; ++",
            "i"+str(iteration),")",sep="")
        Utils.capture_print(" " * globals.spaces, "{",sep="")
        globals.spaces+=4
        Utils.capture_print(" " * globals.spaces,name, ''.join(f'[{f"i{i+1}"}]' for i in range(iteration))," = new long int",
            "*" * (number_of_indices-iteration-1),"[",indices[iteration],"];",sep="")
        if number_of_indices-1!=iteration:
            Utils.process_new_int_vector_model(name,indices,iteration+1,number_of_indices)
        globals.spaces-=4
        Utils.capture_print(" " * globals.spaces,"}",sep="")