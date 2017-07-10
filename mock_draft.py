from numpy import *
from string import *
from random import random

rankings = 'espn_rankings.txt'
#Read rankings from fantasy_rankings.txt
#fname,lname,position = loadtxt('espn_rankings.txt', dtype = str,
#    usecols = (0,1,2), unpack = True)
#pteam = loadtxt('espn_rankings.txt', dtype = str, usecols = 3)
#Convert into an array of name and position.
fname = []
lname = []
positions = []
pteam = []
with open(rankings) as f:
    for line in f:
        strings = line.split()
        if len(strings) == 4:
            fname.append(strings[0])
            lname.append(strings[1])
            positions.append(strings[2])
            pteam.append(strings[3])
        else:
            fname.append(strings[0])
            lname.append(strings[1]+' '+strings[2])
            positions.append(strings[3])
            pteam.append(strings[4])
nplayers = len(fname)
players = empty((nplayers,3), dtype = "S30")

for i in range(nplayers):
    players[i,0] = fname[i] + " " + lname[i]
    players[i,1] = positions[i]
    players[i,2] = pteam[i]

#Positional limits, stored as global to make it easy.
sqb = 0
srb = 0
swr = 0
ste = 0
sflex = 0
sdst = 0
sk = 0

def input_int(prompt):
    preresponse = raw_input(prompt)
    try:
        response = int(preresponse)
    except:
        if preresponse == 'quit':
            quit()
        print "Please enter an integer."
        response = input_int(prompt)
    return response

def player_not_found():
    print "That player could not be found.  Make sure you enter his"
    print "first and last name correctly.  For example:"
    print "David Johnson"


def keepers(team_names,teams,round_skip, pteams):
    global players
    for i in range(len(team_names)):
        print "How many keepers for Team %d: %s?" % ( i+1, team_names[i])
        keep = input_int(">")
        for j in range(keep):
            print "Enter the name of keeper #%d." % (j+1)
            player = ''
            while not(player in players):
                player = raw_input(">")
                if not(player in players):
                    player_not_found()
            add_player(player,i,teams)
        print "How many picks will %s lose for keepers, or otherwise?" % team_names[i]
        num = input_int(">")
        if num != 0:
            print "Please enter the round number of each pick lost."
        for j in range(num):
            dround = input_int(">")
            round_skip[i].append(dround)
    print "Are there any other players that you would like to",
    print "remove from the draftable list\n for any reason?"
    response = raw_input("Yes/No: ")
    if (response == "Yes" or response == "yes"):
        print "How many players would you like to remove?"
        num = input_int(">")
        for i in range(num):
            print "Enter the names of the players you would like to remove."
            error = 1
            player = ''
            while not(player in players):
                player = raw_input(">")
                if not(player in players):
                    player_not_found()
            player_spot = argwhere(players == player)
            player_row = player_spot[0]
            players = delete(players, player_row, 0)
    draft(team_names, teams, round_skip, pteams)

def add_player(player_name,team_number,teams):
    global players
    player_spot = argwhere(players == player_name)
    player_row = player_spot[0,0]
    #Find the first empty spot where we can add a player.
    try:
        spot = amax(nonzero(teams[team_number])[0]) + 1
    except:
        spot = 0
    teams[team_number,spot] = players[player_row]
    players = delete(players, player_row, 0)

def player_draft(num_team, teams):
    global players
    print "Here are the top ten players available:\n"
    for i in range(10):
        try:
            print players[i,0], ",",players[i,1], players[i,2]
        except:
            print "End of list."
    print "\nTo draft a player, type his name. To see the next ten available players,"
    print "type 'list'.  Then hit enter to scroll down. When you have finished"
    print "looking, type 'done'."
    print "To see the players available at a given position,"
    print "type 'list' followed by the name of the position."
    print "For example 'list TE' or 'list D/ST'"
    print "To see the players on your team, type 'team'."
    response = raw_input(">")
    if response in players:
        player_spot = argwhere(players == response)
        player_row = player_spot[0,0]
        player = players[player_row]
        add_player(response,num_team,teams)
        return player
    elif response == 'team':
        for player in teams[num_team]:
            print player[0],", ", player[1] , player[2]
        return player_draft(num_team,teams)
    elif response == 'list':
        response = ''
        place = 11
        while response == '':
            for i in range(place,place+10):
                try:
                    print players[i,0], ",", players[i,1], players[i,2]
                except: print "End of list"
            place += 10
            response = raw_input(">")
        return player_draft(num_team,teams)
    elif response == 'list RB':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'RB':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    elif response == 'list WR':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'WR':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    elif response == 'list QB':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'QB':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    elif response == 'list TE':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'TE':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    elif response == 'list K':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'K':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    elif response == 'list D/ST':
        place = 0
        for place in range(len(players)):
            if players[place,1] == 'D/ST':
                print players[place,0], ",", players[place,1], players[place,2]
        response = raw_input("ENTER TO CONTINUE:")
        return player_draft(num_team,teams)
    else:
        player_not_found()
        return player_draft(num_team,teams)


def cpu_draft(num_team, teams,nround, time):
    global players, sqb, srb, swr, sflex, ste, sdst, sk
    nqb = 0
    nrb = 0
    nwr = 0
    nte = 0
    ndst = 0
    nk = 0
    for player in teams[num_team]:
        if player[1] == 'QB':
            nqb += 1
        elif player[1] == 'RB':
            nrb += 1
        elif player[1] == 'WR':
            nwr += 1
        elif player[1] == 'TE':
            nte +=1
        elif player[1] == 'D/ST':
            ndst += 1
        elif player[1]  == 'K':
            nk += 1
    e = 0.
    f = 0.
    g = 0.
    h = 0.
    i = 0.
    j = 0.
    k = 0.
    l = 0.
    m = 0.
    n = 0.
    o = 0.
    p = 0.
    if nround*size(teams,0) <= 12:
        a = 0.5
        b = 0.25
        c = 0.1
        d = 0.0
    elif nround*size(teams,0) <= 20:
        a = 0.7
        b = 0.5
        c = 0.3
        d = 0.2
        e = 0.1
        f = 0.05
        g = 0.
    elif nround*size(teams,0) <= 30:
        a = 0.8
        b = 0.6
        c = 0.4
        d = 0.3
        e = 0.2
        f = 0.1
        g = 0.05
        h = 0.
    elif nround*size(teams,0) <= 40:
        a = 0.8
        b = 0.6
        c = 0.4
        d = 0.3
        e = 0.2
        f = 0.15
        g = 0.1
        h = 0.05
        i = 0.0
    elif nround*size(teams,0) <= 50:
        a = 0.85
        b = 0.70
        c = 0.60
        d = 0.50
        e = 0.4
        f = 0.3
        g = 0.2
        h = 0.15
        i = 0.1
        j = 0.05
        k = 0.0
    elif (nround *size(teams,0)> 5 and nround*size(teams,0) <= 110):
        a = 0.9
        b = 0.8
        c = 0.72
        d = 0.64
        e = 0.56
        f = 0.48
        g = 0.42
        h = 0.34
        i = 0.28
        j = 0.22
        k = 0.16
        l = 0.1
        m = 0.05
        n = 0.0
    else:
        a = 0.92
        b = 0.84
        c = 0.76
        d = 0.68
        e = 0.6
        f = 0.52
        g = 0.44
        h = 0.38
        i = 0.32
        j = 0.26
        k = 0.2
        l = 0.16
        m = 0.12
        n = 0.08
        o = 0.04
        p = 0.0
    draw = random()
    if (ste - nte >= size(teams,1)-nround - sdst + ndst - sk + nk):
        try:
            player_spot = argwhere(players == 'TE')
            player_row = player_spot[0,0]
            player = players[player_row]
            add_player(players[player_row,0],num_team, teams)
            return player
        except:
            pass
    elif (sdst-ndst > 0 and size(teams,1)-nround <=2):
        draft_pos = 'D/ST'
        #try:
        player_spot = argwhere(players == draft_pos)
        player_row = player_spot[0,0]
        player = players[player_row]
        add_player(players[player_row,0],num_team, teams)
        return player
        #except:
        #    pass
    elif (sk-nk > 0 and size(teams,1) - nround <= 2):
        draft_pos = 'K'
        #try:
        player_spot = argwhere(players == draft_pos)
        player_row = player_spot[0,0]
        player = players[player_row]
        add_player(players[player_row,0],num_team, teams)
        return player
        #except:
        #    pass
    try:
        if draw >= a:
            player = players[0]
        elif draw >= b:
            player = players[1]
        elif draw >= c:
            player = players[2]
        elif draw >= d:
            player = players[3]
        elif draw >= e:
            player = players[4]
        elif draw >= f:
            player = players[5]
        elif draw >= g:
            player = players[6]
        elif draw >= h:
            player = players[7]
        elif draw >= i:
            player = players[8]
        elif draw >= j:
            player = players[9]
        elif draw >= k:
            player = players[10]
        elif draw >= l:
            player = players[11]
        elif draw >= m:
            player = players[12]
        elif draw >= n:
            player = players[13]
        elif draw >= o:
            player = players[14]
        elif draw >= p:
            player = players[15]
    except:
        player = players[0]
    position = player[1]
    if time < 2:
        for pos,slot,num in [['QB', sqb, nqb], ['RB',srb+sflex,nrb],['WR', swr+sflex, nwr],
            ['TE', ste+sflex, nte], ['D/ST', sdst, ndst], ['K', sk, nk]]:
            if (position == pos and num >= slot):
                return cpu_draft(num_team, teams, nround, time+1)
    add_player(player[0], num_team, teams)
    return player



def draft(team_names, teams, skips, pteams):
    print "*"*40, "\nLET THE DRAFT BEGIN!\n","*"*40
    for nround in range(1, size(teams,1) + 1):
        print "*"*40, "\nROUND %d\n" % nround, "*"*40
        if (nround % 2 == 1):
            order = range(len(team_names))
        else:
            order = range(len(team_names)-1,-1,-1)
        num_pick = 0
        for j in order:
            num_pick += 1
            if (j in pteams and not(nround in skips[j])):
                print "%s is up to draft." % team_names[j]
                pick = player_draft(j, teams)
                print "With pick number %d in round %d, %s selects %s, %s %s.\n" % (
                    num_pick, nround, team_names[j], pick[0], pick[1], pick[2])
            elif not(nround in skips[j]):
                pick = cpu_draft(j, teams, nround, 0)
                print "With pick number %d in round %d, %s selects %s, %s %s.\n" % (
                    num_pick, nround, team_names[j], pick[0], pick[1], pick[2])
            else:
                print "Team %s is skipped this round as per keeper rules." % team_names[j]

def enter_settings():
    print "How many teams will be in the draft?"
    num_teams = input_int(">")
    print "How many players will there be on each team after the draft?"
    nrounds = input_int(">")
    print "Now we need to input your roster settings."
    print "Type in the number of starters at each position."
    print "Consider superflex to be another QB."
    sqb = input_int("QB: ")
    srb = input_int("RB: ")
    swr = input_int("WR: ")
    ste = input_int("TE: ")
    sflex = input_int("FLEX: ")
    sdst = input_int("D/ST: ")
    sk = input_int("K: ")
    return num_teams, nrounds,sqb, srb, swr, ste, sflex, sdst, sk

def main():
    global sqb,srb,swr,sflex,ste,sdst,sk
    print "*"*40
    print "Hello! Welcome to mock_draft.py!"
    try:
        sf = open('settings.txt','r')
        num_teams = int(sf.readline().split()[1])
        nrounds = int(sf.readline().split()[1])
        dummy = sf.readline()
        sqb = int(sf.readline().split()[1])
        srb = int(sf.readline().split()[1])
        swr = int(sf.readline().split()[1])
        ste = int(sf.readline().split()[1])
        sflex = int(sf.readline().split()[1])
        sdst = int(sf.readline().split()[1])
        sk = int(sf.readline().split()[1])
        sf.close
        print "Roster settings read from settings.txt."
    except:
        num_teams, nrounds, sqb,srb,swr,ste,sflex,sdst,sk = enter_settings()
    round_skip = [[] for i in range(num_teams)]
    teams = zeros((num_teams,nrounds,3), dtype = "S30")
    print "Now we will give every team a name up to 20 characters long."
    team_names = empty(num_teams, dtype = "S20")
    for i in range(1,num_teams+1):
        team_names[i-1] = raw_input("Team %d Name: " % i)
    print "How many teams will you be controlling in the draft?"
    num_control = input_int(">")
    print "Please enter the draft position of the team(s) you will be controlling."
    teams_controlled = []
    for i in range(num_control):
        teams_controlled.append(input_int(">")-1)
    print "Do you want to do any keepers or otherwise remove anyone from the draftable list?"
    response = ''
    while (not(response == "Yes" or response == "No")):
        response = raw_input("Yes/No: ")
    if response == "No":
        draft(team_names,teams,round_skip,teams_controlled)
    else:
        print "Keepers it is then."
        keepers(team_names,teams,round_skip,teams_controlled)
    print "The final teams will be stored in the file results.txt."
    f = open('results.txt','w')
    for i in range(num_teams):
        f.write(team_names[i].ljust(38))
    f.write("\n\n")
    for i in range(nrounds):
        for j in range(num_teams):
            string = teams[j,i,0] + ', ' + teams[j,i,1] + ' ' + teams[j,i,2]
            f.write(string.ljust(38))
        f.write("\n")

main()
