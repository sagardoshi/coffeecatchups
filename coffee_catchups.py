#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.


import csv
import codecs
from random import randrange

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sectionList = ["A", "B", "C", "D"]

namesDict = {}

for section in sectionList:
    namesDict[section] = []

matchedDict = {}

errors = {"repeatMatch": 0}


def coffee_catchups():
    
    with open('MBA_Student_List.csv', 'rU') as infile:
        reader = csv.reader(open('MBA_Student_List.csv', 'rU'), delimiter=",", dialect=csv.excel_tab)
        # reader = reader.encode('utf-8')
        studentList = list(reader)
        
        # Improve legibility of CSV rows
        for bioData in studentList[1:]:
            title = bioData[0]
            firstName = bioData[1]
            middleName = bioData[2]
            lastName = bioData[3]
            email = bioData[4]
            assignedSection = bioData[5]
            namesDict[assignedSection].append(firstName + " " + lastName + " (" + assignedSection + ")" + "$$$" + email)
        


        # Loop through each section's members from A through D and build a schedule for each
        for section in sectionList:
            for name in namesDict[section]:
                build_user_schedule(name)

    with codecs.open('coffee_catchups.csv', 'wb') as outfile:
        
        writer = csv.writer(outfile, delimiter=",")

        writer.writerow(['User', 'Week 1', 'Week 1 Email', 'Week 2', 'Week 2 Email', 'Week 3', 'Week 3 Email', 'Week 4', 'Week 4 Email', 'Week 5', 'Week 5 Email',
                                 'Week 6', 'Week 6 Email', 'Week 7', 'Week 7 Email', 'Week 8', 'Week 8 Email', 'Week 9', 'Week 9 Email', 'Week 10', 'Week 10 Email'])



        for key in sorted(matchedDict.keys()):
            names = [key.split("$$$")[0].upper()]
            # print value
            
            for name in matchedDict[key]:
                names.append(name)
            # print names
            writer.writerow(names)

    infile.close()
    outfile.close()

    return


def build_user_schedule(user):
    orderedPairings = []

    # Select 10 compadres; 1 for each week of the term
    for i in range(1, 11):
        compadreName = select_fresh_pairing(user, orderedPairings)        
        orderedPairings.append(compadreName.split("$$$")[0])
        orderedPairings.append(compadreName.split("$$$")[1])

    # Add collection of compadres as value given user (key) to dict
    matchedDict[user] = orderedPairings

    # Print that user's schedule cleanly
    # print_user_schedule(user, matchedDict)

    return


def select_fresh_pairing(user, orderedPairings):
    
    # Select initial compadre
    compadreName = find_compadre_for_user(user, orderedPairings)

    # Be sure this pairing hasn't occurred the other way around
    while (namesDict.has_key(compadreName) and namesDict[compadreName] == user):
        errors["repeatMatch"] = errors["repeatMatch"] + 1  # Error Tracking
        compadreName = find_compadre_for_user(user, orderedPairings)

    return compadreName



def print_user_schedule(user, matchedDict):

    # Print user and user's schedule more legibly
    print "*** " + user.upper() + " ***"

    for element in matchedDict[user]:
        print "Week " + str(matchedDict[user].index(element) + 1) + ": " + element
    print
    return


def find_compadre_for_user(nombre, orderedPairings):

        # PICKING A SECTION
        compadreSection = sectionList[randrange(0, len(sectionList))]

        # Keep picking new sections until no longer the current user's section
        while nombre in namesDict[compadreSection]:
            compadreSection = sectionList[randrange(0, len(sectionList))]

        # PICKING A COMPADRE
        compadreName = namesDict[compadreSection][randrange(0, len(namesDict[compadreSection]))]

        # Be sure not to repeat compadres for this user during the term
        while compadreName in orderedPairings:
            compadreName = namesDict[compadreSection][randrange(0, len(namesDict[compadreSection]))]                

        return compadreName

coffee_catchups()

