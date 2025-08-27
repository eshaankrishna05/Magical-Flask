#Coded by: Eshaan Krishna
#Reference: CMPUT 175 e-class reference notes for Stacks and Queues (bqueue.py & bstack.py)

from bqueue import BoundedQueue
from bstack import Stack
import os
"""
    #4 Global Dictionaries. 
    (1) FlaskContent (dict): A dictionary that stores chemicals of each flask.
         - key (str): Flask Number.
         - Value (Stack): Non mixable chemicals in that flask.
    (2) FlaskPosition (dict): A dictionary that stores (x,y) cordinates of each flask for display.
        - key (str): Flask Number.
        - Value (list): (x,y) coordinates for display. 
    (3) FlaskSealed (dict): A dictionary that maintains status of sealed flask. Sealed or Unsealed.
        - Key (str): Flask Number.
        - Value (Str): Status Sealed or Unsealed.
    (4) ANSI (dict): A dictionary that maintains ANSI codes for colors/RESET and CLEARINE.
        - Key (str): Color Name.
        - Value (Str): COrresponding code in ANSI.        
"""
FlaskContent={}
FlaskPosition={}
FlaskSealed={}
ANSI = {
    "SOURCE": "\033[31m",
    "DESTINATION": "\033[32m",
    "AA": "\033[41m",
    "BB": "\033[44m",
    "CC": "\033[42m",
    "DD": "\033[48;5;202m",
    "EE": "\033[43m",
    "FF": "\033[45m",
    "RESET": "\033[0m",
    "CLEARLINE": "\033[0K"
}
"""
    4 Global Constants.
    XCordinate (int): Intial x-coordinate.
    YCordinate (int): Intial y-coordinate.
    MaxStackSize (int): Maximum capacity of each flask.
    MaxFlasksInRow (int): Maximum Number of flasks in a row for display.
    Capacity (int): Capacity of flask
"""
XCordinate=2
YCordinate=1
SealValue=3
MaxStackSize=4
MaxFlasksInRow=4
Capacity=4

def ClearScreen():
    #Clears the screen
    #Input/Output:NA    
    if os.name == "nt": # for Windows
        os.system("cls")
    else: # for Mac/Linux
        os.system("clear")
        
def ClearLine():
    '''
    Clears a line
    Input/Output:NA
    '''
    print(ANSI["CLEARLINE"], end='')
          
def MoveCursor(x, y):
    '''
    Moves the cursor to the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
    Returns: NA
    '''
    print("\033[{1};{0}H".format(x, y), end='')

def DrawHeader():
    '''
    Writes the inital 3 header lines
    Input/Output:NA
    '''
    MoveCursor(XCordinate,YCordinate)
    print('Magical Flask Game')
    MoveCursor(XCordinate,YCordinate+2)
    ClearLine()
    print('Select source flask:')
    MoveCursor(XCordinate,YCordinate+3)
    ClearLine()
    print('Select destination flask:')
    
    
def FindFlask(filename):
    '''
    Reads the first line of the file and returns the number of the flask and the number of chemicals
    Input:
        - filename (str): Name of the file
    Returns:
        - NoOfFlasks, NoOfChemicals (Int): As the name suggests
    '''
    f=open(filename,'r')
    FlaskType=f.readline()
    temp=FlaskType.split()
    f.close()
    NoOfFlasks=int(temp[0])
    NoOfChemicals=int(temp[1])
    return(NoOfFlasks, NoOfChemicals)

def MakeStackandUnseal(NoOfFlasks):
    '''
    Creates 2 Dictionaries, that can be changed globally. FlaskContent dictionary stores the chemicals content
    (Stacked) for each flask and FlaskSealed dictionary stores status of flask (Sealed or unsealed) 
    Input:
       - NoOfFlasks (str): Number of flasks
    Returns: NA
    '''
    global FlaskContent
    global FlaskSealed
    for i in range(1, NoOfFlasks+1):
        key="Flask"+str(i)
        FlaskContent[key]=Stack()
        
    for i in range(1, NoOfFlasks+1):
        key="Flask"+str(i)
        FlaskSealed[key]="No"
        

def DefinePosition(NoOfFlasks):
    '''
    Creates a dictionary, that stores the (x,y) position of each element of stack (Chemical) for each flask.
    This is done so that the chemical can move when poured. 
    Input:
       - NoOfFlasks (str): Number of flasks
    Returns: NA
    '''
    global FlaskPosition
    #Checks if we have a case of 4 or less than four Flasks or greater than 4 Flasks
    
    if NoOfFlasks<=MaxFlasksInRow:
        IntialFourInRow=NoOfFlasks #4 or less than four Flasks case
    else:
        IntialFourInRow=MaxFlasksInRow #greataer than 4 Flasks
    x=XCordinate
    y=YCordinate+8
    for i in range(1, IntialFourInRow+1): 
        key="Flask"+str(i)
        FlaskPosition[key]=[[x,y],[x,y-1],[x,y-2],[x,y-3]]
        x=x+6
        y=YCordinate+8

    #This part is executed only if greater than 4 Flasks
    if NoOfFlasks > MaxFlasksInRow:
        x=XCordinate
        y=YCordinate+15
        for i in range(IntialFourInRow+1, NoOfFlasks+1): 
            key="Flask"+str(i)
            FlaskPosition[key]=[[x,y],[x,y-1],[x,y-2],[x,y-3]]
            x=x+6
            y=YCordinate+15
    
def AddContent(filename):
    '''
    This module reads chemical from file and adds it to Bounded Queue or discards - based on the capacity of the Queue.
    Simultaneously it transfers from Queue to flask, based the data it reads from file. 
        Input:
       - filename (str): Name of the file
    Returns: NA
    '''    
    global FlaskContent
    bq=BoundedQueue(Capacity)
    f=open(filename,'r')
    #Skip the line of the file, as it contains flask number and Chemical number
    data=f.readline() 
    data=f.readline()
    data=data.strip()
    
    while data !="":
        #This is a case of transfer from Queue to flask
        if data[:1].isdigit():
            DequeueNo=data[0] 
            FlaskNo=data[-1]
            for i in range(0,int(DequeueNo)): 
                key="Flask"+FlaskNo
                #Dequeue from Queue and push it into flask, that is a Stack
                FlaskContent[key].push(bq.dequeue()) 

        #If Queue is full and chemical is met, skip that chemical                 
        if not bq.isFull() and data.isalpha():
            #else keep enqueuing to the Queue
            bq.enqueue(data) 
  
        data=f.readline()
        data=data.strip()
    f.close()

def DrawNumbers(NoOfFlasks):
    '''
    This module displays flask numbers for flasks
    Input:
       - NoOfFlasks (str): Number of Flasks
    Returns: NA
    '''
    #Checks if we have a case of 4 or less than four Flasks or greater than 4 Flasks
    if NoOfFlasks<=MaxFlasksInRow:
        #4 or less than four Flasks case
        IntialFourInRow=NoOfFlasks 
    else:
        #Greater than 4 Flasks
        IntialFourInRow=MaxFlasksInRow 
    x=XCordinate+1
    for i in range(1,IntialFourInRow+1):
        MoveCursor(x,YCordinate+10)    
        print(str(i),end="")
        x=x+6
        
    #This part is executed only if greater than 4 Flasks    
    if NoOfFlasks > MaxFlasksInRow:
        x=XCordinate+1
        for i in range(IntialFourInRow+1,NoOfFlasks+1):
            MoveCursor(x,YCordinate+17)    
            print(str(i),end="")
            x=x+6
    
def DrawFlaskInner(Initial,IntialFourInRow,Lower):
    """
    This module displays Flasks
    Input:
       - Initial (int): The start index of a four column line
       - IntialFourInRow: The final index of the four column line
       - Lower (int): Y-Coordinate position of display
    Returns: NA
    """
    global FlaskContent
    global FlaskPosition
    
    #Displaying the bottom of the flask
    x=XCordinate
    for i in range(Initial, IntialFourInRow+1):
        MoveCursor(x,Lower-1)
        print("+--+",end="")
        x=x+6
   
    for i in range(Initial, IntialFourInRow+1):
        #Identify the flask
        key="Flask"+str(i)
        StackList=str(FlaskContent[key]).split()
        difference=MaxStackSize-FlaskContent[key].size()
        
        #Displaying the Flask and its chemical in the flask 
        for j in range(0,FlaskContent[key].size()):
            MoveCursor(FlaskPosition[key][j][0],FlaskPosition[key][j][1])
            Content=ANSI[StackList[j]] + StackList[j] + ANSI["RESET"]
            print("|"+ Content +"|",end="")
            
        #Displaying the top of Flask that may be empy and does not contain the chemical     
        if difference!=0:
            for j in range(FlaskContent[key].size(),MaxStackSize):
                MoveCursor(FlaskPosition[key][j][0],FlaskPosition[key][j][1])
                print("|"+"  "+"|",end="")
   
def DrawFlask(NoOfFlasks):
    """
    This module displays Flasks
    Input:
       - NoOfFlasks (int): Number of Flasks
    Returns: NA
    """
    #Checks if we have a case of 4 or less than four Flasks or greater than 4 Flasks
    if NoOfFlasks<=MaxFlasksInRow:
        #4 or less than four Flasks case
        IntialFourInRow=NoOfFlasks  
    else:
        #Greater than 4 Flasks
        IntialFourInRow=MaxFlasksInRow 
    Initial=1
    Lower=YCordinate+10
    DrawFlaskInner(Initial,IntialFourInRow,Lower)

    #This part is executed only if greater than 4 Flasks
    if NoOfFlasks >MaxFlasksInRow:
        IntialFourInRow=NoOfFlasks
        Initial=MaxFlasksInRow+1
        Lower=YCordinate+17
        DrawFlaskInner(Initial,IntialFourInRow,Lower)

def ColorNumbers(Target,Flask,NoOfFlasks):
    """
    This module displays flask numbers for flasks with colors 
    Input:
       - NoOfFlasks (int): Number of Flasks
    Returns: NA
    """
    #Checks if we have a case of 4 or less than four Flasks or greater than 4 Flasks
    if NoOfFlasks<=MaxFlasksInRow:
        #4 or less than four Flasks case
        IntialFourInRow=NoOfFlasks 
    else:
        #Greater than 4 Flasks
        IntialFourInRow=MaxFlasksInRow 
    x=XCordinate+1
    for i in range(1,IntialFourInRow+1):
        
        if str(i)==Target:
            Content= ANSI[Flask] + Target  + ANSI["RESET"]
            MoveCursor(x,YCordinate+10)    
            print(Content,end="")
        x=x+6
        
    #This part is executed only if greater than 4 Flasks  
    if NoOfFlasks > MaxFlasksInRow:
        x=XCordinate+1
        for i in range(IntialFourInRow+1,NoOfFlasks+1):
            if str(i)==Target:
                Content= ANSI[Flask] + Target  + ANSI["RESET"]
                MoveCursor(x,YCordinate+17)    
                print(Content,end="")
            x=x+6
          
def TakeInputSource(NoOfFlasks):
    """
    This module takes input(Flask Number) for source flask
    Input:
       - NoOfFlasks (int): Number of Flasks
    Returns:
       - UserInput1 (str): Source flask Number
    """
    global FlaskContent
    global FlaskSealed
    ValidInputs=[]
    TakeAnInput=True
    #Makes a list of valid Inputs
    for i in range(1,NoOfFlasks+1):
        ValidInputs.append(str(i))
    ValidInputs.append("EXIT")

    #Asks for source flask number until Valid Input
    while TakeAnInput:
        MoveCursor(XCordinate,YCordinate+2)
        ClearLine()
        print('Select source flask:', end='')
        MoveCursor(23,YCordinate+2)
        UserInput1 = input().strip().upper()
        #Checks for valid options
        if UserInput1 in ValidInputs:
            if UserInput1!="EXIT":
                key="Flask"+UserInput1 
                if FlaskContent[key].isEmpty() or FlaskSealed[key]=="Yes":
                    MoveCursor(XCordinate,YCordinate+4)
                    ClearLine()
                    print('Cannot pour from that flask. Try again.',end='')
                else:
                 TakeAnInput=False
            else:
                TakeAnInput=False
        else:
            MoveCursor(XCordinate,YCordinate+4)
            ClearLine()
            print('Invalid Input. Try again.', end='')
    #Displays valid source flask Number and returns the valid source Flask Numner             
    MoveCursor(XCordinate,YCordinate+4)
    ClearLine()
    return UserInput1

def TakeInputDestination(NoOfFlasks):
    """
    This module takes input(flask Number)for destination flask
    Input:
       - NoOfFlasks (int): Number of Flasks
    Returns:
       - UserInput2 (str): Destination flask Number
    """
    global FlaskContent
    global FlaskSealed
    #Makes a list of valid Inputs
    ValidInputs=[]
    TakeAnInput=True
    for i in range(1,NoOfFlasks+1):
        ValidInputs.append(str(i))
    ValidInputs.append("EXIT")
    #Asks for destination flask number until Valid Input
    while TakeAnInput:
        MoveCursor(XCordinate,YCordinate+3)
        ClearLine()
        print('Select destination flask:', end='')
        MoveCursor(28,YCordinate+3)
        UserInput2 = input().strip().upper()
        #Checks for valid options
        if UserInput2 in ValidInputs:
            if UserInput2!="EXIT":
                key="Flask"+UserInput2 
                if FlaskContent[key].size()==MaxStackSize or FlaskSealed[key]=="Yes":
                    MoveCursor(XCordinate,YCordinate+4)
                    ClearLine()
                    print('Cannot pour into that flask. Try again.',end='')
                else:
                    TakeAnInput=False
            else:
                TakeAnInput=False
        else:
            MoveCursor(XCordinate,YCordinate+4)
            ClearLine()
            print('Invalid Input. Try again.', end='')
    #Displays valid destinationflask Number and returns the valid destination Flask Numner               
    MoveCursor(XCordinate,YCordinate+4)
    ClearLine()
    return UserInput2

def ExchangeStack(UserInput1, UserInput2):
    """
    This module pours chemical from source flas to destination flask
    Input:
       - UserInput1 (str): Source flask Number
       - UserInput2 (str): Destination flask Number
    Returns: NA
    """
    global FlaskContent
    global FlaskPosition
    #Pops Source flask Stack and stores in popped. Validation of flask Numbers already done at TakeInputsource.
    Source="Flask"+UserInput1
    Destination="Flask"+UserInput2
    Index=FlaskContent[Source].size()-1
    Popped=FlaskContent[Source].pop()
   
       
    MoveCursor(FlaskPosition[Source][Index][0],FlaskPosition[Source][Index][1])
    print("|"+"  "+"|", end="")

    #Pushes popped into destination flask.Validation of flask Numbers already done at TakeInputdestination.
    FlaskContent[Destination].push(Popped)
    Index=FlaskContent[Destination].size()-1
    Peek=FlaskContent[Destination].peek()
    Content=ANSI[Peek] + Peek + ANSI["RESET"]
    MoveCursor(FlaskPosition[Destination][Index][0],FlaskPosition[Destination][Index][1])
    print("|"+Content+"|", end="")

def CheckSealSourceDestination(Target):
    """
    This module initiates a seal operation for source and destination 
    Input:
       - Target (str): Source flask Number/ or destination flask Number.
       - UserInput2 (str): Destination flask Number
    Returns: NA
    """
    global FlaskContent
    global FlaskPosition
    global FlaskSealed
    #if Size of flask stack is equal to seal Value annd all chemicals are same, then seal the flask.   
    if FlaskContent[Target].size()==SealValue:
    #Once there are seal value chemicals in flask, it checks if all chemicals are same.    
        Temp=str(FlaskContent[Target]).split()
        First=Temp[0]
        Different=False
        
    #flags if one of the three chemicals are different.
        for Element in range(1,SealValue):
            if First != Temp[Element]:
                Different=True
                
    #All chemicals found to be same, so flask is sealed.            
        if not Different:
            Index=FlaskContent[Target].size()
            MoveCursor(FlaskPosition[Target][Index][0],FlaskPosition[Target][Index][1])
            print("+--+", end="")
            FlaskSealed[Target]="Yes"
            
def CheckSeal(UserInput1, UserInput2):
    """
    This module initiates a seal operation for source and destination 
    Input:
       - UserInput1 (str): Source flask Number
       - UserInput2 (str): Destination flask Number
    Returns: NA
    """
    Source="Flask"+UserInput1
    Destination="Flask"+UserInput2
    CheckSealSourceDestination(Source)
    CheckSealSourceDestination(Destination)
            
def CheckWinner(NoOfChemicals):
    """
    This module check if a winner can be declared or not.
    Input:
       - NoOfChemicals (int): Number of chemicals 
    Returns:
       - True/False (bool): True for winner declared/ False for not yet. 
    """
    global FlaskSealed
    Counter=0
    #If Number of chemicals is equal to No of seled flasks, then a winnner is declared
    for key, value in FlaskSealed.items():
        if FlaskSealed[key]=="Yes":
            Counter+=1

    if Counter==NoOfChemicals:
        return True
    else:
        return False
    
def DeclareWinner(NoOfFlasks):
    """
    This module declares winner and displays at correct position
    Input:
       - NoOfFlasks (int): Number of Flasks
    Returns: NA
    """
    if NoOfFlasks<=MaxFlasksInRow:
        MoveCursor(XCordinate,YCordinate+12)
    else:
        MoveCursor(XCordinate,YCordinate+19)
    ClearLine()
    print("You win!",end="")
                
def main():
    """
    This is main module that calls all sub modules
    Input: NA
    Returns: NA
    """  
    global FlaskContent
    global FlaskPosition
    ClearScreen()
    DrawHeader()
    
    #Pass input file as varible.   
    filename="8f6c.txt"
    #Get Number of chemicals and Number of flasks.
    NoOfFlasks, NoOfChemicals=FindFlask(filename)

    #Set the 2 global dictionaries with initial data. MakeStackandUnseal dict seta flasks as unsealed.
    #DefinePosition dict sets (x,y) coordinate position of flask for display
    MakeStackandUnseal(NoOfFlasks)
    DefinePosition(NoOfFlasks)
    
    #Display the all the flasks with flask numbers with initial chemical contents.
    AddContent(filename)
    DrawFlask(NoOfFlasks)
    DrawNumbers(NoOfFlasks)
    GameOver=False
    Winner=False
    
    while not GameOver and not Winner:
        Check=["EXIT",""]
        UserInput1=""
        UserInput2=""
    #Draw headers and take source flask number as input and add color to flask number, once validation done.
        DrawHeader()
        UserInput1=TakeInputSource(NoOfFlasks)
        
        if UserInput1=="EXIT":
                GameOver=True
        else:
            DrawNumbers(NoOfFlasks)
            Flask="SOURCE"
            Target=UserInput1
            ColorNumbers(Target,Flask, NoOfFlasks)
            
    #Take destination flask Number as input.          
            UserInput2=TakeInputDestination(NoOfFlasks)
            if UserInput2=="EXIT":
                GameOver=True
            else:
    #All inputs validated. Now check the last validation source and destination flask should noy be the same.
    #So Take input until detination flask is not the same as source flask.            
                while UserInput1 == UserInput2 and UserInput2 not in Check and UserInput1 not in Check:
                    MoveCursor(XCordinate,YCordinate+4)
                    ClearLine()
                    print("Cannot pour into the same flask. Try again.", end="") 
                    UserInput2=TakeInputDestination(NoOfFlasks)
    #Once all validation done, add color to detination flask Number.
                Flask="DESTINATION"
                Target=UserInput2    
                ColorNumbers(Target,Flask, NoOfFlasks)
    #Call function to pour chemical from source flask to destination flask and check for winner.       
                if UserInput1 != UserInput2 and UserInput2 not in Check and UserInput1 not in Check:
                    ExchangeStack(UserInput1, UserInput2)
                    CheckSeal(UserInput1, UserInput2)
                    Winner=CheckWinner(NoOfChemicals)
    #If winner is found, declasre the win.         
            if Winner:
                DeclareWinner(NoOfFlasks)

if __name__ == '__main__':
    main()               
        
