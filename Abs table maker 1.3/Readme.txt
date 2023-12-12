Welcome to Abs_table_maker 1.3!! Programmed by Juan Morales López, chemistry student at Universidad de Jaén, Spain. e-mail: jml00032@red.ujaen.es Date of this version: July 6th of 2023
Feel free to e-mail me to write problems and suggestions with the use of this program (after reading the Readme file, of course!)

------- Table of contents: ---------------------------------------
1. What is Abs table maker and what do I need to use it.
2. How to prepare to use it.
3. How to use it.
4. FAQ
5. Change list


--------------------- 1. What is Abs table maker and what do I need to use it? ----------------------------
It is a python program to automatize the process of writing absorbance tables in the same format as tables in Computational Chemistry papers. By now, it is only compatible with Gaussian 16 (not revised in previous versions, log files may change).
You only need the ".log" files from your absorbance calculations as input for the program, and you will get a ".docx" file with the table in an appropriate format like this: 
                (ID file number,          experimental energies (and wavelengths),            calculated energies (and wavelengths) (and DeltaE with experimental peaks),          transitions,         oscillator strength,            % contributions)

- You need to install Python in your machine and also to install "python-docx" library for it: just write "pip install python-docx" in your CMD screen in Windows, or other similar formulas to install Python libraries.
- You need a program able to read ".docx" documents(i.e. Microsoft Word, OpenOffice...), since the final table will be written in such format.


-------------------- 2. How to prepare to use it. ---------------------------------------------------------
I recommend you to do this.
- Install python (the most recent version available) and install python-docx.
- Move your Gaussian absorbance .log files into "input" folder and enumerate them in the order that you want them analyzed. Example: compound_1.log should be renamed as 1.compound_1.log. This is just to be sure that you don't mess up the input process manually.
- Think about which f (oscillator strength) you want the program to retain (according to your requirements).
- In case you want to compare your calculations with experimental absorbance data, gather the wavelength of the peaks (in nm).


-------------------- 3. How to use it. --------------------------------------------------------------------
After you install Python and python-docx, you can just execute (double click) Abs_table_maker (manual).py, but the program will ask you some questions that you need to correctly answer to proceed.

"How many log files do you want to use to make your table?:"
- You just need to write a number, like 4, if you want to add 4 different log files to your table, and then press enter. The program will ask you then for 4 different .log files to gather information from them.

"Which is the minimum oscillator strength (f) that you want to include in your transitions? (S0->S1 will always be included):"
- Again, just input a number. This filters transitions below a certain oscillator strength threshold set by the user. S0->S1 is always included, even with f = 0, since it's usually valuable for some calculations. Leave it at 0 if you want no filter.

"How many experimental absorbance peaks do you want to use as reference?"
- Again, input a number. Leave this number to 0 if you don't want to use this feature. This is a bit more complicated, but usually we need to compare the energy of our calculated absorbance peaks with experimental data, in which case the program will do
it for you, even for many experimental peaks. Most people just compare with 1 experimental peak (the one of highest wavelength or lower energy) and calculate the energy difference (in eV) between experimental and calculated data. If you choose 2 or more
in this option, the program will calculate the energy difference between your calculated transitions and all of the experimental peaks given, and will retain the lowest difference in energy of all of them (you will see it in the table, on the third column, 
last number). 

"Write (in nm) the wavelength of experimental absorbance number " n " "
- In case you put something other than 0 in the previous option, the program will ask you for the wavelength of your experimental absorbance peaks (in nm, in number).
Example 1: you choose "1" absorbance peak and write "358" in this option. That is 358 nm. The program will calculate the energy of the peak (3.45 eV) based on the wavelength. It will calculate the energy difference between the experimental peak
of 358 nm and all of your calculated absorbance peaks (which you will see on the table, third column, last number). If one of your calculated absorbance peak is, for example, of 422 nm (2.94 eV), the energy difference will be 2.94 - 3.45 = -0.51 eV and 
in the third column you will see: 2.94 (422) -0.51.
Example 2: you choose "2" absorbance peaks and write "358" nm (3.45 eV) and "489" nm (2.54 eV). Your calculated abs peak is, again, of 422 nm (2.94 eV). DeltaE1 = 2.94 -3.45 = -0.51 eV.   DeltaE2 = 2.94 - 2.54 = 0.4, which is smaller (in absolute value),
so in the third column you will see: 2.94 (422) 0.4.

"Drag the log file number " n " into the command screen and press enter: "
- In this case, literally, drag the first .log file that you want to include in your table to the command screen and press enter (when you do this, the path for the file will be entered as input into the program and it will be able to read it).

Repeat this cicle for all your .log files and voilá! Job done.

After all, your "AbsTable.docx" file with the table will be stored in the "output" folder of this program.


------------------- 4. FAQ. -----------------------------------------------------------------------------

!!!!Work in progress!!!!
4.1 ---After I write the answer to any of the questions I get the message "Error detected. Please check your inputs. Press enter to close". What is the problem?---
In this case, usually you didn't write the input in the desired format. Please check section 3. of this document to check the desired input format.

4.2 ---After I drag a .log file and press enter I get this error message: "Error: gaussian didn't terminate correctly. Press enter to end program"---
I hope the error messages are self explanatory in this case. Open your .log files with any text processor to check if Gaussian terminated correctly (last line should be "Normal termination of Gaussian 16 at..."). If it didn't, the program won't process
it to avoid any bad data in your table (this should act as an alarm for the user, since with the program doing all the hard work you don't have a reason to open the .log file) and you will have to start again without that file.

4.3 ---Same situation, but: "Error: didn't detect absorption data. Press enter to end program"---
 If it doesn't detect the "Excitation energies and oscillator strengths:" line, the program will know that your file doesn't contain absorbance data (such as an Opt calculation), so it won't process the file to avoid any bad data in your table and
you will have to start again without that file.

4.4 ---The program reads all the files normally, but after I input the last .log file and press enter it says "Error detected. Please check your inputs. Press enter to close". What is the problem?---
If the last .log file is correct (Gaussian terminated correctly, it is an absorption file...), then check if you have opened "AbsTable.docx" (the output file) while running the program. If so, close it and the problem will solve. The program will always
try to write in "/output/AbsTable.docx" and, if it's already open (because you are looking at a previous attempt, for example), it won't have permission to write on it and will generate an error (in this case it's a generic error message).
If this is not your case, check that you are double clicking Abs_table_maker (manual).py instead of executing it through CMD (in Windows systems). If you don't double-click the file, it won't be able to find the "/output" folder to write "AbsTable.docx"
and the program will fail and close.

4.5 ---The orbital transitions (and %contributions) don't match the shape of the table---
Keep in mind that the output AbsTable.docx is a table with almost no format done. If you experience weird shapes in your table, just manually adjust the length of each column until all of them have the proper length to display all the information they contain.
The most notable example is in the last column "%Contribution": when there's 3 or more different orbital transitions, you must enlarge the column so it can display all of them. If not, your data won't match reality. To be sure that all the data is correct,
just look that, at the end of the table, all of the columns match each other and there's no empty cells.

4.6 ---I'm not sure how the output table should look like---
In the "output" folder I have included an example AbsTable.docx made from a .log file (included in the "input" folder) with 200 transitions. It's the raw output, just with the column length manually adjusted to fit the results.
I hope it helps you understand how a proper result should look like in case of doubt.

4.6 ---Other random errors such as the program closing while reading a file---
By now, I've just put some output messages inside the program to help you track your progress and possible errors, but some unexpected errors may occur and the program could close without an error message. Usually, this kind of errors will happen 
because your .log file contains unusual data that I didn't expect to encounter, so check the transitions lines specially to look for any differences between it and the rest of your files and send me an e-mail with a description of the problem and your
.log file so I can fix it. 
(if you are used to python, you can erase lines 10 and 101, the "try" and "except" commands, then remove the indentation for the whole block and execute the program with CMD, in which case you will get a traceback message which will give you some 
hints about the error cause). 

----------------- 5. Change list. -----------------------------------------------------------------------
-------- From 1.0 to 1.1 ---------
- Solved error when for a transition there were no contributions of 15% or more. Now, the program just leaves a blank line to notice it.
- Added os module at start to set pathing and avoid some errors with the output file.
- Solved some issues in which the program would close after detecting an error before the user could read the error message.

-------- From 1.1 to 1.2 ---------
- Solved error in .log reading process when transitions format changed from "      301 ->310       " to "       301 -> 310       "" (space after the arrow). Now it reads both cases correctly.

-------- From 1.2 to 1.3 ---------
- Solved error in which the program wouldn't ask empty space if no transitions had contributions over 15%, now it leaves a message indicating it.

