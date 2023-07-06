#Abs_table_maker v1.3. Made by Juan Morales López, chemistry student from Universidad de Jaén, Spain. e-mail: jml00032@red.ujaen.es  Date of this version: July 6th of 2023
from docx import Document

def abs_state_reader(file_name):

    """Read the log file in reverse order and create a list of lines"""
    with open(file_name, "r") as file_in:
            lines = file_in.readlines() #generate a list of lines
            lines = list(reversed(lines))
            ini = 0
            fin = 0
            
    """ Check if Gaussian terminated correctly to avoid errors"""
    line = str(lines[0])
    if line.startswith(" Normal termination of Gaussian"):
            print("Normal termination of Gaussian. Reading file.")
    else:
            input("Error: gaussian didn't terminate correctly. Press enter to end program")
            quit()

    """Locate the lines in which the absorption info starts and ends, reading it from the end"""
    abso = False
    for line in lines: #search for the Excitation energies line, which is before the first excited State
            line = str(line)
            if line.startswith(" Excitation energies and oscillator strengths:"):
                abso = True
                break
            else:
                ini = ini + 1
                
    if abso == True:
            print("Absorption data detected. Extracting info.")
    else:
            input("Error: didn't detect absorption data. Press enter to end program")
            quit()

    for line in lines: #search for the SaveETr line, which is after the last excited State
            line = str(line)
            if line.startswith(" SavETr"):
                break
            else:
                fin = fin + 1
              
    selection = list(reversed(lines[fin+1:ini-1])) #Select the lines which contain the absorption info and reverse it again to put them back to normal order
          
    """Detect the number of excited states calculated and store all the info about them"""
    number = 0
    lineposition = 0
    linepositions = []
    states = []
    multiplicities = []
    energies = []
    wavelengths = []
    strengths = []
    for line in selection:
            lineposition = lineposition + 1
            if line.startswith(" Excited State"): #look for the line with the excited state info and count it
                linepositions.append(lineposition - 1)
                spaces = []
                number = number + 1
                words = line.split(" ")
                count = 0
                for word in words: #look for empty spaces in the line and store its positions
                    count = count + 1
                    if word=="":
                        spaces.append(count-1)
                count = 0
                for i_erase in spaces: #erase spaces from the line
                    del words[i_erase - count]
                    count = count + 1    
                state = words[2].split(":")
                state = state[0]
                multiplicity = words[3].split("-")
                multiplicity = multiplicity[0]
                multiplicities.append(multiplicity)
                states.append(state)
                energy = words[4]
                energies.append(energy)
                wavelength = words[6]
                wavelengths.append(wavelength)
                strength = words[8].split("=")
                strength = strength[1]
                strengths.append(strength)
    linepositions.append(len(selection))
                   
    print(str(number) + " Excited States detected in the file.")

    """Detect the transitions and store them"""
    States = []
    for i_selection in range(0,number):
        Transitions = []
        for i_line in range(linepositions[i_selection]+1, linepositions[i_selection + 1]):
            line = selection[i_line]
            if line.startswith("   "): #look for transition lines
                words = line.split("->") #this makes every tipe of log file give the same "words", so we can proceed from now on
                orbital1 = words[0].strip()
                words2 = words[1].split(" ")
                count = 0
                spaces2 = []
                for i_word in words2: #look for empty spaces in the line and store its positions
                    count = count + 1
                    if i_word=="":
                        spaces2.append(count-1)
                count = 0
                for i_erase in spaces2: #erase spaces from the line
                    del words2[i_erase - count]
                    count = count + 1  
                orbital2 = words2[0]
                orbitals = orbital1 + "->" + orbital2
                words3 = float(words2[1].rstrip()) #eliminate \n symbol
                contrib = words3*words3 * 200
                contrib = int(contrib)
                if contrib>=15: #include all the transitions with contribution equal or superior to 15%
                    transition = [orbitals, contrib]
                    Transitions.append(transition)
        state = [states[i_selection], multiplicities[i_selection], energies[i_selection], wavelengths[i_selection], strengths[i_selection], Transitions]
        States.append(state)
        print("Excited State " + states[i_selection] + " is a " + multiplicities[i_selection] + " with " + energies[i_selection] + " eV of energy, " + wavelengths[i_selection] + " nm of wavelength and " + strengths[i_selection] + " oscillator strength. It has " + str(len(Transitions)) + " transitions with a contribution >= than 15%")
    print("Data added to the table.\n")
    return States