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

#%% Functions.

def ReplaceDay(date,datelist):
    # Given a date "##/##" and data, find holidays.
    try:
        test = datelist[date]
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

#%% Calculate non-holiday class days.

course_days = []
course_meetings = []

for i in range(len(data["Sundays"])):
    #week = i+1 # Not sure if I need this, but a reminder to myself.
    [M,W,F] = [data["Mondays"][i],data["Wednesdays"][i],data["Fridays"][i]]
    course_days.append([M,W,F]) # Put dates in course days variable.
    
    # Deal with holidays.
    M = ReplaceDay(data["Mondays"][i],data["Holidays"])
    W = ReplaceDay(data["Wednesdays"][i],data["Holidays"])
    F = ReplaceDay(data["Fridays"][i],data["Holidays"])
    
    # Deal with finals week.
    if i == len(data["Sundays"])-1:
        print("Replacing finals week dates with 'FW's.")
        [M,W,F] = ["FINWK", "FINWK", "FINWK"]
    # End if.
    
    # Input into course meetings variable.
    course_meetings.append([M,W,F])
# End for through semester weeks.

# 5 holidays #num_holidays = course_days.count("H")
# 43 meetings #num_meetings = sum(1 for week in course_days for day in week if day[0].isdigit())

# num_mtgs_w_FW = num_meetings+1 # Represents number of meetings including final.

#%% Get the number of lectures I have.

#prepped_lectures = []

#for i in range(len(data["2360Lectures"])):
    #
# End for.

num_prepped_lectures = sum(1 for lec in data["2360Lectures"] if lec["Topic"] != "NotPrepped")

#%% LaTeX table output.

SPB_flag = 1 # Spring break flag. 1 if before SPB, 0 if after.

lec_num = 0 # Lecture number counter.
ex_num = 0 # Exam number counter.

tab_text = ""
weekday_table = ["M","W","F"] # Index 0 is M for Monday, corresponds to j below.

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
            rowstr = "\multirow{3}{*}{"+f"{i+SPB_flag:02d}"+"}" # Week.
        # End if Monday.
        rowstr += (" & "+day+" & " # Date column
                   +weekday_table[j]+" & ") # Day column
        
        # Handle other holidays.
        if course_meetings[i][j] == "HOLID":
            rowstr += ("{:>9}".format("-")+" & " # Section
                       +data["Holidays"][course_days[i][j]]["Name"] # Topic
                       +" \\\\ \n")
            if j != 2:
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
                         +data["2360Final"]["Date"]+" & "
                         +data["2360Final"]["Day"]+" & "
                         +"\\textbf{FINAL} & "
                         +"Comprehensive final exam, location "
                         +data["2360Final"]["Location"]
                         +" \\\\")
            break
        else: # Input lectures and exams.
            pass
        
        # Need to handle exams here
        try:
            thisexam = data["2360Exams"][course_days[i][j]]
            examstring = "\\textbf{EXAM "+str(thisexam['Number'])+"}"
            print(thisexam)
            rowstr += (examstring
                       +" & "+thisexam["Covers"]
                       +" \\\\ \n")
            print(rowstr)
            if j != 2:
                rowstr += " "*19
            else:
                rowstr += "\midrule \n"
            # End if j == 2.
            tab_text += rowstr
            continue
        except:
            pass
        
        # Input a lecture.
        rowstr += ("{:>9}".format(data["2360Lectures"][lec_num]["Sections"])
                   +" & "
                   +data["2360Lectures"][lec_num]["Topic"])
        
        rowstr += " \\\\ \n"
        
        if j != 2:
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

#%% Put the results into the data and file.
"""
data["rho"] = round(Density,1)

data["rho_uncertainty"] = round(uDensity,1)

with open(infname,"w") as f:
    json.dump(data,f,ensure_ascii=False,indent='\t')
# End with.
"""