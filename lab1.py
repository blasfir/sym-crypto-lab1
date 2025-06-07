import re
import math


def remove_spaces(text):
    return re.sub(r"\s+", "", text)

def letter_frequencies(text, alphabet):
    result = [0] * len(alphabet)
    for char in text:
        if char in alphabet:
            result[alphabet.index(char)] += 1
    return result

def create_matrix(size):
    result = []
    for _ in range(size):
        row = [0] * size  
        result.append(row)
    return result

def frequeny_of_overlapping_bigrams(text, alphabet, matrix):
    for i in range(len(text) - 1):
        a, b = text[i], text[i + 1]
        if a in alphabet and b in alphabet:
            i1, i2 = alphabet.index(a), alphabet.index(b)
            matrix[i1][i2] += 1

def frequeny_of_nonoverlapping_bigrams(text, alphabet, matrix):
    for i in range(0, len(text) - 1, 2):
        a, b = text[i], text[i + 1]
        if a in alphabet and b in alphabet:
            i1, i2 = alphabet.index(a), alphabet.index(b)
            matrix[i1][i2] += 1

def fill_matrix(matrix, alphabet):
    width = 6
    result = " " * width + "".join(f"{ch:>{width}}" for ch in alphabet) + "\n"
    for i, j in enumerate(matrix):
        result += f"{alphabet[i]:<{width}}" + "".join(f"{count:>{width}}" for count in j) + "\n"
    return result

def calculate_H1(frequencies):
    total = sum(frequencies)
    result = 0
    for frequency in frequencies:
        if frequency > 0:
            p = frequency / total
            result -= p * math.log2(p)
    return result

def calculate_H2(bigram_matrix):
    total = 0
    for frequencies in bigram_matrix:
        for frequency in frequencies:
            total += frequency
    result = 0
    for frequencies in bigram_matrix:
        for frequency in frequencies:
            if frequency > 0:
                p = frequency / total
                result -= p * math.log2(p)
    result = result / 2            
    return result

def print_letter_frequencies(frequencies, alphabet, text_len, file):
    frequencies = frequencies.copy()
    alphabet = alphabet.copy()
    while frequencies:
        max_i = frequencies.index(max(frequencies))
        frequency = frequencies.pop(max_i)
        char = alphabet.pop(max_i)
        file.write(f"Літера '{char}' має частоту: {frequency / text_len:.5f}\n")

with open("text.txt", encoding="utf-8") as f:
    text = f.read().lower()

alphabet_with_space = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
alphabet_no_space = alphabet_with_space[:-1]

letter_frequencies_with_space = letter_frequencies(text, alphabet_with_space)
overlapping_bigram_matrix_with_space = create_matrix(len(alphabet_with_space))
frequeny_of_overlapping_bigrams(text, alphabet_with_space, overlapping_bigram_matrix_with_space)
nonoverlapping_bigram_matrix_with_space = create_matrix(len(alphabet_with_space))
frequeny_of_nonoverlapping_bigrams(text, alphabet_with_space, nonoverlapping_bigram_matrix_with_space)
H1_with_space = calculate_H1(letter_frequencies_with_space)
H2_with_space = calculate_H2(overlapping_bigram_matrix_with_space)
clean_text = remove_spaces(text)
letter_frequencies_no_space = letter_frequencies(clean_text, alphabet_no_space)
nonoverlapping_bigram_matrix_no_space = create_matrix(len(alphabet_no_space))
frequeny_of_nonoverlapping_bigrams(clean_text, alphabet_no_space, nonoverlapping_bigram_matrix_no_space)
H1_no_space = calculate_H1(letter_frequencies_no_space)
overlapping_bigram_matrix_no_space = create_matrix(len(alphabet_no_space))
frequeny_of_overlapping_bigrams(clean_text, alphabet_no_space, overlapping_bigram_matrix_no_space)
H2_no_space = calculate_H2(overlapping_bigram_matrix_no_space)

with open("text1.txt", "w", encoding="utf-8") as out:
    out.write("Біграми (перекривні):\n")
    out.write(fill_matrix(overlapping_bigram_matrix_with_space, alphabet_with_space))
    out.write("\n")

    out.write("Біграми (неперекривні):\n")
    out.write(fill_matrix(nonoverlapping_bigram_matrix_with_space, alphabet_with_space))
    out.write("\n")

    out.write(f"H1 (з пробілами): {H1_with_space:.5f}\n")
    out.write(f"H2 (з пробілами): {H2_with_space:.5f}\n\n")

    out.write(f"H1 (без пробілів): {H1_no_space:.5f}\n")
    out.write(f"H2 (без пробілів): {H2_no_space:.5f}\n\n")

    out.write("Найчастіші літери:\n")
    print_letter_frequencies(letter_frequencies_with_space, alphabet_with_space, len(text), out)