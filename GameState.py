from Discovery import Watson
from NLC import NLC

WAR_OF_1812_DOCUMENT = '98e9b50f1327e045364f669dab17a2ea'
MITOSIS_DOCUMENT = 'ad9d680ed1a99a7c856a89991d25d6f7'
        
class PlayerState:
    helpString = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase'''
    
    def __init__(self, name):
        self.name = name
        self.questionNumber = 0 #TODO
        self.watson = Watson()
        self.nlc = NLC()
        self.gameState = GameState(name)
        self.location = self.gameState.Hallway

    # act :: (PlayerState, String) -> String
    def act(self, inputString):
        # Do some small string processing.
        words = inputString.split(' ', 1)
        if not words:
            return "No command specified!"
        elif words[0] == "help":
            return PlayerState.helpString
        elif words[0] == "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return PlayerState.formatResponse(self.watson.ask(argument))
        elif words[0] == "answer":
            if len(words) == 1:
                return "No answer specified!"
            else:
                return self.location.answer(words[1])
        else:
            intent = self.nlc.classify(inputString) #TODO: Fake method
            retStr = self.location.actOnIntent(self, intent)
            return "Invalid command." if retStr is None else retStr
    
    @staticmethod
    def formatResponse(stringArr):
        if len(stringArr) == 0:
            return "No results!"
        i = 1
        acc = ""
        for x in stringArr:
            acc += "Result {0}: {1}\n\n".format(i, x)
            i += 1
        return acc.strip()

class LocationState:
    def __init__(self):
        # commandDictionary :: Dictionary String ((PlayerState, LocationState) -> String)
        self.commandDictionary = dict()
        self.student = None

    # actOnIntent :: (LocationState, PlayerState, String) -> Maybe String
    def actOnIntent(self, playerState, intent):
        if intent in self.commandDictionary:
            return self.commandDictionary[intent](playerState, self)
        else:
            return None
        
    def answer(self, string):
        if self.student is None:
            return "No student to answer!"
        elif not self.student.talkedTo:
            return "You haven't heard what this student has to say yet!"
        else:
            return self.student.answer(string)
        
    def leaveHook(self):
        pass

class Student:
    def __init__(self, name, firstTalk, subsequentTalk, answeredTalk, answer, answeredCorrect, answeredIncorrect):
        self.name = name
        self.firstTalk = firstTalk
        self.subsequentTalk = subsequentTalk
        self.answeredTalk = answeredTalk
        self.correctAnswer = answer
        self.talkedTo = False
        self.answered = False
        self.answeredCorrect = answeredCorrect
        self.answeredIncorrect = answeredIncorrect
    def talkTo(self):
        if self.answered:
            return self.answeredTalk
        elif self.talkedTo:
            return self.subsequentTalk
        else:
            self.talkedTo = True
            return self.firstTalk
    def answer(self, string): #Intend to overwrite?
        if string.strip() == self.correctAnswer: #TODO: Better answer validation
            self.answered = True
            return self.answeredCorrect
        else:
            return self.answeredIncorrect

class GameState:
    def __init__(self, playerName):
        self.Hallway = LocationState()
        self.Classroom = LocationState()
        self.Hallway.commandDictionary = hallwayCommands
        self.Classroom.commandDictionary = classroomCommands
        # US History classroom student 1
        self.Hallway.students.append(Student("Lin-Manuel Miranda",
                          "Hey Prof. %s, I have a question. What date was the treaty of Ghent signed? (format: MM/DD/YYYY)" % playerName,
                          "To repeat my question, what date was the treaty of Ghent signed? (format: MM/DD/YYYY)",
                          "Thank you for answering my question!",
                          '12/24/1814',
                          "Thanks for that answer!",
                          "Hm, I don't think that's quite right...")
                          )
        self.Classroom.gotNotes = False
        self.Classroom.gotWikipedia = False
        # Biology classroom student 1
        self.Classroom.students.append(Student("John Doe",
                                    "Hey there Prof! Say, since you're just subbing, could you help me with this question on my Biology homework? What's the final phase of mitosis? (format: all lowercase)",
                                    "The question was, what's the final phase of mitosis?",
                                    "Thanks for the help!",
                                    "telophase",
                                    "Yeah, I do think the notes said something like that.",
                                    "I don't think that sounds right.")
                                    )
        # Biology classroom student 2
        SamWinchester = Student("Sam Winchester",
                              "I can't remember what the latin name of the American Black Bear for our homework. Do you remember, Professor? (format: genus species)",
                              "What is the latin name of the American Black Bear?",
                              "Thank you, Professor!",
                              "ursus americanus",
                              "Oh yeah, Ursus Americanus. Thank you!",
                              "I'm not sure that's correct, Professor.")
        # US History classroom student 2
        ElizabethRoss = Student("Elizabeth Ross",
                              "Hey Professor, I'm really bad with dates. What date was the 13th Amendment ratified? (format: MM/DD/YYYY)",
                              "What was my question? I'm asking what date the 13th Amendment was ratified.",
                              "Thanks so much!",
                              "12/06/1865",
                              "That doesn't sound super familiar, but I'll trust you, thanks Professor!",
                              "I'm not entirely sure, but that doesn't sound like the right answer.")
        # US History classroom student 3
        FrankPierce = Student("Frank Pierce",
                              "Hi! So, I don't have the Presidents memorized yet. Who was the 14th again? (format: first last)",
                              "Hi again. If it isn't too much trouble, who was the 14th president of the U.S.?",
                              "You're the best!",
                              "franklin pierce",
                              "Oh, I should have known that, it's so close to my name! Thank you!",
                              "Are you sure?")
        # World History classroom student 1
        MarieCurie = Student("Marie Curie",
                              "Hey, this question is kinda specific. Who was the German emperor during WWI? (format: title lastname suffix)",
                              "I can't remember who the emperor of Germany during WWI was. Can you help?",
                              "Neat-o, professor! Thanks!",
                              "kaiser wilhelm ii",
                              "That sounds right... At least it sounds German. Thanks!",
                              "That doesn't sound like the right person...")
        # World History classroom student 2
        RosalindFranklin = Student("Rosalind Franklin",
                              "Okay, so in Ancient Greece, they used some sort of coin with an owl on it. Who was the goddess on the other side?",
                              "What is the name of the goddess on the coins in Ancient Greece?",
                              "Thanks so much, Professor!",
                              "artemis",
                              "Yeah! Like that Eoin Colfer series! Thanks!",
                              "Hm, that doesn't sound like the right Greek goddess.")
        # Literature classroom student 1
        FrancisBacon = Student("Francis Bacon",
                              "So in \"Tale of Two Cities\", by Charles Dickens, what is the name of the first book?",
                              "I know, it's confusing to me too. \"Tale of Two Cities\" had like three books inside it. What's the first one?",
                              "Thanks for your help!",
                              "recalled to life",
                              "That's it! Thanks, Professor! I could have just looked in the book I guess, but I really hate it.",
                              "I don't think that's right.")
        # Literature classroom student 2
        KevinPrice = Student("Kevin Price",
                              "So in \"Jane Eyre\", by Charlotte Bronte, what's the name of the family she moves in with in her childhood?",
                              "What's the name of her uncle's family in \"Jane Eyre\"?",
                              "I wish you were my full time teacher!",
                              "reed",
                              "That's what it was, of course! Thanks!",
                              "I don't think that's the right last name.")
        # Math classroom student 1
        HoldenCaulfield = Student("Holden Caulfield",
                              "So apparently the quadratic equation is a special equation, because it contains only one unknown. What's the word for that?",
                              "What is the name of a math function that contains only one unknown?",
                              "Thanks for the help!",
                              "univariate",
                              "That makes sense, like one variable. Thanks!",
                              "Math already doesn't make much sense, but I don't think that's right.")
        # Math classroom student 2
        SteveBoxwell = Student("Steve Boxwell",
                              "In geometry, what's the name of a line segment that has its endpoints on the circle, but is not specifically filling any other requirement?",
                              "You forget already? I asked you, what is the name of a line segment that has its endpoints on a circle?",
                              "You're an alright substitute teacher, I guess.",
                              "univariate",
                              "I already knew that, but thanks anyway. You're not too bad.",
                              "That's not right. You call yourself a substitude teacher?")
        # Physics classroom student 1
        BettyWhite = Student("Betty White",
                              "What's the name of the person that found the theory of general relativity? (format: first last)",
                              "Do you know the scientist who found the theory of general relativity? He's got, like, crazy hair, or something?",
                              "Thank you!",
                              "albert einstein",
                              "Oh yeah, it was him! Thank you!",
                              "That doesn't sound familiar, Professor.")
        # Physics classroom student 2
        CharlesDickens = Student("Charles Dickens",
                              "Hey there, Professor. Do you know what quantity is defined by the second law of thermodynamics?",
                              "The first law of thermodynamics is the one about equal and opposite reactions, I think. What does the second define?",
                              "You're the greatest substitute ever, thanks!",
                              "entropy",
                              "Yeah, entropy! Thanks, Professor!",
                              "I think it was something else.")




def makeMoveCommand(locationAccessor, msgString):
    def moveCommand(playerState, locationState):
        playerState.location = locationAccessor(playerState.gameState)
        locationState.leaveHook()
        return msgString
    return moveCommand

def talkToStudent(playerState, locationState):
    return locationState.student.talkTo();

def hallwayLookaround(playerState, locationState): 
    if locationState.student.answered:
        return "You see the student whose question you answered. There is also a door to the singular classroom of the school."
    else:
        return "There's a student who appears to want to ask you a question. There is also a door to the singular classroom of the school."
    
hallwayCommands = {
    "move to classroom" : makeMoveCommand(lambda gs: gs.Classroom, "You move to the classroom."),
    "talk to student" : talkToStudent,
    "look around" : hallwayLookaround
    }

def classroomLookaround(playerState, locationState):
    studentStatus = "There's a student looking at a diagram of cells, loking somewhat confused." if not locationState.student.answered else "There's the student you answered, sitting at their desk."
    deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s" % (studentStatus, deskStatus, computerStatus, door)

def classroomDesk(playerState, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        playerState.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the War of 1812!"

def classroomComputer(playerState, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.student.talkedTo:
        locationState.gotWikipedia = True
        playerState.watson.findDocument(MITOSIS_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on mitosis!"
    else:
        return "You have no reason to use a computer at the moment."

classroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : talkToStudent,
    "look around" : classroomLookaround,
    "interact with desk" : classroomDesk,
    "interact with computer" : classroomComputer
}
