# -*- coding: utf-8 -*-
"""
Jeremiah Rittenhouse
Professor, Missouri University of Science and Technology

08/12/2024
"""

#%% Imports.

import numpy as np
import json
import os

#%% Control panel.

MWF = True
TTh = False

coursenumber = "3313"

#%% Functions.

def ReplaceDay(date,datelist):
    # Given a date "##/##" and data, find holidays.
    try:
        test = datelist[date]
        print("Replacing a day, "+str(datelist[date]))
        return(datelist["Symbol"])
    except KeyError:
        return(date)
    except: # Any other error.
        print("Incorrectly formatted data file?")
    # End try holiday
    return()
# End def TryHoliday().

#%% Input file handling.

__location__ = os.path.realpath(
    os.path.join(os.getcwd(),os.path.dirname(__file__)))

relfname = "SP2025Calendar.json"

infname = os.path.join(__location__,relfname)

#%% Calendar dates input.

with open(infname) as f:
    data = json.load(f)
    #print(data)
# End with.

#%% Assign weekdays based on MWF and TTH true/false.

if MWF:
    weekdays = ["Mondays","Wednesdays","Fridays"]
    weekday_table = ["M","W","F"]
elif TTh:
    weekdays = ["Tuesdays","Thursdays"]
    weekday_table = ["T","Th"]
else:
    KeyError("Neither MWF nor TTh were true.")
# End if else MWF/TTh.

#%% Calculate non-holiday class days.

course_days = []
course_meetings = []

for i in range(len(data["Sundays"])):
    #week = i+1 # Not sure if I need this, but a reminder to myself.
    weekdaydata = []
    coursedaydata = []
    for j,day in enumerate(weekdays):
        coursedaydata.append(data[day][i]) # If course_days gets weekdaydata, later modifications to weekdaydata affect course_days.
        weekdaydata.append(data[day][i])
    # End for day in weekdays.
    
    course_days.append(coursedaydata) # Put dates in course days variable.
    
    # Deal with holidays.
    for j,daydata in enumerate(weekdaydata):
        weekdaydata[j] = ReplaceDay(data[weekdays[j]][i],data["Holidays"]) # 
    # End for through weekdaydata.
    print(weekdaydata)
    
    # Deal with finals week.
    if i == len(data["Sundays"])-1:
        print("Replacing finals week dates with 'FINWK's.")
        for j,daydata in enumerate(weekdaydata):
            weekdaydata[j] = "FINWK"
        # End for daydata in weekdaydata.
        #[M,W,F] = ["FINWK", "FINWK", "FINWK"]
    # End if.
    
    # Input into course meetings variable.
    course_meetings.append(weekdaydata)
# End for through semester weeks.

#num_prepped_lectures = sum(1 for lec in data[coursenumber+"Lectures"] if lec["Topic"] != "NotPrepped")
num_prepped_lectures = sum(1 for lec in data[coursenumber+"MWFLectures"] if lec["Topic"] != "NotPrepped")

#%% LaTeX table output.

SPB_flag = 1 # Spring break flag. 1 if before SPB, 0 if after.

lec_num = 0 # Lecture number counter.
ex_num = 0 # Exam number counter.

tab_text = ""

for i,week in enumerate(course_days):
    for j,day in enumerate(week):
        rowstr = ""
        
        # Handle spring break first because it doesn't use a multirow.
        if course_meetings[i][j] == "HOLID":
            if data["Holidays"][course_days[i][j]]["Name"] == "Spring break":
                if SPB_flag == 0: # Skip multiple entries of spring break.
                    continue
                rowstr += ("Break"+" "*15+"&" # Week
                           +" "*7 # Date
                           +"&   & " # Day
                           +"{:>9}".format("-") # Section
                           +" & Spring break \\\\ \n \\midrule \n") # Topic
                tab_text += rowstr
                SPB_flag=0
                continue # Skips to next loop iteration.
            # End if spring break.
        # End if holiday.
        
        # Handle multirow entry for all Mondays except spring break.
        if j == 0: # Monday.
            rowstr = "\multirow{"+str(len(weekday_table))+"}{*}{"+f"{i+SPB_flag:02d}"+"}" # Week.
        # End if Monday.
        rowstr += (" & "+day+" & " # Date column
                   +"{:>2}".format(weekday_table[j])+" & ") # Day column
        
        # Handle other holidays.
        if course_meetings[i][j] == "HOLID":
            rowstr += ("{:>9}".format("-")+" & " # Section
                       +data["Holidays"][course_days[i][j]]["Name"] # Topic
                       +" \\\\ \n")
            if j != len(weekday_table)-1:
                rowstr += " "*19
            else:
                rowstr += "\midrule \n"
            # End if j == 2.
            tab_text += rowstr
            continue # Keeps iteration counter from increasing on holidays.
        # End if holiday but not spring break.
        
        # Handle finals week.
        elif course_meetings[i][j] == "FINWK":
            tab_text += ("{:>18}".format("16")+"  & "
                         +data[coursenumber+"Final"]["Date"]+" & "
                         +data[coursenumber+"Final"]["Day"]+" & "
                         +"\\textbf{FINAL} & "
                         +"Final exam, "
                         +data[coursenumber+"Final"]["Time"]
                         +", location "+data[coursenumber+"Final"]["Location"]
                         +" \\\\")
            break
        else: # Input lectures and exams.
            pass
        
        # Need to handle exams here
        try:
            thisexam = data[coursenumber+"Exams"][course_days[i][j]]
            examstring = "\\textbf{EXAM "+str(thisexam['Number'])+"}"
            print(thisexam)
            rowstr += (examstring
                       +" & "+thisexam["Covers"]
                       +" \\\\ \n")
            print(rowstr)
            if j != len(weekday_table)-1:
                rowstr += " "*19
            else:
                rowstr += "\midrule \n"
            # End if j == 2.
            tab_text += rowstr
            continue
        except:
            pass
        
        # Input a lecture.
        """
        rowstr += ("{:>9}".format(data[coursenumber+"Lectures"][lec_num]["Sections"])
                   +" & "
                   +data[coursenumber+"Lectures"][lec_num]["Topic"])
        """
        rowstr += ("{:>9}".format(data[coursenumber+"MWFLectures"][lec_num]["Sections"])
                   +" & "
                   +data[coursenumber+"MWFLectures"][lec_num]["Topic"])
        #"""

        rowstr += " \\\\ \n"
        
        if j != len(weekday_table)-1:
            rowstr += " "*19
        else:
            rowstr += "\midrule \n"
        # End if j == 2.
        tab_text += rowstr
        lec_num += 1
    # End for through week.
# End for through all weeks.
print(tab_text)
print(lec_num)

#%% Put the calendar into a text data file.
outfname = coursenumber+"CalendarTableText.txt"

with open(outfname,"w") as f:
    f.write(tab_text)
    #json.dump(data,f,ensure_ascii=False,indent='\t')
# End with.