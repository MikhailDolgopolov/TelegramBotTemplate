import random
import nltk
try:
    from nltk.corpus import wordnet
except LookupError:
    # Если не загружен, загружаем WordNet
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    from nltk.corpus import wordnet


from translate import Translator
from nltk.stem import WordNetLemmatizer

def get_nouns():
    filename = 'common_nouns.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            common_nouns = [line.strip() for line in f]
        print("Список common_nouns загружен из файла.")
    except FileNotFoundError:
        print("Файл не найден. Генерируем список из WordNet...")

        # Получаем все существительные (nouns) из WordNet
        all_nouns = list(wordnet.all_lemma_names(pos='n'))

        # Фильтруем только нарицательные существительные, исключая собственные имена
        common_nouns = [noun for noun in all_nouns if noun.islower()]

        print(len(all_nouns)-len(common_nouns))

        # Записываем список common_nouns в файл
        with open(filename, 'w', encoding='utf-8') as f:
            for noun in common_nouns:
                f.write(noun + '\n')

        print("Список common_nouns записан в файл.")
    return common_nouns


def get_word(common_nouns):
    translator = Translator(to_lang="ru")


    # Генерация случайного слова
    word = translation = "_"
    while word.lower() == translation.lower() or " " in translation or not translation.islower():
        word = random.choice(common_nouns)
        while '_' in word:
            word = random.choice(common_nouns)

        translation = translator.translate(word)

    # Создаем объект лемматизатора
    lemmatizer = WordNetLemmatizer()
    print(word, translation)
    return lemmatizer.lemmatize(translation, pos='n').lower()


arr = get_nouns()
for i in range(20):
    print(get_word(arr))

