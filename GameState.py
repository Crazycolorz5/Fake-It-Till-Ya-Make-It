from Discovery import Watson
from NLC import *
from enum import Enum
from StateBase import *
from BiologyClassroom import makeBiologyClassroom
from MathClassroom import makeMathClassroom

class PlayerState(Enum):
    DEFAULT = 1
    CHOOSE_ROOM = 2
    CHOOSE_STUDENT = 3

class Player:
    helpString = '''help: gives a brief description of basic commands user can enter
quit: quits the demo
answer _: submits an answer to the current question
query _: queries Watson for given keyword/keyphrase'''
    
    def __init__(self, name):
        self.name = name
        self.watson = Watson()
        self.nlc = NLC()
        self.studentNLC = StudentNLC()
        self.gameState = GameState(name)
        self.location = self.gameState.Hallway
        self.lastStudent = None
        self.state = PlayerState.DEFAULT

    # act :: (Player, String) -> String
    def act(self, inputString):
        # Do some small string processing.
        words = inputString.split(' ', 1)
        if not words:
            return "No command specified!"
        elif words[0] == "help":
            return Player.helpString
        elif words[0] == "query":
            if len(words) == 1:
                return "No query specified!"
            else:
                argument = words[1].strip('"')
                return Player.formatResponse(self.watson.ask(argument))
        elif words[0] == "answer":
            if len(words) == 1:
                return "No answer specified!"
            elif self.lastStudent == None:
                return "You have not spoken to a student!"
            elif not self.lastStudent.talkedTo:
                return "You haven't heard what this student has to say yet!"
            else:
                return self.lastStudent.answer(words[1])        
        else:
            if self.state == PlayerState.DEFAULT:
                self.lastStudent = None #Will be set later if we are to talk to a student.
                intent = self.nlc.classify(inputString)
                retStr = self.location.actOnIntent(self, intent)
                return "Invalid command." if retStr is None else retStr
            elif self.state == PlayerState.CHOOSE_ROOM:
                pass #TODO
            elif self.state == PlayerState.CHOOSE_STUDENT:
                classifiedName = self.studentNLC.classify(inputString)
                if classifiedName == "cancel":
                    self.state = PlayerState.DEFAULT
                    return "You decide against talking to a student right now."
                studentList = self.location.students
                for student in studentList:
                    if student.name.casefold() == classifiedName.casefold(): 
                        #Note: Student names (to the classifier) are case-insensitive, but commands ARE.
                        self.lastStudent = student
                        self.state = PlayerState.DEFAULT
                        return student.talkTo() #breaks control flow.
                return "Invalid student name. Please try again." #Note no state change.
    
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

class GameState:
    def __init__(self, playerName):
        self.Hallway = LocationState()
        self.Hallway2 = LocationState()
        self.BiologyClassroom = makeBiologyClassroom()
        self.MathClassroom = makeMathClassroom()
        self.PhysicsClassroom = LocationState()
        self.LitClassroom = LocationState()
        self.USHistClassroom = LocationState()
        self.WorldHistClassroom = LocationState()
        
        self.Hallway2.commandDictionary = hallwayCommands
        self.Hallway.commandDictionary = hallwayCommands
        self.PhysicsClassroom.commandDictionary = classroomCommands
        self.LitClassroom.commandDictionary = classroomCommands
        self.USHistClassroom.commandDictionary = classroomCommands
        self.WorldHistClassroom.commandDictionary = classroomCommands
        
        # US History classroom student 1
        # In the hallway currently for testing.
        LinManuelMiranda = Student("Lin-Manuel Miranda",
                          "Hey Prof. %s, I have a question. What date was the treaty of Ghent signed? (format: MM/DD/YYYY)" % playerName,
                          "To repeat my question, what date was the treaty of Ghent signed? (format: MM/DD/YYYY)",
                          "Thank you for answering my question!",
                          '12/24/1814',
                          "Thanks for that answer!",
                          "Hm, I don't think that's quite right...")
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
                              "Hi! So, how many people have served as the President of the U.S.? Like, total?",
                              "Hi again. If it isn't too much trouble, how many people have been president?",
                              "You're the best!",
                              "44",
                              "Oh, I should have known that! Thank you!",
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
                              "So what year was \"Tale of Two Cities\", by Charles Dickens, published?",
                              "I know, it's confusing to me too. \"Tale of Two Cities\" was published in what year?",
                              "Thanks for your help!",
                              "1859",
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
                              
                              
        # Add students to classrooms
        self.PhysicsClassroom.students = [BettyWhite, CharlesDickens]
        self.LitClassroom.students = [FrancisBacon, KevinPrice]
        self.USHistClassroom.students = [LinManuelMiranda, ElizabethRoss, FrankPierce]
        self.WorldHistClassroom.students = [MarieCurie, RosalindFranklin]

def hallwayLookaround(player, locationState): 
    if locationState.students[0].answered: #TODO: Store this as a flag in the location.
        return "You see the student whose question you answered. There is also a door to the singular classroom of the school."
    else:
        return "There's a student who appears to want to ask you a question. There is also a door to the singular classroom of the school."
    
hallwayCommands = {
    "move to classroom" : makeMoveCommand(lambda gs: gs.BiologyClassroom, "You move to the biology classroom."), #TODO: Ask which classroom once we have more.
    "talk to student" : selectStudent,
    "look around" : hallwayLookaround
    }

def classroomLookaround(player, locationState):
    answeredJohnDoe = locationState.answered("John Doe")
    answeredSamWinchester = locationState.answered("Sam Winchester")
    johnDoeStatus = "There's a student looking at a diagram of cells, loking somewhat confused." if not answeredJohnDoe else "John Doe is sitting at their desk." #TODO: Store this as a flag in the location.
    samWinchesterStatus = "There's a student waiting by the teacher's desk to ask a question." if not answeredSamWinchester else "Sam Winchester has returned to their desk and is waiting for the school day to end."
    deskStatus = "There's a teacher's desk." if not locationState.gotNotes else "There's a teacher's desk, where you got the lecture notes from."
    computerStatus = "There are several computers in the corner of the room, presumably for students to use during a free period." if not locationState.gotWikipedia else "There are several computers, including the one you get the Wikipedia article from. You have to remember to tell your students not to cite Wikipedia."
    door = "There is a door to the hallway."
    return "%s\n%s\n%s\n%s\n%s" % (johnDoeStatus, samWinchesterStatus, deskStatus, computerStatus, door)

def classroomDesk(player, locationState):
    if locationState.gotNotes:
        return "You've already gotten the lecture notes from the teacher's desk."
    else:
        locationState.gotNotes = True
        player.watson.findDocument(WAR_OF_1812_DOCUMENT)
        return "You open the drawer and grab the lecture notes the regular teacher left you. To reduce prep time, you pull out your phone, take a picture of the notes, and send it to IBM Watson for analysis.\nYou got a document on the War of 1812!"

def classroomComputer(player, locationState):
    if locationState.gotWikipedia:
        return "You have no further use for the computer at this time."
    elif locationState.students[0].talkedTo: #TODO: Store this as a flag in the location.
        locationState.gotWikipedia = True
        player.watson.findDocument(MITOSIS_DOCUMENT)
        return "As per the student's request, you search the web for an article on mitosis.\nYou grab the Wikipedia page and send it to IBM Watson for analysis.\nYou got a document on mitosis!"
    else:
        return "You have no reason to use a computer at the moment."

classroomCommands = {
    "move to hallway": makeMoveCommand(lambda gs: gs.Hallway, "You move to the hallway."),
    "talk to student" : selectStudent,
    "look around" : classroomLookaround,
    "interact with desk" : classroomDesk,
    "interact with computer" : classroomComputer
}
