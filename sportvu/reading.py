import numpy as np
import xml.etree.ElementTree as ET
import csv

################################################################################
def get_player_data(files):
        
    playerdata = np.loadtxt('Player_ID.csv',delimiter=',',dtype=str,skiprows=1,unpack=True)
    pd_ids = playerdata[0].astype(int)
    pd_names = playerdata[1]
    playerdata[playerdata==''] = '0.0'
    pd_masses = playerdata[2].astype(float)/2.2
    
    
    homeScore = []
    awayScore = []
  


    sc = []
    
    players = []
    ball = []
    for i in range(0,11):
        players.append([])

    player_ids_home = []
    player_ids_away = []
    ball_ids = []

    homeid = None
    awayid = None
    ballid = -1
    
    print("Getting positions....")
    for k in range(0, len(files)):
        tree = ET.parse(files[k])
        root = tree.getroot()
        sequences = root[0][4][0][11]
        homeScore.append((int)(root[0][4][0][10][4][k].get('score')))
        awayScore.append((int)(root[0][4][0][9][4][k].get('score')))
 

        q = (int)(sequences.get('period'))
        for s in sequences:
            sc.append(s.get('shot-clock'))
            t = float(s.get('game-clock'))
            locs = s.get('locations')
            
            locs = locs.split(';')

            if q == 1:
                t = abs(t - 720.0)
            elif q == 2:
                t = abs(t - 1440.0)
            elif q == 3:
                t = abs(t - 2160.0)
            elif q == 4:
                t = abs(t - 2880.0)
            elif q == 5:
                t = abs(t - 3600.0)

            if len(locs)>10:
                for i in range(0,11):
                
                    vals = locs[i].split(',')

                    if i==1:
                        homeid = int(vals[0])
                    if i==6:
                        awayid = int(vals[0])

                    teamid = int(vals[0])
                    pid = int(vals[1])
                    x = float(vals[2])
                    y = float(vals[3])
                    z = float(vals[4])
                    #m = get_mass(str(pid))
                    
                    
                    m = 0.6237
                    if pid>=0:
                        massindex = pd_ids.tolist().index(pid)
                        if massindex>=0:
                            m = pd_masses[massindex]
                    
                    players[i].append([teamid,pid,x,y,z,t,m])

                    if teamid==homeid:
                        player_ids_home.append(pid)
                    if teamid==awayid:
                        player_ids_away.append(pid)
                    if teamid==ballid:
                        ball_ids.append(pid)
                        
            elif len(locs) == 10 and len(players[0]) > 0:
                #print len(players[0])
                #print len(players[0][len(players[0])-1])
                a = len(players[0]) -1
                                     
                players[0].append([players[0][a][0],players[0][a][1],players[0][a][2],players[0][a][3],players[0][a][4],players[0][a][5],players[0][a][6]])
                                     
                for i in range(0,10):
                    vals = locs[i].split(',')

                    if i==1:
                        homeid = int(vals[0])
                    if i==6:
                        awayid = int(vals[0])

                    teamid = int(vals[0])
                    pid = int(vals[1])
                    x = float(vals[2])
                    y = float(vals[3])
                    z = float(vals[4])
                    #m = get_mass(str(pid))
                    
                    
                    m = 0.6237
                    if pid>=0:
                        massindex = pd_ids.tolist().index(pid)
                        if massindex>=0:
                            m = pd_masses[massindex]
                    
                    players[i+1].append([teamid,pid,x,y,z,t,m])

                    if teamid==homeid:
                        player_ids_home.append(pid)
                    if teamid==awayid:
                        player_ids_away.append(pid)
                    if teamid==ballid:
                        ball_ids.append(pid)
                    
                    

    homeplayers = np.unique(player_ids_home) 
    awayplayers = np.unique(player_ids_away) 
    balls = np.unique(ball_ids)
    hometeam = {}
    awayteam = {}
    ball = {}
    print("Calculating velocities....")
    getVelocity(players)
    print("Calculating energies....")
    appendEnergy(players)
    print("Calculating powers....")
    appendPower(players)
    #get_mass(awayteam)
    #etMass(hometeam)
    print "Initializing keys...."
    
    for h in homeplayers:
        hometeam[str(h)] = {}
        hometeam[str(h)]['x'] = []
        hometeam[str(h)]['y'] = []
        hometeam[str(h)]['z'] = []
        hometeam[str(h)]['t'] = []
        hometeam[str(h)]['v'] = []
        hometeam[str(h)]['ke'] = []
        hometeam[str(h)]['power'] = []
        hometeam[str(h)]['mins'] = 0
        

    for h in awayplayers:
        awayteam[str(h)] = {}
        awayteam[str(h)]['x'] = []
        awayteam[str(h)]['y'] = []
        awayteam[str(h)]['z'] = []
        awayteam[str(h)]['t'] = []
        awayteam[str(h)]['v'] = []
        awayteam[str(h)]['ke'] = []
        awayteam[str(h)]['power'] = []
        awayteam[str(h)]['mins'] = 0
      
    for h in balls:
        ball[str(h)] = {}
        ball[str(h)]['x'] = []
        ball[str(h)]['y'] = []
        ball[str(h)]['z'] = []
        ball[str(h)]['t'] = []
        ball[str(h)]['v'] = []
      
    
    print("Reordering the players in the dictionaries...")
    nplayers = len(players[10])
    for i in range(0,nplayers):
        for p in players:
            #print(p)
            teamid = p[i][0]
            pid = str(p[i][1])
            x = p[i][2]
            y = p[i][3]
            z = p[i][4]
            t = p[i][5]
            v = p[i][7]
            ke = p[i][8]
            power = p[i][9]
            #print(teamid,homeid)
            if teamid==homeid:
                hometeam[pid]['x'].append(x)
                hometeam[pid]['y'].append(y)
                hometeam[pid]['z'].append(z)
                hometeam[pid]['t'].append(t)
                hometeam[pid]['v'].append(v)
                hometeam[pid]['ke'].append(ke)
                hometeam[pid]['power'].append(power)

            elif teamid==awayid:
                awayteam[pid]['x'].append(x)
                awayteam[pid]['y'].append(y)
                awayteam[pid]['z'].append(z)
                awayteam[pid]['t'].append(t)
                awayteam[pid]['v'].append(v)
                awayteam[pid]['ke'].append(ke)
                awayteam[pid]['power'].append(power)
            elif teamid==ballid:
                ball[pid]['x'].append(x)
                ball[pid]['y'].append(y)
                ball[pid]['z'].append(z)
                ball[pid]['t'].append(t)
                ball[pid]['v'].append(v)
                
    sc = shots(sc)
    
    getMinsPlayed(awayteam, awayplayers)
    getMinsPlayed(hometeam, homeplayers)
    
    return players,homeplayers,awayplayers,hometeam,awayteam,ball, homeScore, awayScore, sc

    return player_data
################################################################################

######## HELPER FUNCTIONS TO READ IN DATA ########################################
def getMinsPlayed(team, players):
    for p in players:
        count = 0
        for i in range(0,len(team['%s' %p]['t'])-1):
            if team['%s' %p]['t'][i] != team['%s' %p]['t'][i+1]:
                count += 1.
        team['%s' %p]['mins'] = count/25./60
        
def shots(shotclock):
    shotTimes = []
    a = '24.00'
    for i in range(0, len(shotclock)-1):
        if shotclock[i] != a and shotclock[i+1] == a:
                #numShots += 1
                r = shotclock[i]
                if len(r) > 1:
                    b = (float)(r)
                    shotTimes.append((float)(b))
                else:
                    shotTimes.append(0.0)
        else:
            shotTimes.append(-1)
    return shotTimes

################################################################################

################################################################################
def get_sportvu_data(filename):

    return game_data
################################################################################
