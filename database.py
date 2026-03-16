import sqlite3

conn = sqlite3.connect("words.db")
cursor = conn.cursor()


def add_word(user_id, word, translation):

    word_check = word.lower()

    cursor.execute(
        "SELECT * FROM words WHERE user_id = ? AND lower(word) = ?",
        (user_id, word_check)
    )

    existing = cursor.fetchone()

    if existing:
        return False

    word = word.capitalize()
    translation = translation.capitalize()

    cursor.execute(
        "INSERT INTO words (user_id, word, translation) VALUES (?, ?, ?)",
        (user_id, word, translation)
    )

    conn.commit()

    return True


def get_words(user_id):

    cursor.execute(
        "SELECT word, translation FROM words WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchall()