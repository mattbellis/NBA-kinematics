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
    homeplayers = {}
    awayplayers = {}
    ball = []

    for i in range(0,11):
        players.append([])

    player_ids_home = []
    player_ids_away = []
    ball_ids = []

    homeids = []
    awayids = []

    homeid = None
    awayid = None
    ballid = -1
    
    print("Getting positions....")
    for k in range(0, len(files)):
        print("Getting data from %s" % (files[k]))
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
                    pid = str(vals[1])
                    x = float(vals[2])
                    y = float(vals[3])
                    z = float(vals[4])
                    #m = get_mass(str(pid))
                    
                    
                    '''
                    m = 0.6237
                    if int(pid)>=0:
                        massindex = pd_ids.tolist().index(pid)
                        if massindex>=0:
                            m = pd_masses[massindex]
                    '''
                    
                    players[i].append([teamid,pid,x,y,z,t])

                    if teamid==homeid:
                        player_ids_home.append(pid)
                    if teamid==awayid:
                        player_ids_away.append(pid)
                    if teamid==ballid:
                        ball_ids.append(pid)

                    if i>=1 and i<6:
                        homeids.append(pid)
                        keys = homeplayers.keys()
                        if pid in keys:
                            homeplayers[pid].append([teamid,pid,x,y,z,t])
                        else:
                            homeplayers[pid] = []
                            homeplayers[pid].append([teamid,pid,x,y,z,t])
                    elif i>=6:
                        awayids.append(pid)
                        keys = awayplayers.keys()
                        if pid in keys:
                            awayplayers[pid].append([teamid,pid,x,y,z,t])
                        else:
                            awayplayers[pid] = []
                            awayplayers[pid].append([teamid,pid,x,y,z,t])

            '''
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
                    
            '''

                    
    print("Read in data and reordering the players...")
    for i,player in enumerate(players):
        #player = players[key]
        temp = np.array(player)
        temp = temp.transpose()
        tempplayer = {}
        tempplayer['x'] = np.array(temp[2]).astype(float)
        tempplayer['y'] = np.array(temp[3]).astype(float)
        tempplayer['z'] = np.array(temp[4]).astype(float)
        tempplayer['t'] = np.array(temp[5]).astype(float)
        #tempplayer['gameTime'] = np.array(temp[5]).astype(float)
        players[i] = tempplayer

    alltimes = players[0]['t']
    #print(len(alltimes))
    alltimes = alltimes[alltimes>=0]
    #print(len(alltimes))
    alltimes = np.unique(alltimes)

    print("Reordering the hometeam players...")
    for key in homeplayers.keys():
        player = homeplayers[key]
        temp = np.array(player)
        temp = temp.transpose()
        tempplayer = {}
        x = np.array(temp[2]).astype(float)
        y = np.array(temp[3]).astype(float)
        z = np.array(temp[4]).astype(float)
        tempplayer['t'] = np.array(temp[5]).astype(float)
        tempplayer['gameTime'] = alltimes
        homeplayers[key] = tempplayer

        tempplayer['x'] = np.zeros(len(alltimes))
        tempplayer['y'] = np.zeros(len(alltimes))
        tempplayer['z'] = np.zeros(len(alltimes))

        tcount = 0
        ptimes = tempplayer['t']
        maxtcount = len(ptimes)
        #print(maxtcount,len(alltimes))
        for i,t in enumerate(alltimes):
            found_one = False
            while tcount < maxtcount and found_one is False:
                #print(i,t,tcount,ptimes[tcount],abs(ptimes[tcount]-t))
                if abs(ptimes[tcount]-t)<0.03: # The 0.03 is because of some funky 0.01 times. Weird. 
                    xi,yi,zi = x[tcount],y[tcount],z[tcount]
                    tempplayer['x'][i] = xi
                    tempplayer['y'][i] = yi
                    tempplayer['z'][i] = zi
                    found_one = True # If we found one, we don't need to go further
                    tcount -= 1
                elif ptimes[tcount]-t>0.1:
                    break # Too far. 
                tcount += 1
            
        tempplayer['t'] = tempplayer['gameTime'] 

    print("Reordering the awayteam players...")
    for key in awayplayers.keys():
        player = awayplayers[key]
        temp = np.array(player)
        temp = temp.transpose()
        tempplayer = {}
        x = np.array(temp[2]).astype(float)
        y = np.array(temp[3]).astype(float)
        z = np.array(temp[4]).astype(float)
        tempplayer['t'] = np.array(temp[5]).astype(float)
        tempplayer['gameTime'] = alltimes
        awayplayers[key] = tempplayer

        tempplayer['x'] = np.zeros(len(alltimes))
        tempplayer['y'] = np.zeros(len(alltimes))
        tempplayer['z'] = np.zeros(len(alltimes))

        tcount = 0
        ptimes = tempplayer['t']
        maxtcount = len(ptimes)
        #print(maxtcount,len(alltimes))
        for i,t in enumerate(alltimes):
            found_one = False
            while tcount < maxtcount and found_one is False:
                #print(i,t,tcount,ptimes[tcount],abs(ptimes[tcount]-t))
                if abs(ptimes[tcount]-t)<0.03: # The 0.03 is because of some funky 0.01 times. Weird. 
                    xi,yi,zi = x[tcount],y[tcount],z[tcount]
                    tempplayer['x'][i] = xi
                    tempplayer['y'][i] = yi
                    tempplayer['z'][i] = zi
                    found_one = True # If we found one, we don't need to go further
                    tcount -= 1
                elif ptimes[tcount]-t>0.1:
                    break # Too far. 
                tcount += 1
            
        tempplayer['t'] = tempplayer['gameTime'] 


    hometeam = homeplayers
    awayteam = awayplayers
    #homeplayers = np.unique(player_ids_home) 
    #awayplayers = np.unique(player_ids_away) 
    balls = np.unique(ball_ids)
    #hometeam = {}
    #awayteam = {}
    ball = {}
    '''
    print("Calculating velocities....")
    getVelocity(players)
    print("Calculating energies....")
    appendKineticEnergy(players)
    print("Calculating powers....")
    #print len(players[0][0])
    getPower(players)
    #get_mass(awayteam)
    #etMass(hometeam)
    '''
    print("Initializing keys....")
    
    '''
    for h in homeplayers:
        hometeam[str(h)] = {}
        hometeam[str(h)]['x'] = []
        hometeam[str(h)]['y'] = []
        hometeam[str(h)]['z'] = []
        hometeam[str(h)]['gameTime'] = []
        #hometeam[str(h)]['v'] = []
        
        #hometeam[str(h)]['veloTime'] = []
        
        hometeam[str(h)]['m'] = []

        #hometeam[str(h)]['ke'] = []
        #hometeam[str(h)]['power'] = []
        hometeam[str(h)]['mins'] = 0
        #hometeam[str(h)]['powerTime'] = []
        

    for h in awayplayers:
        awayteam[str(h)] = {}
        awayteam[str(h)]['x'] = []
        awayteam[str(h)]['y'] = []
        awayteam[str(h)]['z'] = []
        awayteam[str(h)]['gameTime'] = []
        #awayteam[str(h)]['v'] = []

        #awayteam[str(h)]['veloTime'] = []
        
        awayteam[str(h)]['m'] = []

        
        #awayteam[str(h)]['ke'] = []
        #awayteam[str(h)]['power'] = []
        awayteam[str(h)]['mins'] = 0
        #awayteam[str(h)]['powerTime'] = []
    '''

      
    for h in balls:
        ball[str(h)] = {}
        ball[str(h)]['x'] = []
        ball[str(h)]['y'] = []
        ball[str(h)]['z'] = []
        ball[str(h)]['t'] = []
        ball[str(h)]['v'] = []

        ball[str(h)]['m'] = []

    
    '''
    print("Reordering the players in the dictionaries...")
    nsnapshots = len(players[10])
    for i in range(0,nsnapshots):
        #print(i,nsnapshots)
        for p in players:
            #print(p)
            teamid = p[i][0]
            pid = str(p[i][1])
            x = p[i][2]
            y = p[i][3]
            z = p[i][4]
            gt = p[i][5]
            #v = p[i][7]
            m = p[i][6]
            #vt = p[i][8]
            #ke = p[i][9]
            #power = p[i][10]
            #powerTime = p[i][11]
            #print(teamid,homeid)
            if teamid==homeid:
                hometeam[pid]['x'].append(x)
                hometeam[pid]['y'].append(y)
                hometeam[pid]['z'].append(z)
                hometeam[pid]['m'].append(m)
                hometeam[pid]['gameTime'].append(gt)
                #hometeam[pid]['v'].append(v)
                #hometeam[pid]['veloTime'].append(vt)
                #hometeam[pid]['ke'].append(ke)
                #hometeam[pid]['power'].append(power)
                #hometeam[pid]['powerTime'].append(powerTime)

            elif teamid==awayid:
                awayteam[pid]['x'].append(x)
                awayteam[pid]['y'].append(y)
                awayteam[pid]['z'].append(z)
                awayteam[pid]['m'].append(m)
                awayteam[pid]['gameTime'].append(gt)
                #awayteam[pid]['v'].append(v)
                #awayteam[pid]['veloTime'].append(vt)
                #awayteam[pid]['ke'].append(ke)
                #awayteam[pid]['power'].append(power)
                #awayteam[pid]['powerTime'].append(powerTime)
            
            elif teamid==ballid:
                ball[pid]['x'].append(x)
                ball[pid]['y'].append(y)
                ball[pid]['z'].append(z)
                ball[pid]['t'].append(gt)
                #ball[pid]['v'].append(v)
                ball[pid]['m'].append(m)
    '''
                
    for team in [hometeam, awayteam]:
        for key in team.keys():

            player = team[key]

            #player['x'] = np.array(player['x'])
            #player['y'] = np.array(player['y'])
            #player['z'] = np.array(player['z'])
            #player['gameTime'] = np.array(player['gameTime'])

            x,y,z,t = player['x'],player['y'],player['x'],player['gameTime']
            v,veloTime,dt = getVelocity(x,y,z,t)
            player['v'] = v
            player['veloTime'] = veloTime
            player['dt'] = dt

            # Frames are 25 times second
            # We need to make sure we don't count the times when the game clock is stopped.
            count = 0
            timesteps = t
            nsteps = len(timesteps)
            #print(nsteps)
            for istep in range(nsteps-1):
                if t[istep] < t[istep+1]:
                    count += 1
            player['mins'] = count/25./60

        addPlayerNamesAndMasses(team)

                
    sc = shots(sc)
    
    #getMinsPlayed(awayteam, awayplayers)
    #getMinsPlayed(hometeam, homeplayers)

    #print("ALMOST AT END")

    #'''
    entries = [ players,homeplayers,awayplayers,hometeam,awayteam,ball, homeScore, awayScore, sc]
    for entry in entries:
        #print(type(entry))
        if type(entry) is dict:
            #print("FOUND DICT")
            for key in entry.keys():
                #print("\t",type(entry[key]))
                if type(entry[key]) is dict:
                    #print("FOUND ANOTHER DICT")
                    for key2 in entry[key].keys():
                        if type(entry[key][key2]) is list:
                            #print("HERE: ",key,key2)
                            entry[key][key2] = np.array(entry[key][key2])
    #'''
    
    return players,homeplayers,awayplayers,hometeam,awayteam,ball, homeScore, awayScore, sc

    #return player_data
################################################################################

######## HELPER FUNCTIONS TO READ IN DATA ########################################
def getMinsPlayed(team, players):
    for p in players:
        count = 0
        for i in range(0,len(team['%s' %p]['gameTime'])-1):
            if team['%s' %p]['gameTime'][i] != team['%s' %p]['gameTime'][i+1]:
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
    shotTimes = np.array(shotTimes)
    return shotTimes

def distanceTraveled(x,y,z):
    d = []
    for i in range(len(x)-1):
        d.append(np.sqrt((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2 + (z[i+1]-z[i])**2) * .3048)
    d.append(np.sqrt((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2 + (z[i+1]-z[i])**2) * .3048)
    d = np.array(d)
    return d

####
# this function returns a list of velocities, along with a list of times that map up exactly to the velocity
####
def velocity(d,t):
    v = []
    time = []
    for i in range(1, len(d)-1):
        if abs(((float)(t[i+1])-(float)(t[i-1]))) > .01 and abs(((float)(t[i+1])-(float)(t[i-1]))) < .09:
            v.append(abs(((float)(d[i+1])-(float)(d[i-1])/((float)(t[i+1])-(float)(t[i-1])))))
            time.append(t[i])
        else:
            ### means timeout or not in game
            v.append(-1)
            time.append(-1)
            
        

        ####### accounts for outlying points ############
    for j in range(0,len(v)):
        if v[j] > 10:
                v[j] = v[j-1]

    v = np.array(v)
    time = np.array(time)

    return v,time

################################################################################
def getVelocity(x,y,z,t):

    index = t>0
    x = x[index]
    y = y[index]
    z = z[index]
    t = t[index]

    dx = np.zeros(len(x))
    dy = np.zeros(len(x))
    dz = np.zeros(len(x))
    dt = np.zeros(len(x))
    d = np.zeros(len(x))
    v = -1*np.ones(len(x))
    veloTime = t.copy()

    # Do all the *middle* ones
    dx[1:-1] = (x[2:] - x[0:-2])
    dy[1:-1] = (y[2:] - y[0:-2])
    dz[1:-1] = (z[2:] - z[0:-2])
    dt[1:-1] = (t[2:] - t[0:-2])

    #v[1:-1] = (x[2:] - x[0:-2])/(t[2:] - t[0:-2])

    # Do the first point
    dx[0] = (x[1] - x[0])
    dy[0] = (y[1] - y[0])
    dz[0] = (z[1] - z[0])
    dt[0] = (t[1] - t[0])

    # Do the last point
    #v[-1] = (x[-1] - x[-2])/(t[-1] - t[-2])
    dx[-1] = (x[-1] - x[-2])
    dy[-1] = (y[-1] - y[-2])
    dz[-1] = (z[-1] - z[-2])
    dt[-1] = (t[-1] - t[-2])

    d = np.sqrt(dx*dx + dy*dy + dz*dz)
    # coordinates were in feet so convert to meters
    d /= 3.28084
    v = d/dt

    # Some weird hiccups with the time. Either timeouts or on/off the court. 
    v[dt<0.01] = -1
    v[dt>0.09] = -1

    # Get rid of super-high speeds
    v[v>10] = -1

    index = v>=0
    v = v[index]
    veloTime = veloTime[index]
    dt = dt[index]

    return v,veloTime,dt

################################################################################


        
        
        
def getKineticEnergy(p):
    v = []
    m = []
    for k in range(0, len(p)):
        v.append(p[k][7])
        m.append(p[k][6])
    ke = []
    for i in range(0,len(v)):
        if v[i] != -1:
            ke.append(0.5 * m[i] * v[i]**2)
        else:
            ke.append(-1)
            
    ke = np.array(ke)
    return ke

def appendKineticEnergy(players):
    
    for p in players:
        

        ke = getKineticEnergy(p)
        for k in range(0, len(p)):
            p[k].append(ke[k])
    

    
def getPower(players):
    
    for p in players:
        power = []
        pt = []
        for i in range(0, len(p)-1):
            ke1 = p[i][9]
            ke2 = p[i+1][9]
            t1 = p[i][8]
            t2 = p[i+1][8]
            if( ke1 != -1 and ke2 != 1):
                power.append(abs(ke1 - ke2) / 2.0)
                pt.append((t2-t1)/2.0)
            else:
                power.append(-1)
                pt.append(-1)
        power.append(-1)
        pt.append(-1)
                
                
        for k in range(0, len(p)):

            p[k].append(power[k])
            p[k].append(pt[k])
                
    
################################################################################
def addPlayerNamesAndMasses(team):

    data = np.loadtxt('Player_ID.csv',skiprows=1,delimiter=',',unpack=True,dtype=bytes)
    ids = data[0].astype(str)
    names = data[1].astype(str)
    masses = data[2].astype(str)

    for k in team.keys():
        index = ids.tolist().index(str(k))
        team[k]["name"] = names[index]
        #print("masses: ",masses[index],type(masses[index]),names[index])
        if masses[index].isnumeric():
            team[k]["mass"] = 0.453592*float(masses[index])
        

