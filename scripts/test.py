import numpy as np
import matplotlib.pylab as plt
import sys

sys.path.insert(0, '../sportvu/')
import reading as r

infilename = ['Sportvu_Data/quarter1.XML']


#infilename = ['quarter1.XML', 'quarter2.XML', 'quarter3.XML', 'quarter4.XML']

players,homeplayers,awayplayers,hometeam,awayteam,ball, homeScore, awayScore, sc = r.get_player_data(infilename)
r.playerNames(hometeam,awayteam)
