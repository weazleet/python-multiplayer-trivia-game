# UI.py
from game import QuizGame
from team import Team
import customtkinter as ctk


class QuizUI:
    def __init__(self):
        self.window = ctk.CTk()

        self.window.title("What the f*ck you know?")
        
        self.fullscreen = False
        self.window.bind("<F11>", self.toggleFullscreen)
        self.window.bind("<Escape>", self.exitFullscreen)
        self.window.bind("<F10>", lambda event: self.maximiseWindow())

        self.game = QuizGame()
        self.colors = {
                    "background": "#14171C",
                    "panel": "#20242B",
                    "card": "#2A3038",
                    "primary": "#2878C7",
                    "primaryHover": "#2165A8",
                    "accent": "#E3B341",
                    "accentHover": "#C99A2F",
                    "text": "#F4F4F4",
                    "mutedText": "#B5BBC4",
                    "error": "#E05A5A",
                    "correct": "#39A96B",
                    "incorrect": "#D94C4C"}
        
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.mainFrame = ctk.CTkFrame(self.window, fg_color=self.colors["background"])
        self.mainFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.fontAppTitle = ctk.CTkFont(family="Arial", size=42, weight="bold")
        self.fontScreenTitle = ctk.CTkFont(family="Arial", size=32, weight="bold")
        self.fontQuestion = ctk.CTkFont(family="Arial", size=28, weight="bold")
        self.fontSubheading = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.fontButton = ctk.CTkFont(family="Arial", size=22)
        self.fontBody = ctk.CTkFont(family="Arial", size=20)
        self.fontSmall = ctk.CTkFont(family="Arial", size=16)
        self.fontWinner = ctk.CTkFont(family="Arial", size=34, weight="bold")
        self.fontDetailQuestion = ctk.CTkFont(family="Arial", size=17, weight="bold")
        self.fontDetailBody = ctk.CTkFont(family="Arial", size=16)
        self.fontDetailSmall = ctk.CTkFont(family="Arial", size=15)

        ctk.set_appearance_mode("dark")

        self.showStartScreen()

        self.window.after(150, self.maximiseWindow)

    def maximiseWindow(self):
        try:
            self.window.state("zoomed")
        except Exception:
            self.window.attributes("-zoomed", True)

    def run(self):
        self.window.mainloop()

    def toggleFullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)

    def exitFullscreen(self, event=None):
        self.fullscreen = False
        self.window.attributes("-fullscreen", False)

    def clearScreen(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

    def prepareScreen(self):
        self.clearScreen()

        for row in range(5):
            self.mainFrame.grid_rowconfigure(row, weight=0)

        self.mainFrame.grid_columnconfigure(0, weight=1)

    def createStandardLayout(self, includeFooter=True):
        self.prepareScreen()

        self.mainFrame.grid_rowconfigure(0, weight=0)
        self.mainFrame.grid_rowconfigure(1, weight=1)
        self.mainFrame.grid_rowconfigure(2, weight=0)

        headerFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.colors["panel"], corner_radius=15)
        headerFrame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        contentFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.colors["panel"], corner_radius=15)
        contentFrame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        footerFrame= None

        if includeFooter:
            footerFrame = ctk.CTkFrame(self.mainFrame, fg_color=self.colors["panel"], corner_radius=15)
            footerFrame.grid(row=2, column=0, padx=20, pady=(10,20), sticky="ew")

        return headerFrame, contentFrame, footerFrame

    def wrapTextToWidth(self, text, font, maxWidth):
        words = text.split()
        lines = []
        currentLine = ""

        for word in words:
            testLine = f"{currentLine} {word}".strip()

            if font.measure(testLine) <= maxWidth:
                currentLine = testLine
            else:
                lines.append(currentLine)
                currentLine = word
        if currentLine:
            lines.append(currentLine)
        return "\n".join(lines)

    def buildRoundDetails(self, parent, roundData):
        categoryLabel = ctk.CTkLabel(parent, text=roundData["category"], font=self.fontQuestion)
        categoryLabel.pack(pady=(20, 10))

        questionsFrame = ctk.CTkFrame(parent, fg_color="transparent")
        questionsFrame.pack(fill="x", padx=20, pady=(5, 25))

        self.window.update_idletasks()

        questionCount = len(roundData["questions"])

        availableWidth = questionsFrame.winfo_width()

        if availableWidth <= 1:
            availableWidth = parent.winfo_width() - 40

        spacing = questionCount * 16
        cardWidth = (availableWidth - spacing) // questionCount
        cardWidth = max(200, min(cardWidth, 320))
        questionWrap = max(130, cardWidth - 120)
        answerWrap = max(120, cardWidth - 90)

        for column in range(questionCount):
            questionsFrame.grid_columnconfigure(column, weight=1, uniform="question")

        for index, questionData in enumerate(roundData["questions"]):
            questionCard = ctk.CTkFrame(questionsFrame,width=cardWidth, corner_radius=15, border_width=1, fg_color=self.colors["card"])
            questionCard.grid(row=0, column=index, padx=8, pady=8, sticky="nsew")

            questionCard.grid_columnconfigure(0, weight=1)
            questionCard.grid_rowconfigure(0, minsize=50)
            questionCard.grid_rowconfigure(1, minsize=130)
            questionCard.grid_rowconfigure(2, minsize=80)
            questionCard.grid_rowconfigure(3, weight=1)

            numberLabel = ctk.CTkLabel(questionCard, text=f"Q{index + 1}", font=self.fontSubheading)
            numberLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

            questionTextWidth = cardWidth - 70

            wrappedQuestion = self.wrapTextToWidth(questionData["text"], self.fontDetailQuestion, questionTextWidth)
            questionLabel = ctk.CTkLabel(questionCard, text=wrappedQuestion, font=self.fontDetailQuestion, width=questionTextWidth - 10, height=120, justify="center")
            questionLabel.grid(row=1, column=0, padx=25, pady=5)

            correctLabel = ctk.CTkLabel(questionCard, text=f"Correct Answer:\n{questionData['correct_answer']}", font=self.fontDetailBody, width=cardWidth - 30, height=70,justify="center")
            correctLabel.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")

            answersFrame = ctk.CTkFrame(questionCard, fg_color="transparent")
            answersFrame.grid(row=3, column=0, padx=10, pady=(5, 15), sticky="nsew")
            answersFrame.grid_columnconfigure(0, weight=1)

            for teamIndex, answerData in enumerate(questionData["team_answers"]):
                answerLabel = ctk.CTkLabel(answersFrame, text=f"{answerData['team']}:\n{answerData['answer']}", font=self.fontDetailSmall, width=cardWidth - 90, wraplength=answerWrap, justify="left", anchor="w")
                answerLabel.grid(row=teamIndex, column=0, padx=(5, 10), pady=4, sticky="ew")

                if answerData["correct"]:
                    marker = "+1"
                    markerColour = self.colors["correct"]
                else:
                    marker = "X"
                    markerColour = self.colors["incorrect"]

                markerLabel = ctk.CTkLabel(answersFrame, text=marker, font=self.fontSubheading, text_color=markerColour)
                markerLabel.grid(row=teamIndex, column=1, sticky="e", padx=5, pady=4) 

    def showStartScreen(self):
        headerFrame, contentFrame, _ = self.createStandardLayout(includeFooter=False)

        title = ctk.CTkLabel(headerFrame, text="WHAT THE F*CK YOU KNOW?", font=self.fontAppTitle)
        title.pack(pady=60)

        menuFrame = ctk.CTkFrame(contentFrame, fg_color="transparent")
        menuFrame.pack(expand=True)

        startButton = ctk.CTkButton(menuFrame, text="Start Game",width=420, height=80, font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=self.showTeamSetup)
        startButton.pack(padx=300, pady=45, fill="x")

        quitButton = ctk.CTkButton(menuFrame, text="Quit",width=420, height=80, font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=self.window.destroy)
        quitButton.pack(padx=300, pady=45, fill="x")

    def showTeamSetup(self):
        headerFrame, contentFrame, _ = self.createStandardLayout(includeFooter=False)

        title = ctk.CTkLabel(headerFrame, text="Team Setup", font=self.fontScreenTitle)
        title.pack(pady=20)

        teamSetupFrame = ctk.CTkFrame(contentFrame, fg_color="transparent")
        teamSetupFrame.pack(expand=True)

        prompt = ctk.CTkLabel(teamSetupFrame, text="How many teams are playing?", font=self.fontSubheading)
        prompt.pack(pady=30)

        teamButtonFrame = ctk.CTkFrame(teamSetupFrame, fg_color='transparent')
        teamButtonFrame.pack(pady=(30, 0))
        teamButtonFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for column, teamCount in enumerate((2, 3, 4)):
            teamButton = ctk.CTkButton(teamButtonFrame, text=f"{teamCount}", height=160, width=160, font=self.fontAppTitle, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda count=teamCount: self.createTeamEntries(count))
            teamButton.grid(row=0, column=column, padx=20, pady=20)

        moreButton = ctk.CTkButton(teamButtonFrame, text="+", height=160, width=160, font=self.fontAppTitle, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=self.showCustomTeamCount)
        moreButton.grid(row=0, column=3, padx=20, pady=20)

    def showCustomTeamCount(self):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()

        title = ctk.CTkLabel(headerFrame, text="MORE TEAMS", font=self.fontScreenTitle)
        title.pack(pady=20)

        prompt = ctk.CTkLabel(contentFrame, text="How many teams are playing?", font=self.fontSubheading)
        prompt.pack(pady=30)

        self.teamCountEntry = ctk.CTkEntry(contentFrame, placeholder_text="Enter 5 or more", font=self.fontBody)
        self.teamCountEntry.pack(pady=10)

        self.teamSetupMessage = ctk.CTkLabel(contentFrame, text="")
        self.teamSetupMessage.pack(pady=5)

        continueButton = ctk.CTkButton(footerFrame, text="Continue", font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=self.validateCustomTeamCount)
        continueButton.pack(pady=15)

    def validateCustomTeamCount(self):
        teamCount = self.teamCountEntry.get()

        if teamCount.isdigit() and 5 <= int(teamCount) <= 12:
            self.createTeamEntries(int(teamCount))
            return

        self.teamSetupMessage.configure(text="Please enter 5 or more teams.", font=self.fontSmall)

    def createTeamEntries(self, teamCount):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()
        title = ctk.CTkLabel(headerFrame, text="ENTER TEAM NAMES", font=self.fontScreenTitle)
        title.pack(pady=20)

        entriesFrame = ctk.CTkFrame(contentFrame, fg_color="transparent")
        entriesFrame.pack(expand=True)
  
        self.teamNameEntries = []

        for number in range(1, teamCount + 1):
            entry = ctk.CTkEntry(entriesFrame, placeholder_text=f"Team {number} name", font=self.fontBody, width=420, height=48, fg_color=self.colors["card"], border_color=self.colors["primary"], text_color=self.colors["text"], placeholder_text_color=self.colors["mutedText"])
            entry.pack(pady=8)

            self.teamNameEntries.append(entry)

        self.teamNameMessage = ctk.CTkLabel(entriesFrame, text="")
        self.teamNameMessage.pack(pady=5)

        continueButton = ctk.CTkButton(footerFrame, text="Continue", fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, height=55, font=self.fontButton, command=self.saveTeams)
        continueButton.pack(pady=15)

    def saveTeams(self):
        teamNames = []

        for entry in self.teamNameEntries:
            teamName = entry.get().strip()

            if not teamName:
                self.teamNameMessage.configure(text="All teams must have a name.")
                return

            teamNames.append(teamName)

        if len(teamNames) != len(set(teamNames)):
            self.teamNameMessage.configure(text="Each team must have a unique name.")
            return

        self.game.teams = []

        for teamName in teamNames:
            self.game.teams.append(Team(teamName))

        self.showDifficultyScreen()

    def showDifficultyScreen(self):
        headerFrame, contentFrame, _ = self.createStandardLayout(includeFooter=False)

        title = ctk.CTkLabel(headerFrame, text="CHOOSE DIFFICULTY", font=self.fontScreenTitle)
        title.pack(pady=40)

        difficultyFrame = ctk.CTkFrame(contentFrame, fg_color="transparent")
        difficultyFrame.pack(expand=True)

        easyButton = ctk.CTkButton(difficultyFrame, text="Easy", font=self.fontButton, height=80, width=420, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda: self.selectDifficulty("Easy"))
        easyButton.pack(padx=300, pady=30, fill="x")

        mediumButton = ctk.CTkButton(difficultyFrame, text="Medium", font=self.fontButton, height=80, width=420, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda: self.selectDifficulty("Medium"))
        mediumButton.pack(padx=300, pady=30, fill="x")

        hardButton = ctk.CTkButton(difficultyFrame, text="Hard", font=self.fontButton, height=80, width=420, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda: self.selectDifficulty("Hard"))
        hardButton.pack(padx=300, pady=30, fill="x")

    def selectDifficulty(self, difficulty):
        self.game.setDifficulty(difficulty)
        self.showCategoryScreen()
        
    def showCategoryScreen(self):
        headerFrame, contentFrame, _ = self.createStandardLayout(includeFooter=False)

        title = ctk.CTkLabel(headerFrame, text="CHOOSE CATEGORY", font=self.fontScreenTitle)
        title.pack(pady=40)

        availableCategories = self.game.getAvailableCategories()

        for column in range(3):
            contentFrame.grid_columnconfigure(column, weight=1)

        for row in range(4):
            contentFrame.grid_rowconfigure(row, weight=1)

        for index, category in enumerate(availableCategories):
            row = index // 3
            column = index % 3

            categoryButton = ctk.CTkButton(contentFrame, text=category, font=self.fontSubheading, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda c=category: self.selectCategory(c))
            categoryButton.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")

    def selectCategory(self, category):
        self.game.setCategory(category)
        self.game.startRound()

        self.currentTeamIndex = 0

        self.showQuestionScreen()

    def showQuestionScreen(self):
        self.clearScreen()

        self.mainFrame.grid_rowconfigure(0, weight=0)
        self.mainFrame.grid_rowconfigure(1, weight=0)
        self.mainFrame.grid_rowconfigure(2, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)

        question = self.game.getCurrentQuestion()
        team = self.game.teams[self.currentTeamIndex]

        roundNumber = len(self.game.usedCategories)
        questionNumber = self.game.currentQuestion + 1

        #Header Frame
        headerFrame = ctk.CTkFrame(self.mainFrame)
        headerFrame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        roundLabel = ctk.CTkLabel(headerFrame, text=f"Round {roundNumber} of {self.game.totalRounds}", font=self.fontSmall, text_color=self.colors["mutedText"])
        roundLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        categoryLabel = ctk.CTkLabel(headerFrame, text=self.game.category, font=self.fontBody, text_color=self.colors["accent"])
        categoryLabel.grid(row=0, column=1, padx=10, pady=10)

        questionCountLabel = ctk.CTkLabel(headerFrame, text=f"Question {questionNumber} of {self.game.roundSize}", font=self.fontSmall, text_color=self.colors["mutedText"])
        questionCountLabel.grid(row=0, column=2, sticky="e", padx=10, pady=10)

        #Question Frame
        questionFrame = ctk.CTkFrame(self.mainFrame)
        questionFrame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        teamLabel = ctk.CTkLabel(questionFrame, text=f"{team.name}'s turn", font=self.fontSubheading, text_color=self.colors["accent"])
        teamLabel.pack(pady=(15, 10))

        questionLabel = ctk.CTkLabel(questionFrame, text=question.text, font=self.fontQuestion, wraplength=700)
        questionLabel.pack(padx=30, pady=15)

        #Answer Frame
        answerFrame = ctk.CTkFrame(self.mainFrame)
        answerFrame.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="nsew")
        answerFrame.grid_columnconfigure(0, weight=1)
        for row in range(3):
            answerFrame.grid_rowconfigure(row, weight=1)

        for index, answer in enumerate(question.answers):
            answerButton = ctk.CTkButton(answerFrame, text=answer, height=120, font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, command=lambda i=index: self.handleAnswer(i))
            answerButton.grid(row=index, column=0, padx=200, pady=8, sticky="ew")

    def handleAnswer(self, answerIndex):
        team = self.game.teams[self.currentTeamIndex]

        self.game.submitAnswer(team, answerIndex)

        self.currentTeamIndex += 1

        if self.currentTeamIndex < len(self.game.teams):
            self.showQuestionScreen()
            return

        self.currentTeamIndex = 0
        self.game.nextQuestion()

        if self.game.currentQuestion < len(self.game.roundQuestions):
            self.showQuestionScreen()
        else:
            self.roundComplete()

    def roundComplete(self):
        self.roundScores = self.game.scoreRound()
        self.game.saveRoundHistory()
        self.showRoundResults()
            

    def showRoundResults(self):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()

        title = ctk.CTkLabel(headerFrame, text="ROUND COMPLETE", font=self.fontScreenTitle)
        title.pack(pady=30)

        sortedTeams = sorted(self.game.teams, key=lambda team: team.score, reverse=True)

        if len(sortedTeams) <= 4:
            resultsGrid = ctk.CTkFrame(contentFrame, fg_color="transparent")
        else:
            resultsGrid = ctk.CTkScrollableFrame(contentFrame, fg_color="transparent")
        resultsGrid.pack(fill="both", expand=True, padx=40, pady=20)

        resultsGrid.grid_columnconfigure((0, 1), weight=1)
        rowCount = (len(self.game.teams) + 1) // 2

        for row in range(rowCount):
            resultsGrid.grid_rowconfigure(row, weight=0, minsize=220)

        for index, team in enumerate(self.game.teams):
            score = self.roundScores[team.name]

            row = index // 2
            column = index % 2

            teamCard = ctk.CTkFrame(resultsGrid,fg_color=self.colors["card"], corner_radius=18, border_width=2, border_color=self.colors["panel"])
            teamCard.grid(row=row, column=column, padx=15, pady=15, sticky="ew")

            teamNameLabel = ctk.CTkLabel(teamCard, text=team.name, font=self.fontSubheading)
            teamNameLabel.pack(pady=(20, 10))

            resultsLabel = ctk.CTkLabel(teamCard, text=f"Round Score: {score}/{self.game.roundSize}", font=self.fontBody)
            resultsLabel.pack(pady=5)

            totalLabel = ctk.CTkLabel(teamCard, text=f"Total Score: {team.score}/{self.game.totalQuestions}", font=self.fontBody)
            totalLabel.pack(pady=(5, 20))

        detailsButton = ctk.CTkButton(footerFrame, text="More Details", font=self.fontButton, fg_color=self.colors["card"], hover_color=self.colors["panel"], text_color=self.colors["text"], corner_radius=12, border_width=2, border_color=self.colors["primary"], width=420, height=55, command=self.showRoundDetails)
        detailsButton.pack(pady=10)

        continueButton = ctk.CTkButton(footerFrame, text="Continue", font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, width=420, height=55, command=self.continueGame)
        continueButton.pack(pady=30)

    def showRoundDetails(self):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()

        title = ctk.CTkLabel(headerFrame, text="ROUND DETAILS", font=self.fontScreenTitle)
        title.pack(pady=25)

        roundData = self.game.roundHistory[-1]

        detailsScroll = ctk.CTkScrollableFrame(contentFrame, fg_color="transparent")
        detailsScroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.buildRoundDetails(detailsScroll, roundData)

        backButton = ctk.CTkButton(footerFrame, text="Back to Round Results", width=420, height=55, font=self.fontButton, fg_color=self.colors["card"], hover_color=self.colors["panel"], text_color=self.colors["text"], corner_radius=12, border_width=2, border_color=self.colors["primary"], command=self.showRoundResults)
        backButton.pack(pady=20)

    def continueGame(self):
        self.game.resetRound()

        if len(self.game.usedCategories) < self.game.totalRounds:
            self.showCategoryScreen()
        else:
            self.showFinalResults()

    def replaySameTeams(self):
        self.game.resetGame(keepTeams=True)
        self.showDifficultyScreen()

    def replayNewTeams(self):
        self.game.resetGame(keepTeams=False)
        self.showTeamSetup()

    def showFinalResults(self):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()

        contentFrame.grid_columnconfigure(0, weight=1)

        contentFrame.grid_rowconfigure(0, weight=0)
        contentFrame.grid_rowconfigure(1, weight=1, minsize=220)
        contentFrame.grid_rowconfigure(2, weight=0)
        contentFrame.grid_rowconfigure(3, weight=0)

        sortedTeams = sorted(self.game.teams, key=lambda team: team.score, reverse=True)

        highestScore = sortedTeams[0].score

        title = ctk.CTkLabel(headerFrame, text="QUIZ COMPLETE!", font=self.fontScreenTitle)
        title.pack(pady=25)

        infoLabel = ctk.CTkLabel(contentFrame, text=f"Difficulty: {self.game.difficulty}  |  "
                                 f"Rounds Played: {self.game.totalRounds}\n"
                                 f"Categories Played: {', '.join(self.game.usedCategories)}", font=self.fontBody)
        infoLabel.grid(row=0, column=0, pady=10)

        if len(sortedTeams) <= 4:
            standingsFrame = ctk.CTkFrame(contentFrame, fg_color="transparent")
        else:
            standingsFrame = ctk.CTkScrollableFrame(contentFrame, fg_color="transparent")
        standingsFrame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        standingsFrame.grid_columnconfigure((0, 1), weight=1)

        resultsRows = (len(sortedTeams) + 1) // 2
        for row in range(resultsRows):
            standingsFrame.grid_rowconfigure(row, weight=1, minsize=190)

        footerFrame.grid_columnconfigure((0, 1, 2), weight=1)

        for index, team in enumerate(sortedTeams):
            position = index + 1

            row = index //2
            column = index % 2

            isWinner = team.score == highestScore
            borderColour = (self.colors["accent"] if isWinner else self.colors["panel"])

            resultCard = ctk.CTkFrame(standingsFrame, corner_radius=18, border_width=2, border_color=borderColour, fg_color=self.colors["card"])
            resultCard.grid(row=row, column=column, padx=10, pady=6, sticky="ew")

            positionLabel = ctk.CTkLabel(resultCard, text=f"{position}", font=self.fontScreenTitle)
            positionLabel.pack(pady=(8, 2))

            teamNameLabel = ctk.CTkLabel(resultCard, text=team.name, font=self.fontSubheading)
            teamNameLabel.pack(pady=(5, 5))
    
            scoreLabel = ctk.CTkLabel(resultCard, text=f"{team.score}/{self.game.totalQuestions}", font=self.fontBody)
            scoreLabel.pack(pady=(2, 8))

        
        
        winners = [team for team in sortedTeams if team.score == highestScore]
        
        if len(winners) ==1:
            winnerText = f"Winner: {winners[0].name}!"
        else:
            winnerNames = [team.name for team in winners]
            winnerText = f"It's a tie between {', '.join(winnerNames)}!"

        winnerLabel = ctk.CTkLabel(contentFrame, text=winnerText, font=self.fontWinner, text_color=self.colors["accent"])
        winnerLabel.grid(row=2, column=0, pady=20)

        detailsButton = ctk.CTkButton(contentFrame, text="More Details", width=420, height=50, font=self.fontButton, fg_color=self.colors["card"], hover_color=self.colors["panel"], text_color=self.colors["text"], corner_radius=12, border_width=2, border_color=self.colors["primary"], command=self.showFinalDetails)
        detailsButton.grid(row=3, column=0, padx=100, pady=(5, 15))

        replaySameButton = ctk.CTkButton(footerFrame, text="Play Again - Same Teams", font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, height=55, command=self.replaySameTeams)
        replaySameButton.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

        replayNewButton = ctk.CTkButton(footerFrame, text="Play Again - New Teams", font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, height=55, command=self.replayNewTeams)
        replayNewButton.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

        quitButton = ctk.CTkButton(footerFrame, text="Quit", font=self.fontButton, fg_color=self.colors["primary"], hover_color=self.colors["primaryHover"], text_color=self.colors["text"], corner_radius=12, height=55, command=self.window.destroy)
        quitButton.grid(row=0, column=2, padx=10, pady=20, sticky="ew")

    def showFinalDetails(self):
        headerFrame, contentFrame, footerFrame = self.createStandardLayout()

        title = ctk.CTkLabel(headerFrame, text="FULL QUIZ DETAILS", font=self.fontScreenTitle)
        title.pack(pady=25)

        scrollFrame = ctk.CTkScrollableFrame(contentFrame)

        scrollFrame.pack(fill="both", expand=True, padx=15, pady=15)

        for roundData in self.game.roundHistory:
            self.buildRoundDetails(scrollFrame,roundData)

        backButton = ctk.CTkButton(footerFrame, text="Back to Final Results", height=55, font=self.fontButton, fg_color=self.colors["card"], hover_color=self.colors["panel"], text_color=self.colors["text"], corner_radius=12, border_width=2, border_color=self.colors["primary"], command=self.showFinalResults)
        backButton.pack(pady=20)

if __name__ == "__main__":
    app = QuizUI()
    app.run()
