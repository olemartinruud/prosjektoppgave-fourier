#!/bin/env python3

# Man må installere python3.6, Pillow og numpy ved hjelp av pip install
# Altså etter man har installert python3.6 så må man skrive disse i et kommandovindu
#
# pip install Pillow
# pip install numpy
#
# Da skal det funke, hvis ikke spør meg
from PIL import Image
import numpy as np
import os
import json
from math import cos, pi
import re

IMAGE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bilder/fourier_bilder/'))
ANALYSERTE_BLOKKER_DIR = os.path.join(IMAGE_DIR, "analyserte_blokker/")

# Gjør om en array til en 1d array med pikselverdier. 3 ulike metoder (se "Prosjektoppgaven.mw")
def image_array_to_values_metode1(np_array):
    res = []
    for row in np_array:
        for value in row:
            res.append(value)
    return res

def values_to_image_array_metode1(value_array):
    np_array = [ [] for i in range(8) ]
    for i in range(8):
        for j in range(8):
            np_array[i].append(value_array[j + (i * 8)])

    return np.array(np_array, dtype=np.uint8)

def image_array_to_values_metode2(np_array):
    res = []
    reverse_row = False
    for row in np_array:
        altered_row = reversed(row) if reverse_row else row
        reverse_row = not reverse_row
        for value in altered_row:
            res.append(value)
    return res

def values_to_image_array_metode2(value_array):
    np_array = [ [] for i in range(8) ]
    reverse_row = False
    for i in range(8):
        for j in range(8):
            row_offset = j if not reverse_row else 7-j
            np_array[i].append(value_array[(i*8) + row_offset])
        reverse_row = not reverse_row
    return np.array(np_array, dtype=np.uint8)

def image_array_to_values_metode3(np_array):
    res = []
    increment_offset = 1
    x = 0
    y = 0

    res.append(np_array[y][x])

    for index in range(int(np_array.shape[0]/2)):
        for i in range(increment_offset, 0, -1):
            if(y > 0):
                y -= 1
            x += 1
            res.append(np_array[y][x])
            #print("X-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

        for i in range(increment_offset, 0, -1):
            if(x > 0):
                x -= 1
            y += 1
            res.append(np_array[y][x])
            #print("Y-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

    for index in range(int(np_array.shape[0]/2)):
        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(y > 0 and moved_over):
                y -= 1
            moved_over = True
            x += 1
            res.append(np_array[y][x])
            #print("X-loop: " + str(y) + str(x))

        increment_offset -= 1

        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(x > 0 and moved_over):
                x -= 1
            moved_over = True
            y += 1
            res.append(np_array[y][x])
            #print("Y-loop: " + str(y) + str(x))

        increment_offset -= 1

    return res

def values_to_image_array_metode3(value_array):
    np_array = np.indices((8,8))[0]
    increment_offset = 1
    x = 0
    y = 0

    reversed_value_array = list(reversed(value_array))

    np_array[y][x] = reversed_value_array.pop()

    for index in range(int(np_array.shape[0]/2)):
        for i in range(increment_offset, 0, -1):
            if(y > 0):
                y -= 1
            x += 1
            np_array[y][x] = reversed_value_array.pop()
            #print("X-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

        for i in range(increment_offset, 0, -1):
            if(x > 0):
                x -= 1
            y += 1
            np_array[y][x] = reversed_value_array.pop()
            #print("Y-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

    for index in range(int(np_array.shape[0]/2)):
        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(y > 0 and moved_over):
                y -= 1
            moved_over = True
            x += 1
            np_array[y][x] = reversed_value_array.pop()
            #print("X-loop: " + str(y) + str(x))

        increment_offset -= 1

        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(x > 0 and moved_over):
                x -= 1
            moved_over = True
            y += 1
            np_array[y][x] = reversed_value_array.pop()
            #print("Y-loop: " + str(y) + str(x))

        increment_offset -= 1

    return np.array(np_array, dtype=np.uint8)

#####################################################################################################
# Velg om du vil generere piecewise for maple eller lage et bilde fra psi(t) funksjonen.
GENERATE_PIECEWISE_BOOL = False

# Velg perioden til piecewise-kommandoen. Det vi har brukt før er 64
PERIODE = 64

# Velg indeksene for 8x8 blokken dere vil analysere! 0, 0 er den blokken øverst til venstre.
BLOCK_INDEXES = ( 11, 11 ) # VELG HVILKEN BLOKK AV 8x8 DERE VIL UNDERSØKE. (x, y)
# natur (22,26)
# kunstig (11,11)

# Skriv inn navnet på bildefilen. NB! Filen må ligge i mappen "fourier_bilder"
IMAGE_NAME = "kunstig.png"

# Endre denne variabelen til metoden dere ønsker. Fjern hastaggen foran metoden dere ønsker og putt en hastag forran alle metodene dere ikke vil bruke
#METHOD = image_array_to_values_metode1; REVERSE_METODE = values_to_image_array_metode1; METHOD_NAME = "metode1"
METHOD = image_array_to_values_metode2; REVERSE_METODE = values_to_image_array_metode2; METHOD_NAME = "metode2"
#METHOD = image_array_to_values_metode3; REVERSE_METODE = values_to_image_array_metode3; METHOD_NAME = "metode3"

# Her skrive man inn cosinusuttrykket fra maple! Sørg for at det ser riktig ut og at verdien fra cosinusuttrykket blir returnert fra funksjonen
# Bytt ut "255*cos(.4*t)" med det som kommer ut fra maple!
def psi(t):
<<<<<<< HEAD
    return 87.31250000-3.566504710*cos(.1472621557*t)+141.0276691*cos(0.4908738522e-1*t)+.985911939*cos(.2945243113*t)-30.20040468*cos(.1963495409*t)-19.82176616*cos(.2454369261*t)+64.69265187*cos(0.9817477044e-1*t)-5.785914227*cos(.4908738522*t)+11.87593921*cos(.3436116965*t)+9.888450648*cos(.3926990818*t)+1.725469068*cos(.4417864670*t)-8.730228779*cos(.8344855487*t)-8.052902122*cos(.5399612374*t)-3.278710526*cos(.5890486226*t)+4.938007688*cos(.6381360078*t)-5.852056005*cos(.7853981635*t)-2.248346107*cos(.8835729339*t)+6.159973590*cos(.9326603192*t)+7.475453779*cos(.9817477044*t)+8.610305090*cos(.6872233931*t)+3.258151057*cos(.7363107783*t)+1.287146206*cos(1.030835090*t)-4.999438596*cos(1.079922475*t)-5.420052033*cos(1.129009860*t)-3.142672782*cos(1.423534171*t)-2.335600308*cos(1.472621557*t)+3.729066048*cos(1.276272016*t)-1.094383682*cos(1.178097245*t)+2.971808007*cos(1.227184630*t)+1.643479624*cos(1.325359401*t)-1.312866830*cos(1.374446786*t)
=======
    return 87.31250000-26.28139678*cos(.6872233931*t)-.558105397*cos(.6381360078*t)-.4429782361*cos(.5890486226*t)-9.727022590*cos(.5399612374*t)+35.73977026*cos(.4417864670*t)-23.77173001*cos(.4908738522*t)-.2758849375*cos(1.276272016*t)+14.43287478*cos(1.325359401*t)+94.78152004*cos(.3926990818*t)-5.178799325*cos(1.374446786*t)+7.848280087*cos(1.472621557*t)-2.032607729*cos(1.423534171*t)+94.76072592*cos(0.4908738522e-1*t)+7.59868663*cos(0.9817477044e-1*t)+2.820123666*cos(.1472621557*t)+31.59389714*cos(.3436116965*t)-17.08111621*cos(.2945243113*t)-2.833511842*cos(.2454369261*t)+3.628188064*cos(.1963495409*t)-27.53698704*cos(.7363107783*t)+6.488675826*cos(.7853981635*t)-16.34303864*cos(.8344855487*t)-26.89808731*cos(.8835729339*t)+9.868053260*cos(.9817477044*t)+4.170214808*cos(.9326603192*t)+18.53256178*cos(1.030835090*t)+9.288161939*cos(1.079922475*t)-8.128108834*cos(1.129009860*t)+4.725676731*cos(1.178097245*t)-2.928708739*cos(1.227184630*t)
>>>>>>> 1e3afea5121ecbf8736f629d3eeb9b2b36497a78

####################################################################################################

class pf:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

   def format(text, l_pf):
       return l_pf + text + pf.END

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# Returnerer en 8x8 som er et resultat av psi(t)
def change_to_fourierseriesvalues(eight_by_eight, method_func, reverse_method_func):
    try:
        value_array = method_func(eight_by_eight)
        T = len(value_array)
    except:
        print("Error: Vennligst velg en \"method\" funksjon.")
        return eight_by_eight

    for i in range(T):
        value_array[i] = clamp(int(psi(i)), 0, 255)

    return reverse_method_func(value_array)

# Bredde og høyde på arrayen må være delelig på 8
def array_into_eight_by_eight(np_array):
    width = np_array.shape[0]
    height = np_array.shape[1]
    if(width % 8 > 0 or height % 8 > 0):
        return None
    # Les som en bok
    array_eight_by_eights = [ [] for i in range(int(height/8)+1) ]
    array_eight_by_eight_col_offset = 0

    for y_matrix in range(int(width/8)):
        n1 = np.arange(8*y_matrix, 8*y_matrix+8)
        for x_matrix in range(int(height/8)):
            n2 = np.arange(8*x_matrix, 8*x_matrix+8)
            array_eight_by_eights[array_eight_by_eight_col_offset].append(np_array[n1[:,None], n2[None,:]])

        array_eight_by_eight_col_offset += 1

    return array_eight_by_eights

# Gjør om en 2d array med 8x8 blokker til en stor 2d array med pikselverdier
def assembly_array_of_eight_by_eight(array_eight_by_eights):
    rows_eight_by_eight = []
    for row_eight_by_eight in array_eight_by_eights:
        rows_eight_by_eight.append(np.concatenate(row_eight_by_eight, axis=1))
    return np.concatenate(rows_eight_by_eight, axis=0)

# Gjør om en 2d array med pikselverdier til en png-bildefil
def numpyarray_to_image(np_array, filepath):
    new_image = Image.fromarray(np_array,'L')
    with open(filepath, 'wb') as image_file:
        new_image.save(image_file, 'PNG')

def numpyarray_to_image_scale(np_array, filepath, scalefactor):
    new_image = Image.fromarray(np_array,'L')
    with open(filepath, 'wb') as image_file:
        new_image.save(image_file, 'PNG')

# Gjør om en bildefil til en 2d array med pikselverdier (bare sort/hvitt)
def image_to_numpyarray(loaded_image):
    converted_image_file = loaded_image.convert('L')
    return np.reshape(np.array(converted_image_file.getdata(), np.dtype(np.uint8)), (-1, converted_image_file.width))

# Skriver en array til en json fil
def write_array_to_datafile(filepath, np_array):
    with open(filepath, "w") as json_file:
        json_str = json.dumps(np_array.tolist())
        json_str = re.sub(r'([0-9]+\],)','\g<1>\n', json_str)
        json_str = re.sub(r'([^\-]\b[0-9]{1}\b)','   \g<1>',json_str)
        json_str = re.sub(r'([\-]\b[0-9]{1}\b)|([^\-]\b[0-9]{2}\b)','  \g<1>\g<2>',json_str)
        json_str = re.sub(r'([\-]\b[0-9]{2}\b)|([^\-]\b[0-9]{3}\b)',' \g<1>\g<2>',json_str)
        json_file.write(json_str)

# Leser en json fil med en 2d array
def read_array_from_datafile(filepath):
    res_json = ""
    with open(filepath, 'r') as json_file:
        res_json = json.load(json_file)
    return res


# Ser om en mappe eksisterer og lager den hvis ikke den eksisterer. Returnerer dirpath
def check_directory(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return dirpath

# Gjør om 1d array med verdier til en piecewise kommando
def array_to_piecewise(array, periode):
    res = "f(t) := piecewise("
    roffset = 0
    array_len = len(array)
    increment = periode/array_len
    for value in array:
        res += str(roffset) + " <= t <= " + str(roffset+increment) + ", " + str(value) + ", "
        roffset += increment
    res = res.strip().strip(',')
    return res + ")"

# En funksjon som brukes tichange_to_fourierseriesvaluesl testing av et lite bilde
def test_main():
    image_data_name = "rocket_original.json"
    image_array = read_array_from_datafile(os.path.join(DATA_DIR, image_data_name))
    image_np_array = np.array(image_array, np.dtype(np.uint8))
    image_name = image_data_name.split('.')[0] + ".png"
    filepath = os.path.join(IMAGE_DIR, image_name)

    numpyarray_to_image(image_np_array, filepath)

    print("Lagret bilde: " + filepath)
    print("Piecewise metode 1:")
    print(array_to_piecewise(image_array_to_values_metode1(image_np_array)))
    print("Piecewise metode 2:")
    print(array_to_piecewise(image_array_to_values_metode2(image_np_array)))
    print("Piecewise metode 3:")
    print(array_to_piecewise(image_array_to_values_metode3(image_np_array)))

def generate_piecewise():
    image_name = IMAGE_NAME.split('.')[0]

    np_array = None
    with Image.open(os.path.join(IMAGE_DIR, IMAGE_NAME)) as big_image:
        np_array = image_to_numpyarray(big_image)

    array_eight_by_eights = array_into_eight_by_eight(np_array)

    print("Kjoerte " + pf.format(METHOD.__name__, pf.BOLD) + " paa bilde " + pf.format(IMAGE_NAME, pf.BOLD) + " med " + pf.format(str(PERIODE), pf.BOLD) + " som periode")
    print(array_to_piecewise(METHOD(array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]]), PERIODE))

def generate_image_from_psi():
    image_name = IMAGE_NAME.split('.')[0]

    print("Laster bilde: " + pf.format(IMAGE_NAME, pf.BOLD))
    np_array = None
    with Image.open(os.path.join(IMAGE_DIR, IMAGE_NAME)) as big_image:
        np_array = image_to_numpyarray(big_image)

    print("Skriver bildedata av hele bildet til json-filer.")
    write_array_to_datafile(os.path.join(IMAGE_DIR, image_name + ".json"), np_array)

    print("Genererer 8x8 blokker av det lastede bildet.")
    array_eight_by_eights = array_into_eight_by_eight(np_array)

    image_org_dir = check_directory(os.path.join(ANALYSERTE_BLOKKER_DIR, image_name, METHOD_NAME, "bilder", "org/"))
    image_fourier_dir = check_directory(os.path.join(ANALYSERTE_BLOKKER_DIR, image_name, METHOD_NAME, "bilder", "fourier/"))
    data_org_dir = check_directory(os.path.join(ANALYSERTE_BLOKKER_DIR, image_name, METHOD_NAME, "data", "org/"))
    data_fourier_dir = check_directory(os.path.join(ANALYSERTE_BLOKKER_DIR, image_name, METHOD_NAME, "data", "fourier/"))
    data_delta_dir = check_directory(os.path.join(ANALYSERTE_BLOKKER_DIR, image_name, METHOD_NAME, "data", "delta/"))

    print("Velger 8x8-blokken som skal analyseres: " + pf.format(str(BLOCK_INDEXES), pf.BOLD))
    print("Lager bilde av 8x8-blokken som skal analyseres før den endres.")
    org_eight_by_eight = array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]]
    numpyarray_to_image(org_eight_by_eight, os.path.join(image_org_dir, str(BLOCK_INDEXES) + ".png"))

    print("Skriver data av 8x8-blokken som skal analyseres før den endres.")
    write_array_to_datafile(os.path.join(data_org_dir, str(BLOCK_INDEXES) + ".json"), org_eight_by_eight)

    print(pf.format("Lager en ny 8x8 fra psi(t) funksjonen.", pf.BOLD))
    fourier_eight_by_eight = change_to_fourierseriesvalues(org_eight_by_eight, METHOD, REVERSE_METODE).astype(np.dtype(np.uint8))

    print("Lager bilde av 8x8-blokken som er generert fra psi(t).")
    numpyarray_to_image(fourier_eight_by_eight, os.path.join(image_fourier_dir, str(BLOCK_INDEXES) + ".png"))

    print("Skriver data av 8x8-blokken som er generert fra psi(t).")
    write_array_to_datafile(os.path.join(data_fourier_dir, str(BLOCK_INDEXES) + ".json"), fourier_eight_by_eight)

    print("Skriver data av 8x8-blokken som er forskjellen mellom pikselverdienen fra orginal og fourier")
    write_array_to_datafile(os.path.join(data_delta_dir, str(BLOCK_INDEXES) + ".json"), org_eight_by_eight.astype(np.dtype(np.int8)) - fourier_eight_by_eight.astype(np.dtype(np.int8)))

    print(pf.format("Fullført! Sjekk \"fourier_bilder\" mappen for oppdateringer!", pf.BOLD))

def run():
    if(GENERATE_PIECEWISE_BOOL):
        generate_piecewise()
    else:
        generate_image_from_psi()

def main():
    run()


if __name__ == '__main__':
    main()
