import numpy as np
import pandas as pd
import time
import seaborn as sns
import random
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

'''Diamond Valley JP pricing'''

RTP = 0.9716

JP_cont = 0.01

base_loss = 1-RTP

mean_JP = 59456

seed = 4000

bet = 200

pct_cont = 0.2

avg_spins = (mean_JP - seed)/(bet/100)

p = 1/avg_spins

frequency = 15

break_even = base_loss/JP_cont*mean_JP


'''EV as a function of starting JP and full ownership of contribution'''
def EV_func_2(JP, x):
    EV = 0
    for i in range(x):
        EV = EV + ((1-p)**i)*(p*(JP+ i*bet/100) - bet*base_loss)
    return EV


'''EV as a function starting JP and pct_cont owenership of total contribution'''
def EV_func_3(JP, x):
    EV = 0
    for i in range(x):
        EV = EV + ((1-((1/pct_cont)*p))**i)*(p*(JP+ i*bet*(1/pct_cont)/100) - bet*base_loss)
    return EV


'''Shorter calculation for EV'''
def EV_func_4(JP):
    return pct_cont*(JP + (bet*JP_cont*avg_spins))-pct_cont*(bet*avg_spins*base_loss)


'''CDF and PDF with Geometric distribution where p = 1/avg_spins'''
def CDF(x):
    k = (x - seed)/(bet/100)
    return float((1 - p)**k)

def PDF(x):
    k = (x - seed)/(bet/100)
    return ((1 - p)**(k-1))*(p)


'''applying EV_func_4 to calculate EV as a function of starting JP value and percent of market owned'''
JP_values = []
for i in range(1000000):
    JP_values.append(4000 + bet*JP_cont*i)

EV_list = EV_func_4(np.array(JP_values))   

prob_playable = CDF(break_even)

EV_data = pd.DataFrame(JP_values, columns = ['JP'])
EV_data['EV'] = EV_func_4(EV_data['JP'])
EV_data['p(x=x)'] = PDF(EV_data['JP'])
EV_data['EV_per_JP'] = EV_data['EV']*EV_data['p(x=x)']

playable_data = EV_data[EV_data['EV'] > 0]

EV_per_JP = playable_data['EV_per_JP'].sum()

EV_per_year = (EV_per_JP*365/frequency)#/pct_cont

avg_time_until_return = (1/(pct_cont*prob_playable))*frequency


'''Using odds and stake as described above to calculate the required kelly bankroll, given a fixed stake 
per JP and plotting on a 3d space with respect to JP_value and pct of market owned'''
def kelly_bank(JP, pct):
    b = ((JP + mean_JP) - (pct*avg_spins*base_loss*bet))/(pct*avg_spins*base_loss*bet)
    return break_even/((pct*b + pct - 1)/b)
  
x = np.linspace(167, 500, 30)
y = np.linspace(0.1, 0.6)

X, Y = np.meshgrid(x, y)
Z = (kelly_bank(X*1000, Y))/1000

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='b')
ax.set_title('surface');
ax.set_xlabel('JP_value in 000')
ax.set_ylabel('Market ownership')
ax.set_zlabel('Kelly Bank in 000');







            
        























