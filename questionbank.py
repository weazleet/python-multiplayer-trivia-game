from pathlib import Path
import json
from question import Question
import random

class QuestionBank:
    def __init__(self):
        self.questions = []
        self.categories = []

    def loadQuestions(self, file_path):
        base_path = Path(__file__).resolve().parent
        file_path = base_path / file_path

        with file_path.open(encoding="utf-8") as file:
            questionData = json.load(file)
        
        self.categories = list(questionData.keys())

        for category in questionData.values():
            for question in category:
                newQuestion = Question(
                    question["text"],
                    question["answers"],
                    question["correct_answer"],
                    question["category"],
                    question["difficulty"]
                )

                self.questions.append(newQuestion)
    
    def shuffleQuestions(self):
        random.shuffle(self.questions)

    def shuffleAnswers(self):
        for question in self.questions:
            random.shuffle(question.answers)

    def getCategoryQuestions(self, category, difficulty):
        categoryQuestions = []

        for question in self.questions:
            if question.category == category and question.difficulty == difficulty:
                categoryQuestions.append(question)

        random.shuffle(categoryQuestions)

        return categoryQuestions
