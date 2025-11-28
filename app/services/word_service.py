import random

# Mock word database
WORDS_DB = [
    {
        "word": "Runway",
        "part_of_speech": "Noun",
        "meaning": "A long, flat surface along which aircraft take off and land",
        "example": "The plane landed on the runway smoothly"
    },
    {
        "word": "Serendipity",
        "part_of_speech": "Noun",
        "meaning": "The occurrence of events by chance in a happy way",
        "example": "Finding that book was pure serendipity"
    },
    {
        "word": "Resilient",
        "part_of_speech": "Adjective",
        "meaning": "Able to recover quickly from difficult conditions",
        "example": "The community proved resilient after the disaster"
    },
    {
        "word": "Ephemeral",
        "part_of_speech": "Adjective",
        "meaning": "Lasting for a very short time",
        "example": "The beauty of cherry blossoms is ephemeral"
    },
    {
        "word": "Collaborate",
        "part_of_speech": "Verb",
        "meaning": "To work jointly on an activity or project",
        "example": "We need to collaborate to finish this project"
    }
]

class WordService:
    @staticmethod
    def get_random_word():
        """ดึงคำศัพท์สุ่มจากฐานข้อมูล"""
        return random.choice(WORDS_DB)
    
    @staticmethod
    def get_word_by_name(word_name: str):
        """ค้นหาคำศัพท์จากชื่อ"""
        for word in WORDS_DB:
            if word["word"].lower() == word_name.lower():
                return word
        return None