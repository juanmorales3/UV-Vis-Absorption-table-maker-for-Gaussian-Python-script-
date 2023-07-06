#Abs_table_maker v1.3. Made by Juan Morales López, chemistry student from Universidad de Jaén, Spain. e-mail: jml00032@red.ujaen.es  Date of this version: July 6th of 2023

from docx import Document
from programs.Abs_state_reader import abs_state_reader
import os

currentdir = os.getcwd()
os.chdir(currentdir) #set the current directory as Python directory to avoid errors in pathing

try:
    document = Document()
    number = int(input("How many log files do you want to use to make your table?: "))
    number2 = float(input("Which is the minimum oscillator strength (f) that you want to include in your transitions? (S0->S1 will always be included):"))
    number3 = int(input("How many experimental absorbance peaks do you want to use as reference?"))
    Absor = [] #This vector contains all of the experimental absorbance values given by the user, as energy in eV
    Wave = [] #This vector contains all of the experimental absorbance values given by the user, as wavelength in nm
    for i_number in range(1,number3+1):
        absor = float(input("Write (in nm) the wavelength of experimental absorbance number " + str(i_number) + ": "))
        Wave.append(absor)
        absor = (1/(absor*pow(10,-9)))*(6.6261*pow(10,-34))*(2.998*pow(10,8))*(1/(1.602*pow(10,-9)))*pow(10,10) #Switch units to eV for comparison
        Absor.append(absor)
     
    """Prepare the first row of the table""" 
    table = document.add_table(rows = number+1, cols = 6) 
    table.columns[0].cells[0].text = "ID"
    table.columns[1].cells[0].text = "eV (nm) exp"
    table.columns[2].cells[0].text = "eV (nm) calc"
    table.columns[3].cells[0].text = "Transition"
    table.columns[4].cells[0].text = "f"
    table.columns[5].cells[0].text = "% Contribution"

    """Add the data for each transition to the table"""
    for i_file in range(1,number+1): #do this for every log file
        path = input("Drag the log file number " + str(i_file) + " into the command screen and press enter: ")  
        path = path.replace("\\", "/")
        path = path.strip("\"")
        States = abs_state_reader(path)
        length = len(States)
        state = States[0] #Prepare the cell text for the first transition   
        cell0 = str(i_file) #Molecule ID
        
        if number3 is not int(0): #do this if the user has selected experimental peaks
            cell1 = str(round(Absor[0],2)) + " (" + str(int(Wave[0])) + ")" #Write first experimental peak
            for i_absor in range(2,len(Absor)+1): 
                cell1 = cell1 + "\n" + str(round(Absor[i_absor-1],2)) + " (" + str(int(Wave[i_absor-1])) + ")" #Write experimental peaks 2 and succesive
        
        if number3 is not int(0): #do this if the user has selected experimental peaks
            distance = 1000  #big number to start
            for i_absor in range(1,len(Absor)+1): #do this for every experimental absorbance energy 
                comp = float(state[2]) - Absor[i_absor-1] #calculate energy difference between calculated transition and experimental transition
                if abs(distance)>abs(comp): #if the difference is less (in absolute value) than the value stored so far, replace the stored value with the difference
                    distance = comp
            cell2 = str(round(float(state[2]),2)) + " (" + str(round(float(state[3]))) + ")" + " " + str(round(distance,2)) #Calculated abs and distance to experimental abs
        else: #do this in case there are no experimental peaks
            cell2 = str(round(float(state[2]),2)) + " (" + str(round(float(state[3]))) + ")" #Calculated abs only
            
        multiplicity = state[1] #This line contains excited states multiplicity
        cell3 = "S_0->" + str(multiplicity[0]) + "_" + "1" #State transition
        cell4 = state[4] #Oscillator strength
        transitions = state[5]
        numberoftrans = len(transitions)
        transition = transitions[0]
        cell5 = str(transition[0]) + " (" + str(transition[1]) + ")" #Add first transition
        
        for i_trans in range(2,numberoftrans+1): #Add the other transitions
            transition = transitions[i_trans-1]
            cell5 = cell5 + ", " + str(transition[0]) + " (" + str(transition[1]) + ")"
            
        for i_state in range(2,length+1): #Add the cell text for the rest of states
            state = States[i_state-1]
            if float(state[4])>=number2: #only add the state if f is equal or greater than the fixed value
                if number3 is not int(0):
                    distance = 1000  
                    for i_absor in range(1,len(Absor)+1):
                        comp = float(state[2]) - Absor[i_absor-1]
                        if abs(distance)>abs(comp):
                            distance = comp
                    cell2 = cell2 + "\n" + str(round(float(state[2]),2)) + " (" + str(round(float(state[3]))) + ")" + " " + str(round(distance,2)) #Calculated abs and distance to experimental abs
                else: #do this in case there are no experimental peaks
                    cell2 = cell2 + "\n" + str(round(float(state[2]),2)) + " (" + str(round(float(state[3]))) + ")" #Calculated abs only
                multiplicity = state[1]
                cell3 = cell3 + "\n" + "S_0->" + str(multiplicity[0]) + "_" + str(i_state)
                cell4 = cell4 + "\n" + state[4]
                transitions = state[5]
                numberoftrans = len(transitions)
                if len(transitions) is not int(0):
                    transition = transitions[0]
                    cell5 = cell5 + "\n" + str(transition[0]) + " (" + str(transition[1]) + ")"
                    for i_trans in range(2,numberoftrans+1): #Add the other transitions
                        transition = transitions[i_trans-1]
                        cell5 = cell5 + ", " + str(transition[0]) + " (" + str(transition[1]) + ")"
                else:
                    cell5 = cell5 + "\n" + "No trans. over 15% contrib."
        table.rows[i_file].cells[0].text = cell0 #Write in the table all the data stored in the cell variables
        if number3 is not int(0):
            table.rows[i_file].cells[1].text = cell1
        table.rows[i_file].cells[2].text = cell2
        table.rows[i_file].cells[3].text = cell3
        table.rows[i_file].cells[4].text = cell4
        table.rows[i_file].cells[5].text = cell5
    document.save(r"output\AbsTable.docx")
    input("Process finished. Press any key to close.")
except:
    input("Error detected. Please check your inputs. Press enter to close")