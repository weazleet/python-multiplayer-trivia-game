# Title: What the f*ck you know?
# Author: Nick
# Date created: 16/08/26

# Description: A simple trivia game, with categories and multiple choice answers

# Imports
from question import Question
from questionbank import QuestionBank
from team import Team


# Load Question List from questions JSON
bank = QuestionBank()
bank.loadQuestions("data/questions.json")
bank.shuffleAnswers()


# Main Game
class QuizGame:

    #Constructor initialises class variables
    def __init__(self):
        #Game-Level values
        self.difficulty = ""
        self.totalQuestions = 0
        self.totalRounds = 0
        self.teams = []

        #Round-Level values
        self.currentQuestion = 0
        self.roundSize = 5
        self.roundQuestions = []
        self.category = ""
        self.usedCategories = []
        self.roundHistory = []

    # Quiz Game Logic
    def playQuiz(self):
        if not self.teams:
            self.setupTeams()

        self.chooseDifficulty()
        for roundNumber in range(self.totalRounds):
            self.chooseCategory()
            print()
            print(f"Round {roundNumber + 1} of {self.totalRounds}")
            print(self.category)
            print()
            
            self.startRound()            

            while self.currentQuestion < len(self.roundQuestions):
                self.displayQuestion()

                for team in self.teams:
                    userAnswer = self.getAnswer(team)
                    self.storeAnswer(team, userAnswer)

                self.nextQuestion()

                print()
            self.markRound()
            for team in self.teams:
                team.roundAnswers = []
            self.currentQuestion = 0
            self.roundQuestions = []
        self.displayFinalResults()

    #Display of quiz results with winner output
    def displayFinalResults(self):
        sortedTeams = sorted(self.teams, key=lambda team: team.score, reverse=True)
        print()
        print("===== QUIZ COMPLETE =====")
        print(f"Difficulty: {self.difficulty}")
        print(f"Rounds Played: {self.totalRounds}")
        print(f"Categories Played: {', '.join(self.usedCategories)}")
        print("===== FINAL RESULTS =====")

        for position, team in enumerate(sortedTeams, start=1):
            print(f"{position}. {team.name} - "
                  f"{team.score}/{self.totalQuestions}")
        highestScore = sortedTeams[0].score

        winners = []

        for team in sortedTeams:
            if team.score == highestScore:
                winners.append(team)
        print()

        if len(winners) ==1:
            print(f"Winner: {winners[0].name}!")
        else:
            winnerNames = [team.name for team in winners]
            print(f"It's a tie between {', '.join(winnerNames)}!")

    #Game replay function
    def replayGame(self):
        while True:
            print()
            print("1. Play again with same teams")
            print("2. Play again with new teams")
            print("3. Quit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.resetGame(keepTeams=True)
                return True

            elif choice == "2":
                self.resetGame(keepTeams=False)
                return True

            elif choice == "3":
                return False

            print("Invalid choice, try again!")

    #Full game reset
    def resetGame(self, keepTeams):
        self.difficulty = ""
        self.totalQuestions = 0
        self.totalRounds = 0

        self.currentQuestion = 0
        self.roundQuestions = []
        self.category = ""
        self.usedCategories = []
        self.roundHistory = []

        if keepTeams:
            for team in self.teams:
                team.score = 0
                team.roundAnswers = []
        else:
            self.teams = []

    def resetRound(self):
        for team in self.teams:
            team.roundAnswers = []
        self.currentQuestion = 0
        self.roundQuestions = []
        self.category = ""

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

        if difficulty == "Easy":
            self.totalRounds = 3
        elif difficulty == "Medium":
            self.totalRounds = 5
        elif difficulty == "Hard":
            self.totalRounds = len(bank.categories)

    def saveRoundHistory(self):
        roundData = {"category": self.category, "questions": []}

        for index, question in enumerate(self.roundQuestions):
            questionData = {"text": question.text, "correct_answer": question.correct_answer, "team_answers": []}
            for team in self.teams:
                answer = team.roundAnswers[index]

                answerData = {"team": team.name, "answer": answer, "correct": answer == question.correct_answer}

                questionData["team_answers"].append(answerData)
            roundData["questions"].append(questionData)
        self.roundHistory.append(roundData)

    #difficulty selection
    def chooseDifficulty(self):
        while True:
            print("Choose Difficulty")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")

            choice = input("Enter your choice (1/2/3): ")

            if choice == "1":
                self.difficulty = "Easy"
                self.totalRounds = 3
                break
            elif choice == "2":
                self.difficulty = "Medium"
                self.totalRounds = 5
                break
            elif choice == "3":
                self.difficulty = "Hard"
                self.totalRounds = len(bank.categories)
                break

            print("Invalid choice, try again!")

    #category selection
    def chooseCategory(self):
        availableCategories = []

        for category in bank.categories:
            if category not in self.usedCategories:
                availableCategories.append(category)

        while True:
            print("Choose Category")

            for number, category in enumerate(availableCategories, start=1):
                print(f"{number}. {category}")

            choice = input("Enter category number: ")

            if choice.isdigit():
                choice = int(choice)

                if 1 <= choice <= len(availableCategories):
                    self.category = availableCategories[choice - 1]
                    self.usedCategories.append(self.category)
                    break

            print("Invalid choice, try again!")

    def getAvailableCategories(self):
        availableCategories = []

        for category in bank.categories:
            if category not in self.usedCategories:
                availableCategories.append(category)

        return availableCategories

    def setCategory(self, category):
        if category in self.getAvailableCategories():
            self.category = category
            self.usedCategories.append(category)

    def startRound(self):
        self.currentQuestion = 0

        self.roundQuestions = bank.getCategoryQuestions(self.category, self.difficulty)[:self.roundSize]

        self.totalQuestions += len(self.roundQuestions)

    #team setup
    def setupTeams(self):
        while True:
            teamCount = input("How many teams are playing?: ")

            if teamCount.isdigit() and int(teamCount) >= 2:
                teamCount = int(teamCount)
                break

            print("Please enter at least 2 teams.")

        for number in range(1, teamCount + 1):
            while True:
                teamName = input(f"Enter Team {number} name: ").strip()

                if teamName:
                    self.teams.append(Team(teamName))
                    break

                print("Team name cannot be empty.")

    def getCurrentQuestion(self):
        return self.roundQuestions[self.currentQuestion]

    #Show question and multiple choice answers
    def displayQuestion(self):
        question = self.roundQuestions[self.currentQuestion]

        print(question.text)
        print()

        for number, answer in enumerate(question.answers, start=1):
            print(f"{number}. {answer}")

    def submitAnswer(self, team, answerIndex):
        question = self.getCurrentQuestion()

        selectedAnswer = question.answers[answerIndex]

        team.roundAnswers.append(selectedAnswer)

    #get team answer
    def getAnswer(self, team):
        while True:
            userAnswer = input(f"{team.name}, enter your answer (1/2/3): ")

            if userAnswer in ("1", "2", "3"):
                return int(userAnswer)

            print("You have not entered an answer correctly, try again!")

    #goto next question in list
    def nextQuestion(self):
        self.currentQuestion += 1

    #store team answer
    def storeAnswer(self, team, userAnswer):
        question = self.roundQuestions[self.currentQuestion]

        selectedAnswer = question.answers[userAnswer - 1]

        team.roundAnswers.append(selectedAnswer)

    #mark team answers
    def markRound(self):
        for team in self.teams:
            roundScore = 0

            print()
            print(f"===== {team.name} =====")

            for index, answer in enumerate(team.roundAnswers):
                question = self.roundQuestions[index]

                if answer == question.correct_answer:
                    team.score += 1
                    roundScore += 1

                print(f"{index + 1}. {question.text}")
                print(f"Your answer: {answer}")
                print(f"Correct answer: {question.correct_answer}")
                print()

            print(f"Round Score: {roundScore}/{len(team.roundAnswers)}")

    def scoreRound(self):
        roundScores = {}

        for team in self.teams:
            roundScore = 0

            for index, answer in enumerate(team.roundAnswers):
                question = self.roundQuestions[index]

                if answer == question.correct_answer:
                    team.score += 1
                    roundScore += 1

            roundScores[team.name] = roundScore

        return roundScores

#Game execution
if __name__ == "__main__":
    game = QuizGame()

    while True:
        game.playQuiz()

        if not game.replayGame():
            break