import random
import music21

def songCleaner(filename):
    """ takes in a string of multiple ABC songs (in G) and converts
        it into a string of notes """
    """NOTE: For now, you need to manually remove lyrics, alternate versions,
        "variations", and anything else that comes after the body of
        the song! """
    # Be careful that the first song starts at the top of the file!
    file1 = open(filename, 'rb')
    string = file1.read()
    songList = []
    songParts = string.split("X")
    for i in range(1, len(songParts)):
        songList.append(songParts[i].split("K:G")[1])
    songString = ""
    for i in range(len(songList)):
        songString+=(songList[i])
    noEndings = ""
    sections = songString.split("|1")
    listOfParts = []
    listOfParts.append(sections[0])
    for i in range(1,len(sections)):
        listOfParts.append(sections[i].split(":|2")[1])
    notesString = "" 
    for i in range(len(listOfParts)):
        noEndings += listOfParts[i]           
    for i in range(len(noEndings) - 1):        
        #For now, we remove all ornamentation
        if noEndings[i] not in [" ", "|", "\n", ":", "~", "\r"]:
            notesString += noEndings[i]               
    return notesString

def makeNotesList(string):
    notesList = []
    lengths = ["2", "3", "4", "5", "6"]
    accidentals = ["^", "=", "_"]
    while len(string) > 3:
        if string[0] in accidentals:
            if string[2] in lengths: #ANL
                notesList.append(string[0:3])
                string = string[3:]
            else: #AN N
                notesList.append(string[0:2])
                string = string[2:]
        else:
            if string[1] in lengths: #NL
                notesList.append(string[0:2])
                string = string[2:]
            else: #N N
                notesList.append(string[0])
                string = string[1:]
    return notesList

def makeMarkovDict(noteList, k):
    dictionary = {}
    for i in range(len(noteList)-k):
        currentEntry = ()
        for j in range(k):
            currentEntry = currentEntry + (noteList[i+j],)
        if currentEntry not in dictionary:
            dictionary[currentEntry] = [noteList[i+j+1]]
        else:
            dictionary[currentEntry].append(noteList[i+j+1])
    return dictionary

def makeJig(dictionary, numNotes, startNoteList):
    #note: startNoteList must have as many elements as the order!
    order = len(dictionary.keys()[0])
    if tuple(startNoteList) not in dictionary:
        return "error! check your list!"
    jigList = []
    for i in range(order):
        jigList.append(startNoteList[i])
    for i in range(numNotes - order):
        currentEntry = ()
        for j in range(order):
            currentEntry = currentEntry + tuple(jigList[i+j])
        if currentEntry in dictionary:
            validNextNotes = dictionary[currentEntry]
        else:
            validNextNotes = dictionary[tuple(startNoteList)]
        jigList.append(random.choice(validNextNotes))
    return jigList

def makeValidJig(noteList):
    songString = """X: 1
T: Markov Jig
C: Computers
N:A Markov-Generated Jig!
M:6/8
L:1/8
K:G
"""
    accidentals = ["^", "=", "_"]
    currentBeats = 0
    for i in range(len(noteList)):
        if currentBeats < 6:
            if ('2' not in noteList[i] and '3' not in noteList[i]
            and '4' not in noteList[i] and '5' not in noteList[i]
            and '6' not in noteList[i]):
                songString += noteList[i]
                if currentBeats == 2:
                    songString += " "
                currentBeats +=1
            elif '2' in noteList[i]:
                if currentBeats == 0 or currentBeats == 3 or currentBeats ==4:
                    songString += noteList[i]
                    currentBeats += 2
                elif currentBeats == 1:
                    songString += noteList[i] + " "
                    currentBeats = 3
                elif currentBeats ==2:
                    if noteList[i][0] in accidentals: #AN2
                        songString += noteList[i][0:2]
                        songString += "- "
                        songString += noteList[i][0:2]
                        currentBeats = 4
                    else: #N2
                        songString += noteList[i][0]
                        songString += "- "
                        songString += noteList[i][0]
                        currentBeats = 4                   
                elif currentBeats == 5:
                    if noteList[i][0] in accidentals: #AN2
                        songString += noteList[i][0:2]
                        songString += "- | "
                        songString += noteList[i][0:2]
                        currentBeats = 1
                    else: #N2
                        songString += noteList[i][0]
                        songString += "- | "
                        songString += noteList[i][0]
                        currentBeats = 1
            elif '3' in noteList[i]:
                if currentBeats ==0:
                    songString += noteList[i]
                    songString += " "
                    currentBeats +=3
                elif currentBeats == 1:
                    if noteList[i][0] in accidentals: #AN3
                        songString += noteList[i][0:2]
                        songString += "2- "
                        songString += noteList[i][0:2]
                        currentBeats = 4
                    else: #N3
                        songString += noteList[i][0]
                        songString += "2- "
                        songString += noteList[i][0]
                        currentBeats = 4
                elif currentBeats == 2:
                    if noteList[i][0] in accidentals: #AN3
                        songString += noteList[i][0:2]
                        songString += "- "
                        songString += noteList[i][0:2] + "2"
                        currentBeats = 5
                    else: #N3
                        songString += noteList[i][0]
                        songString += "- "
                        songString += noteList[i][0] +"2"
                        currentBeats = 5
                elif currentBeats == 4:
                    if noteList[i][0] in accidentals: #AN3
                        songString += noteList[i][0:2]
                        songString += "2- | "
                        songString += noteList[i][0:2]
                        currentBeats = 1
                    else: #N3
                        songString += noteList[i][0]
                        songString += "2- | "
                        songString += noteList[i][0]
                        currentBeats = 1
                elif currentBeats == 5:
                    if noteList[i][0] in accidentals: #AN3
                        songString += noteList[i][0:2]
                        songString += "- | "
                        songString += noteList[i][0:2]
                        songString += "2"
                        currentBeats = 2
                    else: #N3
                        songString += noteList[i][0]
                        songString += "- | "
                        songString += noteList[i][0]
                        songString += "2"
                        currentBeats = 2
            """elif '4' in noteList[i]: #worry about these later!
                if currentBeats <=2:
                    songString += noteList[i]
                    currentBeats +=4
            elif '5' in noteList[i]:
                if currentBeats <=1:
                    songString += noteList[i]
                    currentBeats +=5
            elif '6' in noteList[i]:
                if currentBeats == 0:
                    songString += noteList[i]
                    currentBeats +=6"""
        elif currentBeats == 6:
            songString += " | "
            currentBeats = 0
    if currentBeats != 0 and currentBeats != 6:
        songString = songString[:-(currentBeats +1)]
    while songString[-1:] == " " or songString[-1:] == "|":
        songString = songString[:-1]
    songString += " ||"
    return songString

def main():
    source = 'JigsInG.txt'
    k = input("Enter the order of the desired Markov model.   ")
    numNotes = input("Enter the number of desired notes in the output.   ")
    display = input("Do you want the output to be displayed in a musicXML viewer? y/n   ")
    cleaned = songCleaner(source)
    notesList = makeNotesList(cleaned)
    markovDict = makeMarkovDict(notesList, k)
    randomStart =  random.randint(0, len(notesList))
    startNoteList = notesList[randomStart:randomStart+k]
    jig = makeJig(markovDict, numNotes, startNoteList)
    output = makeValidJig(jig)
    jigStream = music21.converter.parse(output)
    print()
    print(output)
    if display:
        jigStream.show()
    
if __name__ == "__main__":
    main()
