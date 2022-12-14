import math

# Nacteni souboru
def load_file(filename:str):
    with open(filename, 'r', encoding='cp1250') as file:
        lines = file.readlines()
    file.close()
    return lines

def load_training_file(filename:str):
    words_lines = []
    with open(filename, 'r', encoding='cp1250') as file:
        for line in file:
            sentence_without_newline_char = line.rstrip()
            sentence = "".join('<s> ' + sentence_without_newline_char + ' </s>')
            words_lines.append(sentence)
    file.close()

    return words_lines # list listu (list vet), kde list = 1 veta

def delete_new_lines(words:list):
    words_pomocna = []
    for word in words:
        words_pomocna.append(word.strip('\n'))
    return words_pomocna

def create_training_set(training:list):
    words_set = set()
    for sentence in training:
        for word in sentence:
            words_set.add(word)

    return words_set

def create_ngrams(list_words_in_sentences:list, n:int):
    n_grams_result = []
    for sentence in list_words_in_sentences:
        n_grams = []
        for i in range(len(sentence)):
            n_grams.append(sentence[i: i + n])
        n_grams_result.append(n_grams)

    return n_grams_result

def create_dictionary(ngrams_sentences:list, n:int):
    dictionary = {}
    for ngram_sentence in ngrams_sentences:
        for ngram in ngram_sentence:
            if len(ngram) == n: # smazani kratsich ngramu
                key = " ".join(ngram)
                if key not in dictionary:
                    dictionary[key] = 1
                else:
                    dictionary[key] += 1
    return dictionary

def get_words_train(train_sentences:list):
    words_list = []
    for sentence in train_sentences:
        words = sentence.split(" ")
        words_list.append(words)
    return words_list # list listu slov jednotlivych vet

def get_list_from_lists(list_of_lists: list):
    result_list = []
    for sublist in list_of_lists:
        for item in sublist:
            result_list.append(item)
    return result_list

def check_words_dictionary(list_sentence_words:list, dictionary:set):
    for sentence_words in list_sentence_words:
        idx = -1
        for word in sentence_words:
            idx += 1
            if word not in dictionary:
                sentence_words[idx] = '<unk>'
    return list_sentence_words

def change_format_ngrams(ngrams:list):
    result_list = []
    for ngram in ngrams:
        if not '<unk>' in ngram:
            new_format = ''.join(map(str, ngram))
            result_list.append(new_format)
    return result_list

def trimm_off_trigrams(trigrams:dict, frequency:int):
    keys_to_delete = []
    for key in trigrams:
        if trigrams[key] == frequency:
            keys_to_delete.append(key)

    for key_delete in keys_to_delete:
        del trigrams[key_delete]

def count_words(words_list:list):
    counter = 0
    for word in words_list:
        if word == '</s>':
            counter += 0
        else:
            counter += 1

    return counter

def create_ARPA_file(zerograms:int, unigrams:dict, bigrams:dict, trigrams:dict):
    f = open("language_model.txt", "w", encoding="cp1250")
    f.write("\\data\\\nngram 1 = " + str(len(unigrams)) + "\nngram 2 = " + str(len(bigrams)) + "\nngram 3 = " + str(len(trigrams)) + "\n")

    cardinality = len(unigrams)
    delta = 0

    f.write("\n\\1-grams: \n")
    for unigram, freq in sorted(unigrams.items()):
        prob = math.log10(float(freq + delta) / (zerograms + delta * cardinality))
        f.write(f"{prob} {unigram}\n")

    f.write("\n\\2-grams: \n")
    for bigram, freq in sorted(bigrams.items()):
        bigram_list = list(bigram.split(" "))
        prob = math.log10(float(freq + delta) / (unigrams[(bigram_list[0])] + delta * cardinality))
        f.write(f"{prob} {bigram_list[0]} {bigram_list[1]}\n")

    f.write("\n\\3-grams: \n")
    for trigram, freq in sorted(trigrams.items()):
        trigram_list = list(trigram.split(" "))
        prob = math.log10(float(freq + delta) / (bigrams[(trigram_list[0] + " " + trigram_list[1])] + delta * cardinality))
        f.write(f"{prob} {trigram_list[0]} {trigram_list[1]} {trigram_list[2]}\n")

    f.write("\\end\\")
    f.close()

if __name__ == "__main__":
    words_list = load_file('cestina.txt')
    training_list = load_training_file('train.txt')

    words_list_final = delete_new_lines(words_list)
    words_set = set(words_list_final)
    words_set.add("<s>")
    words_set.add("</s>")

    training_list_final = get_words_train(training_list)
    list_sentences_words = check_words_dictionary(training_list_final, words_set) # zbaveni se preklepu
    words_list = get_list_from_lists(list_sentences_words)

    zerograms = count_words(words_list)
    unigrams = create_ngrams(list_sentences_words, 1)
    bigrams = create_ngrams(list_sentences_words, 2)
    trigrams = create_ngrams(list_sentences_words, 3)

    unigrams_dictionary = create_dictionary(unigrams, 1)
    bigrams_dictionary = create_dictionary(bigrams, 2)
    trigrams_dictionary = create_dictionary(trigrams, 3)

    trimm_off_trigrams(trigrams_dictionary, 1)

    create_ARPA_file(zerograms, unigrams_dictionary, bigrams_dictionary, trigrams_dictionary)
    print()