# Set ce conține fișierele deschise pentru evitarea buclelor
opened_files = set()

# Dicționar pentru a stoca definițiile macro-urilor
macro_definitions = {}  

# Set pentru a urmări macro-urile în curs de procesare (pentru a evita recursivitatea infinită)
currently_processing = set()  

# Lista pentru a ține evidența vectorilor declarați
vectors = []

# Variabilă globală pentru a ține evidența indentării
spaces = 4

equations=[]
main_variables = []
all_variables = set()
equations_coefficients = []
final_coefficients = {}
other_diff_coeffs=[]