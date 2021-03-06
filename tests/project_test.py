
import os
from collections import namedtuple
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import helipypter.vehicles as vh
import helipypter.funcs as func

# Set the CWD to tests dir
os.chdir('tests')

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s -  %(levelname)s -  %(message)s',
    filename='helipypter.out',
    filemode='w'
)


## Build the Project Helicopter
heli = vh.Helicopter(name='Project Helicopter Spec',
                  MR_dia = 35,
                    MR_b = 4,
                   MR_ce = 10.4,
                MR_Omega = 43.2,
                  MR_cd0 = 0.0080,
                  TR_dia = 5.42,
                    TR_b = 4,
                   TR_ce = 7,
                TR_Omega = 239.85,
                  TR_cd0 = 0.015,
                GW_empty = 2853,
                 GW_fuel = 869,
              GW_payload = 1278,
                download = 0.03,
                      fe = 12.9,
                  l_tail = 21.21,
                    S_vt = 20.92,
                   cl_vt = 0.22,
                   AR_vt = 3
                        )
logging.info('\n' + heli.__str__())
logging.info('')


## What is the basic hover performance?
atm = vh.Environment(0)
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
logging.info('{:^45}'.format('Results - HOGE'))
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in heli.HOGE(atm).items():
    logging.info('{:>17}:  {:>7.4}'.format(k, v))
    

logging.info('')
logging.info('')
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
logging.info('{:^45}'.format('Results - HIGE'))
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in heli.HIGE(atm).items():
    logging.info('{:>17}:  {:>7.4}'.format(k, v))


## Forward flight performance over the speed sweep
speeds = list(np.linspace(20, 150, num=27))
data = heli.forward_flight(atm, speeds)

data.to_excel('SpeedSweep.xlsx')

## Uncomment this section to print all the data to console
## It's just a dataframe, so it can be printed, stored,
## saved as text or even as a workbook.

# with pd.option_context('display.max_columns', 100):
#     print(data.set_index('Airspeed'))


## Plot stuff
fig, ax = func.specific_range(data)
fig.savefig('Specific_Range.png')
fig, ax = func.speed_power_polar(data)
fig.savefig('Speed_Power_Polar.png')
fig, ax = func.roc(data)
fig.savefig('Rate_of_Climb.png')


fig, ax = plt.subplots(figsize=(15,7))

# Add the data and color it
ax.plot(data.Airspeed, data.SHP_inst_req, color='orange', label='Installed Power', marker='o', markersize='4')
ax.plot(data.Airspeed, data.SHP_uninst, color='green', label='Uninstalled Power', marker='o', markersize='4')
ax.legend()

# Axis labels
ax.set_xlabel('Airspeed, $V$ [kts]', fontsize=12)
ax.set_ylabel('Engine Power, $P$ [hp]', fontsize=12)

# Set the ticks
ax.tick_params(which='minor', width=0.75, length=2.5)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.tick_params(axis='both', which='both', direction='in')

# Set the grid lines
ax.grid(b=True, which='major', linestyle=':')
ax.grid(b=True, which='minor', linestyle=':', alpha=0.3)

ax2 = ax.twinx()
color = 'darkred'
ax2.set_ylabel('Rate of Climb, $ROC$ [ft/min]', fontsize=12, color=color)
ax2.plot(data.Airspeed, data.ROC, color=color, label='Rate of Climb', marker='o', markersize='4')
ax2.tick_params(labelcolor=color)
ax2.legend()

ax.set_title('Helicopter Speed Sweep', fontsize=18)
fig.savefig('testfig.png')


## Mission Creation

# A mission is a set of misson points, where each point has: a maneuver, an altitude, and a duration (length/range or time).
# Maneuver types include: Idle, Hover, MCP, Flight, Load, or Unload
# Each maneuver type corresponds to a Helicopter class-method.
Point = namedtuple('MissionPoint', ['maneuver', 'altitude', 'duration', 'speed'])
startup = Point('idle', 0, 1, 0)
hover_0 = Point(maneuver='IRP', altitude=0, duration=1, speed=0)
climb_0 = Point('MCP', 0, 5, 1000)
cruise_0 = Point('flight', 5000, 160, 110)
hover_1 = Point('hover', 0, 1, 0)
loiter = Point('loiter', 5000, 10, 60)
unload = Point('unload', 0, 5, 1278)
ground = Point('idle', 0, 1, 0)


mission = (startup, hover_0,
           climb_0, cruise_0, loiter,
           hover_1, unload, hover_1,
           climb_0, cruise_0,
           hover_1, ground
          )

# GW reset for debugging purposes
heli.GW_payload = 1278
heli.GW_fuel = 869

# Mission Loop
logging.info('')
logging.info('')
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
logging.info('{:^45}'.format('Project Spec Mission'))
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
# Initialize the range tracker
mission_range = 0
for point in mission:
    if point.maneuver == 'idle':
        fuel = heli.idle()/60 * point.duration
        heli.burn(fuel)
        logging.info(f'Idled for {point.duration}[mins].')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
    
    elif point.maneuver == 'hover':
        # Actually calculate the fuel cost for
        # hovering at an exact weight and altitude
        data = heli.HOGE(vh.Environment(point.altitude))
        fuel = data['sfc']*data['SHP_unins']*point.duration/60
        heli.burn(fuel)
        logging.info(f'Hovered for {point.duration}[mins], burning {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
    
    elif point.maneuver == 'loiter':
        data = heli.forward_flight(vh.Environment(point.altitude), point.speed)
        fuel = data.SHP_uninst[0]*data.bsfc[0]/60 * point.duration
        heli.burn(fuel)
        logging.info(f'Loitered at {point.speed}[kts] for {point.duration}[mins].')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
    
    elif point.maneuver == 'IRP':
        # IRP is the engine rated limit
        sfc = heli.bsfc(100)
        fuel = sfc*1*heli.pwr_lim/60 * point.duration
        heli.burn(fuel)
        logging.info(f'Ran at IRP for {point.duration}[mins].')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
    
    elif point.maneuver == 'MCP':
        # MCP is defined as 95% of IRP
        sfc = heli.bsfc(95)
        fuel = sfc*0.95*heli.pwr_lim/60 * point.duration
        heli.burn(fuel)
        logging.info(f'MCP Climb for {point.duration}[mins] @ {point.speed}[ft/min].')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
        mission_range += 120*point.duration/60   # 120 kts has more ROC than 1000 TODO: Calculate this.
    
    elif point.maneuver == 'flight':
        data = heli.forward_flight(vh.Environment(point.altitude), point.speed)
        fuel = point.duration/data.SR[0]
        heli.burn(fuel)
        logging.info(f'Forward flight for {point.duration}[nm] @ {point.speed}[kts].')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
        mission_range += point.duration 
    
    elif point.maneuver == 'climb':
        # Represents a hover climb/descent NOT @ MCP
        # There's no range credit for a "climb" maneuver instead of an "MCP" maneuver.
        data = heli.HOGE(vh.Environment(point.altitude), Vroc=point.speed)
        fuel = data['sfc']*data['SHP_unins']*point.duration/60
        heli.burn(fuel)
        logging.info(f'Climb for {point.duration}[min] @ {point.speed}[ft/min]')
        logging.info(f'   Burned {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
    
    elif point.maneuver == 'unload':
        logging.info(f'Landed! Unloading {point.speed}[lbs] of cargo.')
        heli.unload(point.speed)
        fuel = heli.idle()/60 * point.duration
        heli.burn(fuel)
        logging.info(f'Idled for {point.duration}[mins], burning {fuel:.2f}[lbs] of fuel.')
        logging.info(f'   New GW = {heli.GW:.2f}[lbs], fuel: {heli.GW_fuel:.2f}')
        logging.info('')
        
logging.info('')
logging.info(f'Mission Complete! {heli.GW_fuel:.2f} [lbs] of fuel remaining.')
logging.info(f'Total Range = {mission_range:.2f}[nm]')
logging.info('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')