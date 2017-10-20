import numpy as np
import matplotlib.pylab as plt
import xml.etree.ElementTree as ET
import csv


#import matplotlib as mpl
#from mpl_toolkits.mplot3d import Axes3D

def get_data(files):
    
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
    
    for k in range(0, len(files)):
        tree = ET.parse(files[k])
        root = tree.getroot()
        sequences = root[0][4][0][11]

        # Make a list to hold all the players 

        q = (int)(sequences.get('period'))
        for s in sequences:
            t = float(s.get('game-clock'))
            locs = s.get('locations')

            locs = locs.split(';')

            if q == 1:
                t = abs(t - 720.0)
            elif q == 2:
                t = abs(t - 1440.0)
            elif q == 3:
                t = abs(t - 1440.0 - 720.0)
            elif q == 4:
                t = abs(t - 1440.0 - 1440.0)


            for i in range(0,11):
                if len(locs)>10:
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

                    players[i].append([teamid,pid,x,y,z,t])

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
    
    for h in homeplayers:
        hometeam[str(h)] = {}
        hometeam[str(h)]['x'] = []
        hometeam[str(h)]['y'] = []
        hometeam[str(h)]['z'] = []
        hometeam[str(h)]['t'] = []
        hometeam[str(h)]['v'] = []
        hometeam[str(h)]['ke'] = []
        

    for h in awayplayers:
        awayteam[str(h)] = {}
        awayteam[str(h)]['x'] = []
        awayteam[str(h)]['y'] = []
        awayteam[str(h)]['z'] = []
        awayteam[str(h)]['t'] = []
        awayteam[str(h)]['v'] = []
        awayteam[str(h)]['ke'] = []
        
    for h in balls:
        ball[str(h)] = {}
        ball[str(h)]['x'] = []
        ball[str(h)]['y'] = []
        ball[str(h)]['z'] = []
        ball[str(h)]['t'] = []
        
        
   
        
    
      

   # print(hometeam)
   # print(awayteam)
   # print(len(players))
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
            #print(teamid,homeid)
            
            
            
            if teamid==homeid:
                hometeam[pid]['x'].append(x)
                hometeam[pid]['y'].append(y)
                hometeam[pid]['z'].append(z)
                hometeam[pid]['t'].append(t)
            elif teamid==awayid:
                awayteam[pid]['x'].append(x)
                awayteam[pid]['y'].append(y)
                awayteam[pid]['z'].append(z)
                awayteam[pid]['t'].append(t)
            elif teamid==ballid:
                ball[pid]['x'].append(x)
                ball[pid]['y'].append(y)
                ball[pid]['z'].append(z)
                ball[pid]['t'].append(t)

    
       
    
    
    return players,homeplayers,awayplayers,hometeam,awayteam,ball




####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

def xy_position(list_of_players):
    
    player_dict = {}
    
    
    for h in range(0,len(list_of_players)):
        player_dict[str(h)] = {}
        player_dict[str(h)]['x'] = []
        player_dict[str(h)]['y'] = []

    nplayers = len(list_of_players[10])
    for i in range(0,nplayers):
        for g in range(0,11):
            p = str(g)
            x = p[i][2]
            y = p[i][3]
            
            player_dict[str(i)]['x'] = []
            player_dict[str(i)]['y'] = []
    
    return player_dict








def get_string(ID_number):
    infile = open('Player_ID.csv','r')
    rows = csv.reader(infile,delimiter=',')
    
    
    for row in rows:
        if ID_number == row[0]:
            return row[1]
        



def get_mass(team):
    
    for key in list(team.keys()):
        

        infile = open('Player_ID.csv','r')
        rows = csv.reader(infile,delimiter=',')


        for row in rows:

            if key == row[0]:

                    team['%s' %(key)]['m'] = (int(row[2])/2.2)


















def distance(x,y,z):
    ### x,y,z are all lists ###
    holder = []
    for i in range(0,len(x)):
        if i>0:
            dist = np.sqrt((x[i]-x[i-1])**2 + (y[i]-y[i-1])**2 + (z[i]-z[i-1])**2)
            dist_meters = dist * 0.3048
            holder.append(dist_meters)
        
    holder.append(holder[-1])

    return holder


def plot_position(team):
    plt.figure(figsize = (9,4))
    
    for key in list(team.keys()):
        
        x = team['%s' % (key)]['x']
        y = team['%s' % (key)]['y']
        
        plt.plot(x,y,linewidth = 0.5)
        
#def velocity(d,t):
 #   v = []
  #  holder = []
   # for i in range(0, len(d)-2):
    #    if abs(((float)(t[i+2])-(float)(t[i]))) > .01 and abs(((float)(t[i+2])-(float)(t[i]))) < .09:
     #       v.append(abs(((float)(d[i+2])-(float)(d[i])/((float)(t[i+2])-(float)(t[i])))))
      #  else:
       #     v.append(0)

    #if len(v) != len(t):
     #   del t[0]
      #  del t[len(t)-1]
####### accounts for outlying points, v > 32 fps ( 22 mph) ############
   # for j in range(0,len(v)):
    #    if v[j] > 10:
     #           v[j] = v[j-1]

   # return v
        
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

    return v    
    
    
    
def getVelo(team, players):
    for p in players:
        d = distance(team['%s' %p]['x'],team['%s' %p]['y'], team['%s' %p]['z'])
        vel = velocity(d, team['%s' %p]['t'])
        team['%s' %p]['v'] = vel
        
def plot_velo(team):
    plt.figure(figsize = (9,4))
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    for key in list(team.keys()):
        
        
        t = team['%s' % (key)]['t']
        v = team['%s' % (key)]['v']
        
        indexer = 0
        
        if len(v) >= len(t):
            
            indexer = len(t)
            
        elif len(t) > len(v):
            
            indexer = len(v)
        
        x = t[0:indexer]
        y = v[0:indexer]
        
        plt.plot(x,y, label = get_string('%s' % (key)), linewidth = 0.5)
        
        plt.legend()
    

def plot_velo_individuals(team):
    
    for key in list(team.keys()):
        plt.figure(figsize = (9,4))
        plt.xlabel('Time (s)')
        plt.ylabel('Speed (m/s)')
        
        t = team['%s' % (key)]['t']
        v = team['%s' % (key)]['v']
        
        indexer = 0
        
        if len(v) >= len(t):
            
            indexer = len(t)
            
        elif len(t) > len(v):
            
            indexer = len(v)
        
        x = t[0:indexer]
        
        y = v[0:indexer]
        
        plt.plot(x,y, label = get_string('%s' % (key)), linewidth = 0.5)
        
        plt.legend()
    
   
    
    
def get_distance(team, players):
    
    for p in players:
        
        x = team['%s' %p]['x']
        y = team['%s' %p]['y']
        z = team['%s' %p]['z']
        
        d = distance(x,y,z)
        
        team['%s' %p]['d'] = d
        
        
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################


        
        
def kinetic_energy(vel,mass):
    holder = []
    for i in range(0,len(vel)):
        k = (1./2)*(mass)*(vel[i])**2
        
        holder.append(k)
    return holder



def power(velocity,mass): # when entering mass and velocity, make sure player numbers match up!
    holder = []
    k_instantaneous = []
    ticks = 0
    for i in range(0,len(velocity)):
        
        holder.append( 0.5 * mass * velocity[i]**2 )
        ticks += 1
        if ticks == 1500:   # the product of 25 times 60 (or 1 minute)
            x = float(sum(holder)/len(holder))
            k_instantaneous.append(x*25.)
            
            
            holder = []
            ticks = 0
        
    return k_instantaneous

def get_power(team,players):
    for p in players:
        
        
        vel = team['%s' %p]['v']
        mass = team['%s' %p]['m']
        
        
        powerr = power(vel,mass)
        
        team['%s' %p]['P'] = powerr
        
def plot_power(team):
    
    plt.figure(figsize = (9,4))
    
    plt.xlabel('Power (Watts)')
    
    plt.title('Power Output per Minute')
    
    
    data = []
    
    labels = []
    
    for key in list(team.keys()):
        
        
        data.append(team['%s' % (key)]['P'])
        
        labels.append(get_string('%s' %key))
        
        
    
    
    plt.boxplot(data,labels=labels,vert = False)
    
    
def plot_power_single(team_key):
    plt.figure(figsize = (9,4))
    
    plt.xlabel('Power (Watts)')
    
    plt.title('Power Output per Minute')
    
    
    data = []
    
    labels = []
    
    
        
        
    data.append(team_key['P'])

    labels.append(get_string('%s' %team_key))
        
        
    
    
    plt.boxplot(data,labels=labels,vert = False)    
        
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

def tenth_place(listt):
    holder = []           
                
    for i in range(0,len(listt)):
        x = listt[i]
        y = "%.1f" % (x)
        z = float(y)
        
        holder.append(z)
        
    return holder
        
def tenth_non_list(number): # Only used for time
    x = number
    y = "%.1f" % (x/60.)
    z = float(y)
    
    return z





        
        
def shooting_stats(ball):
    
    bx2 = tenth_place(ball['-1']['x'])
    by2 = tenth_place(ball['-1']['y'])
    bz2 = tenth_place(ball['-1']['z'])

    ##### These points will be used in order to test if the shot went in the hoop ######


    hoop_x = np.linspace(4,6.5,26)
    hoop_x2 = np.linspace(87.5,90,26)

    hoop_y = np.linspace(24.2,25.8, 17)
    hoop_z = np.linspace(8.0,9.3,14)


    ###### The hoop points represent points within the hoop below the rim that are still in the net ########
    ### We test below the rim to ensure rimmed out shots aren't included ###






    q2 = 0
    q3 = 0
    q4 = 0

    for i in range(0,len(ball['-1']['t'])):
        if ball['-1']['t'][i] == 12:
            q2 = i
            break

    for i in range(q2, len(ball['-1']['t'])):
        if ball['-1']['t'][i] == 24:
            q3 = i
            break

    for i in range(q3, len(ball['-1']['t'])):
        if ball['-1']['t'][i] == 36:
            q4 = i 
            break


    
    
    
    
    
    
    
    
    counter = 0
    away_shots = 0
    home_shots = 0
    easy_time = []
    holder = []
    shot_time = []
    for i in range(0,len(bx2)):

        tenth_time = tenth_non_list(ball['-1']['t'][i])

        easy_time.append(tenth_time)


        #print easy_time[i]

        if bx2[i] in hoop_x and by2[i] in hoop_y and bz2[i] in hoop_z: ## Tests to see if ball is in net ##

            if easy_time[i] not in holder:

                holder.append(easy_time[i])

                counter += 1

                shot_time.append(i)

                if i < q3:

                    home_shots += 1

                else: 

                    away_shots += 1




        elif bx2[i] in hoop_x2 and by2[i] in hoop_y and bz2[i] in hoop_z:

             if easy_time[i] not in holder:

                holder.append(easy_time[i])

                counter += 1

                shot_time.append(i)

                if i < q3:

                    away_shots += 1

                else: 

                    home_shots += 1






    print("%d shots were calculated to be made in this game." % counter)


    print("The home team made %d shots." % home_shots)

    print("The away team made %d shots." % away_shots)
    
    
    
def series_power(ht, key):
    



    power = {}
    
    
    power[key] = []






    for team in ht:
        
        
        
        
        if key in team:
           
            holder = []
            ticks = 0
            longer_holder = []

            for j in range(0,len(team[key]['power'])):

                if ticks == 1500:
                    avg_power = float(sum(holder))*1./len(holder)
                    longer_holder.append(avg_power)
                    ticks = 0
                    holder = []

                elif team[key]['power'] != 0:

                    holder.append(team[key]['power'][j])

                    ticks += 1











            power[key].append(longer_holder)

        
    return power

def plot_series_power(team,ID):
    
    data = series_power(team,str(ID))
    boxplotdata = data[str(ID)]
                        
                        
    plt.figure()

    plt.boxplot(boxplotdata ,vert = False)
    plt.title(get_string(str(ID)))



    
    
    
def get_player_IDs_series(team_series):
    
    Keyz = []
    
    for team in team_series:
        
        for key in list(team.keys()):
            
            Keyz.append(key)

     
    Keyz = np.unique(Keyz)
    
    return Keyz





def series_power(ht, key):
    



    power = {}
    
    
    power[key] = []






    for team in ht:
        
        
        
        
        if key in team:
           
            holder = []
            ticks = 0
            longer_holder = []

            for j in range(0,len(team[key]['power'])):

                if ticks == 1500:
                    avg_power = float(sum(holder))*1./len(holder)
                    longer_holder.append(avg_power)
                    ticks = 0
                    holder = []

                elif team[key]['power'] != 0:

                    holder.append(team[key]['power'][j])

                    ticks += 1











            power[key].append(longer_holder)

        
    return power


def plot_team_series_power(team_series):
    
    _IDs = get_player_IDs_series(team_series)


    for ID in _IDs:

        plot_series_power(team_series,ID)
        
        
        
def get_full_score(scores):
    
    hold = []

    for score in scores:
        holder = []
        for s in score:
            s = int(s)
            holder.append(s)
        hold.append(sum(holder))
        
    
    return hold



def get_wins(hsg,asg):
    
    home_record = []
    away_record = []
    
    for i in range(0,len(asg)):
        if hsg[i] > asg[i]:
            home_record.append('W')
            away_record.append('L')
        else:
            home_record.append('L')
            away_record.append('W')
                               
                               
    return home_record, away_record


def plot_power_win_loss(team_rec,team,ID):
    winning_power = []
    winning_index = []
    
    losing_power = []
    losing_index = []

    



    for i in range(0,len(team_rec)):
        if team_rec[i] == 'W' and str(ID) in team[i]:
            winning_power.append(team[i][str(ID)]['power'])
            winning_index.append(i)
        elif str(ID) in team[i]:
            losing_power.append(team[i][str(ID)]['power'])
            losing_index.append(i)
            
    wht = []
    lht = []
    for index in winning_index:
        wht.append(team[index]) 
            
    for index in losing_index:
        lht.append(team[index])
    
    
    plot_series_power(wht,ID)
    plot_series_power(lht,ID)
    

    
def percentage(velocity):
    
    ###################
    
    on_bench = 0
    percent_over_0 = 0
    percent_over_0_5 = 0
    percent_over_1_0 = 0
    percent_over_1_0 = 0
    percent_over_1_5 = 0 
    percent_over_2_0 = 0
    percent_over_2_5 = 0
    percent_over_3_0 = 0
    percent_over_3_5 = 0
    percent_over_4_0 = 0
    ##############################
    for i in range(0,len(velocity)):
        
        if velocity[i]>=4.0:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1
            percent_over_2_0 += 1
            percent_over_2_5 += 1
            percent_over_3_0 += 1
            percent_over_3_5 += 1
            percent_over_4_0 += 1
        
        elif velocity[i]>= 3.5:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1
            percent_over_2_0 += 1
            percent_over_2_5 += 1
            percent_over_3_0 += 1
            percent_over_3_5 += 1
            percent_over_4_0 += 1
            percent_over_3_5 += 1
            
        
        elif velocity[i]>= 3.0:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1
            percent_over_2_0 += 1
            percent_over_2_5 += 1            
            percent_over_3_0 += 1
        
        
        
        elif velocity[i]>= 2.5:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1
            percent_over_2_0 += 1
            percent_over_2_5 += 1
            
            
        elif velocity[i]>= 2.0:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1
            percent_over_2_0 += 1
            
            
        
        elif velocity[i]>= 1.5:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            percent_over_1_5 += 1 
            

        elif velocity[i]>= 1.0:
            percent_over_0 += 1
            percent_over_0_5 += 1
            percent_over_1_0 += 1
            
            
        elif velocity[i]>= 0.5:
            percent_over_0_5 += 1
            percent_over_0 += 1
        
        elif velocity[i]>= 0.1:
            percent_over_0 += 1
        else:
            on_bench += 1
            
        ########################################  
        
    x = len(velocity) - on_bench
    if x == 0:
        return 0
    zero = 1.0 * (float)(percent_over_0)/x     
    zero_five = 1.0*(float)(percent_over_0_5)/x
    
    one = 1.0*(float)(percent_over_1_0)/x
    one_five = 1.0*(float)(percent_over_1_5)/x
    
    two = 1.0*(float)(percent_over_2_0)/x
    two_five = 1.0*(float)(percent_over_2_5)/x
    
    three = 1.0*(float)(percent_over_3_0)/x
    three_five = 1.0*(float)(percent_over_3_5)/x
    
    four = 1.0*(float)(percent_over_4_0)/(x)
    

    return zero, zero_five, one, one_five, two, two_five, three, three_five, four



def plot_velo_series(team, player_id):
    
    plt.figure(figsize = (9,4))
    
    plt.xlabel('Velocity')
    
    plt.title('%s' % get_string(str(player_id)))
    
    plt.ylabel('Game')
    
    data = []
    
    labels = []
    
    for game in team:
        
        
        data.append(game['%s' % (str(player_id))]['v'])
        
        labels.append(get_string('%s' % str(team.index(game))))
        
        
    
    
    plt.boxplot(data,labels=labels,vert = False)
    
######################
######################
######################
    
    
def series_velo_all_points(teams,key):
    
    plt.figure(figsize = (8,6))
    
    for team in teams:




        t = team['%s' % str(key)]['t']
        v = team['%s' % str(key)]['v']

        indexer = 0

        if len(v) >= len(t):

            indexer = len(t)

        elif len(t) > len(v):

            indexer = len(v)

        x = t[0:indexer]
        y = v[0:indexer]

        plt.plot(x,y, label = 'Game %d' % (teams.index(team)+1), linewidth = 0.5)
        plt.xlabel('Time (s)')
        
        plt.ylabel('Velocity (m/s)')
        
        plt.title('%s' % get_string(str(key)))
        
        plt.legend()
        
        
        
def series_velo(teams, key):
    
    
    
    
    plt.figure(figsize = (8,6))

    plt.xlabel('Time (s)')

    plt.ylabel('Speed (m/s)')

    plt.title('%s' % get_string('%s' % key))
    
    
    
    for team in teams:
        
        if str(key) in list(team.keys()):



            t = teams.index(team) + 1
            v = float(sum(team['%s' % key]['v']))/len(team['%s' % key]['v'])
            
            v_holder = []

            for v in team['%s' % key]['v']:
                if v == (-1):

                    v_holder.append(v)

            v = team['%s' % key]['v']
            v_graph = (sum(v) + len(v_holder))/(len(v)-len(v_holder)) 
            
            '''
            
            The above line takes the average of point in which the player IS MOVING,
            not just on the bench.  Since each point at which the player is on the 
            bench = -1 (m/s), by adding -1*n_{points of time on the bench} to the 
            sum of list 'v', we get the real sum.  The length is then equal to the 
            length of v - n_{points of time on the bench}.
            
            '''

            plt.plot(t,v_graph, 'o', label = 'Game %d' % (teams.index(team)+1), linewidth = 0.5)

            plt.legend()
            
            
def series_velo_percentage(team,key):
    

    plt.figure(figsize=(8,6))
    x = np.linspace(0, 4.0, 9)
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Percentage of Time Above Velocity')
    plt.title('%s' % get_string(str(key)))
    #plt.xticks([0.0, .5 , 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    plt.yticks([0, .1, .2, .3, .4, .5, .6, .7, .8 , .9, 1.0])

    y1 = percentage(team[0]['%s' % key]['v'])
    y2 = percentage(team[1]['%s' % key]['v'])
    y3 = percentage(team[2]['%s' % key]['v'])
    y4 = percentage(team[3]['%s' % key]['v'])
    y5 = percentage(team[4]['%s' % key]['v'])
    y6 = percentage(team[5]['%s' % key]['v'])
    y7 = percentage(team[6]['%s' % key]['v'])

    # y_master = []
    # for i in range(0,len(y1)):
    #     y_master.append(y1[i])




    plt.plot(x,y1,'ro-', label = 'Game 1') # Game 1 (fresh)
    plt.plot(x,y2,'bo-', label = 'Game 2') # Game 2 (1 day rest)
    plt.plot(x,y3,'mo-', label = 'Game 3') # Game 3 (2 days rest)
    plt.plot(x,y4,'go-', label = 'Game 4') # Game 4 (1 day rest)
    plt.plot(x,y5,'yo-', label = 'Game 5') # Game 5 (2 day rest)
    plt.plot(x,y6,'ko-', label = 'Game 6') # Game 6 (2 day rest)
    plt.plot(x,y7,'-o', label = 'Game 7') # Game 7 (2 day rest)



    plt.legend()
