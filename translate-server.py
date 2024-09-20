import socket

# Dictionary of English to Japanese translations
word_translations = {
    "hello": "こんにちは (konnichiwa)",
    "goodbye": "さようなら (sayōnara)",
    "i": "私 (watashi)",
    "name": "名前 (namae)",
    "love": "愛 (ai)",
    "japan": "日本 (nihon)",
    "english": "英語 (eigo)",
    "student": "学生 (gakusei)",
    "teacher": "先生 (sensei)",
    "friend": "友達 (tomodachi)",
    "book": "本 (hon)",
    "pen": "ペン (pen)",
    "notebook": "ノート (nōto)",
    "computer": "コンピューター (konpyūtā)",
    "laptop": "パソコン (pasokon)",
    "school": "学校 (gakkō)",
    "college": "大学 (daigaku)",
    "job": "仕事 (shigoto)",
    "study": "勉強する (benkyōsuru)",
    "read": "読む (yomu)",
    "tv": "テレビ (terebi)",
    "movie": "映画 (eiga)",
    "music": "音楽 (ongaku)",
    "family": "家族 (kazoku)",
    "house": "家 (ie)",
    "person": "人 (hito)",
    "cat": "猫 (neko)",
    "dog": "犬 (inu)",
    "car": "車 (kuruma)",
    "bus": "バス (basu)",
    "eat": "食べる (taberu)",
    "food": "食べ物 (tabemono)",
    "water": "水 (mizu)",
    "menu": "メニュー (	menyuu)",
    "delicious": "おいしい (oishī)",
    "city": "都市 (toshi)",
    "big": "大きい (ōkī)",
    "small": "小さい (chīsai)",
    "cheap": "やすい (yasui)",
    "expensive": "高い (takai)",
    "happy": "幸せ (shiawase)",
    "sad": "悲しい (kanashī)",
    "beautiful": "美しい (utsukushī)",
    "new": "新しい (atarashī)",
    "old": "古い (furui)", 
    "strong": "強い (tsuyoi)",
    "fast": "速い (hayai)",
    "slow": "遅い (osoi)",
    "hot": "暑い (atsui)",
    "cold": "寒い (samui)",
}

# Number of lessons and words per lessons
LESSONS_COUNT = 10
WORDS_PER_LESSON = 5

def generate_lessons(word_translations):
    """
    Generate lessons from the word_translations dictionary

    Parameters:
    word_translations (dictionary): The dictionary of word translation.

    Returns:
    dict: The vocabulary lessons.
    """
    lessons = {}
    words = list(word_translations.items())
    
    for i in range(LESSONS_COUNT):
        lesson_start = i * WORDS_PER_LESSON
        lesson_end = lesson_start + WORDS_PER_LESSON
        lesson_words = dict(words[lesson_start:lesson_end])
        
        if lesson_words:
            lessons[i + 1] = lesson_words   # Assign the lesson to its number
    
    return lessons

# Create lessons
lessons = generate_lessons(word_translations)


def handle_request(data):
    """
    Processes a client's request.
    The function supports two commands:
    - 'translate <word>': Returns the Japanese translation of the provided English word.
    - 'learn <lesson_number>': Returns a list of vocabulary words for the specified lesson.

    Parameters:
    data (str): The command as a string (E.g: translate hello, learn 1).
    
    Returns:
    str: The response based on the command.
        - If 'translate': Returns the translation of the provided word.
        - If 'learn': Returns vocabulary words from the specified lesson.
    """

    commands = data.lower().split()
    if len(commands) != 2 or commands[0] not in ["learn", "translate"]:
        return "Unknown command. Try again."
    
    elif commands[0] == "learn":
        try:
            # Attempt to convert a non-integer string to an integer
            lesson_number = int(commands[1])  # This will raise a ValueError
        except ValueError as e:
            print(f"ValueError: {e}. Lesson number must be an integer between 1 and 10.")
            return "Unknown command. Try again."
        
        return learn_vocabulary(lesson_number)
    
    elif commands[0] == "translate":
        word = commands[1]
        return translate_word(word)
    
    return "Unknown command. Try again."


def translate_word(word):
    """
    Translates an English word to Japanese using the word_translations dictionary.

    Parameters:
    word (str): The English word to be translated.

    Returns:
    str: The Japanese translation if the word is in the dictionary, or "Translation not found. Try again." if the word is not in the dictionary.    
    """
    return word_translations.get(word, "Translation not found. Try again.")


def learn_vocabulary(lesson_number):
    """
    Returns the vocabulary for a given lesson number.
    
    Parameters:
    lesson_number (int): The lesson to be learned.
    
    Returns:
    str: A formatted string containing the lesson number and vocabulary list, or "Lesson not found. Try again." if the lesson is not available.
    """
    lesson = lessons.get(lesson_number, {})
    
    if not lesson:
        return "Lesson not found. Try again."
    
    vocab_list = '\n'.join([f"{eng}: {jpn}" for eng, jpn in lesson.items()])
    return f"Lesson {lesson_number} vocabulary:\n{vocab_list}"


def main():
    HOST = '127.0.0.1'
    PORT = 65432

    print("Server starting - Listening for connections at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection established with {addr}.")
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received client request: '{data!r}' [{len(data)} bytes]")
                    response = handle_request(data)
                    print(f"Sending response back to client.")
                    conn.sendall(response.encode())

            # Close the connection after successful request
            if response not in ["Unknown command. Try again.", "Translation not found. Try again.", "Lesson not found. Try again."]:
                break
    
    print("Server is done!")

if __name__ == "__main__":
    main()