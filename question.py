# question.py

from dataclasses import dataclass

@dataclass
class Question:
    text: str
    answers: list
    correct_answer: str
    category: str
    difficulty: str