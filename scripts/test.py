import numpy as np
import matplotlib.pylab as plt
import sys

sys.path.insert(0, '../sportvu/')
import reading as r

#infilename = ['Sportvu_Data/game1_q1.XML']
#'''
infilename = ['Sportvu_Data/game1_q1.XML',
              'Sportvu_Data/game1_q2.XML',
              'Sportvu_Data/game1_q3.XML',
              'Sportvu_Data/game1_q4.XML']
#'''


#infilename = ['quarter1.XML', 'quarter2.XML', 'quarter3.XML', 'quarter4.XML']

players,homeplayers,awayplayers,hometeam,awayteam,ball, homeScore, awayScore, sc = r.get_player_data(infilename)
#r.playerNames(hometeam,awayteam)

print(hometeam.keys())

#p = hometeam['457605'] # Isaiah Thomas
p = awayteam['509456'] # John Wall
v = p['v']
t = p['veloTime']

plt.figure()
plt.plot(t,v)

plt.show()
