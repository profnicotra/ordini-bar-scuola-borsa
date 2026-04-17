numero = 0 
fattore = 1 

# Corretti gli errori di battitura (while, fattore)
# Nota: questa condizione specifica si ferma subito perché 
# 0 è uguale a (0 + 1 * 7) - 7.
while numero != (numero + fattore * 7) - (fattore * 7): 
    fattore += 1 

numero = numero + fattore * 7 - fattore
print(numero) # Corretto prin in print
