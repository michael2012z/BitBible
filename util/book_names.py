
def get_long_name(book_short_name):
    for testament in book_names:
        for book in testament:
            long_name, short_name = book
            if book_short_name == short_name:
                return long_name
    return ''

def get_short_name(book_long_name):
    for testament in book_names:
        for book in testament:
            long_name, short_name = book
            if book_long_name == long_name:
                return short_name
    return ''

def get_ot_short_names():
    names = []
    for book in book_names[0]:
        names.append(book[1])
    return names

def get_nt_short_names():
    names = []
    for book in book_names[1]:
        names.append(book[1])
    return names

book_names = [
    [
        ("Genesis", "Gen"),
        ("Exodus", "Exod"),
        ("Leviticus", "Lev"),
        ("Numbers", "Num"),
        ("Deuteronomy", "Deut"),
        ("Joshua", "Josh"),
        ("Judges", "Judg"),
        ("Ruth", "Ruth"),
        ("1 Samuel", "1Sam"),
        ("2 Samuel", "2Sam"),
        ("1 Kings", "1Kgs"),
        ("2 Kings", "2Kgs"),
        ("1 Chronicles", "1Chr"),
        ("2 Chronicles", "2Chr"),
        ("Ezra", "Ezra"),
        ("Nehemiah", "Neh"),
        ("Tobit", "Tob"),
        ("Judith", "Jdt"),
        ("Esther", "Esth"),
        ("Maccabees", "1 Macc"),
        ("2 Maccabees", "2 Macc"),
        ("Job", "Job"),
        ("Psalms", "Ps"),
        ("Proverbs", "Prov"),
        ("Ecclesiastes", "Eccl"),
        ("Song of Songs", "Song"),
        ("Canticles", "Cant"),
        ("Wisdom", "Wis"),
        ("Sirach", "Sir"),
        ("Isaiah", "Isa"),
        ("Jeremiah", "Jer"),
        ("Lamentations", "Lam"),
        ("Baruch", "Bar"),
        ("Ezekiel", "Ezek"),
        ("Daniel", "Dan"),
        ("Hosea", "Hos"),
        ("Joel", "Joel"),
        ("Amos", "Amos"),
        ("Obadiah", "Obad"),
        ("Jonah", "Jonah"),
        ("Micah", "Mic"),
        ("Nahum", "Nah"),
        ("Habakkuk", "Hab"),
        ("Zephaniah", "Zeph"),
        ("Haggai", "Hag"),
        ("Zechariah", "Zech"),
        ("Malachi", "Mal"),
    ],
    [
        ("Matthew", "Matt"),
        ("Mark", "Mark"),
        ("Luke", "Luke"),
        ("John", "John"),
        ("Acts", "Acts"),
        ("Romans", "Rom"),
        ("1 Corinthians", "1Cor"),
        ("2 Corinthians", "2Cor"),
        ("Galatians", "Gal"),
        ("Ephesians", "Eph"),
        ("Philippians", "Phil"),
        ("Colossians", "Col"),
        ("1 Thessalonians", "1Thess"),
        ("2 Thessalonians", "2Thess"),
        ("1 Timothy", "1Tim"),
        ("2 Timothy", "2Tim"),
        ("Titus", "Titus"),
        ("Philemon", "Phlm"),
        ("Hebrews", "Heb"),
        ("James", "Jas"),
        ("1 Peter", "1Pet"),
        ("2 Peter", "2Pet"),
        ("1 John", "1John"),
        ("2 John", "2John"),
        ("3 John", "3John"),
        ("Jude", "Jude"),
        ("Revelation", "Rev"),
    ],
]
