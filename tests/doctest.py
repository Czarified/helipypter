from collections import namedtuple
import copy

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import helipypter.vehicles as vh
import helipypter.funcs as func

# Function to use later on
def chopper_gen(args) -> vh.Helicopter:
    '''
    This function generates a helicopter class based on input arguments.
    It's just a short way to use all the same arguments.
    '''
    chopper = vh.Helicopter(name = args[0] ,
                            MR_dia = args[1] ,
                            MR_b = args[2] ,
                            MR_ce = args[3] ,
                            MR_Omega = args[4] ,
                            MR_cd0 = args[5] ,
                            TR_dia = args[6] ,
                            TR_b = args[7] ,
                            TR_ce = args[8] ,
                            TR_Omega = args[9] ,
                            TR_cd0 = args[10],
                            GW_empty = args[11],
                            GW_fuel = args[12],
                            GW_payload = args[13],
                            download = args[14],
                            fe = args[15],
                            l_tail = args[16],
                            S_vt = args[17],
                            cl_vt = args[18],
                            AR_vt = args[19]
                            )
    return chopper


# Empty weight fraction
EW_frac = 0.528
# Total Gross Weight
GW_total = 5000
# Crew Weight
w_crew = 200
# Trapped Fluids
w_fluids = 13

w_empty = EW_frac*GW_total + w_crew + w_fluids
# Our payload is 6 people @ 213 lbs each
w_payload = 6*213
w_fuel = GW_total - w_empty - w_payload

args = ['Documentation Helicopter Spec', 35, 4, 10.4, 43.2, 0.0080,
        5.42, 4, 7, 239.85, 0.015, w_empty, w_fuel,  w_payload,
        0.03, 12.9, 21.21, 20.92, 0.22, 3
]

doc_chopper = chopper_gen(args)

atm = vh.Environment(0)
output = doc_chopper.HOGE(atm)
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
print('{:^45}'.format('Results - HOGE'))
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in doc_chopper.HOGE(atm).items():
    print('{:>17}:  {:>7.4}'.format(k, v))


speeds = list(np.linspace(20, 150, num=28))
data = doc_chopper.forward_flight(atm, speeds)


pwrs = list(np.linspace(0, 100))
bsfc = []
FF = []
for p in pwrs:
    bsfc.append(doc_chopper.bsfc(p))
    FF.append(p*doc_chopper.bsfc(p))

eff = [0.8*b for b in bsfc]

fig, ax = plt.subplots(figsize=(7,5))
ax.plot(pwrs, bsfc, color='orange', label='default')
ax.plot(pwrs, eff, color='green', label='20% more efficient')
ax.set_xlabel('Percent Power', fontsize=12)
ax.set_ylabel('bsfc, $[\\frac{lb}{hp*hr}]$', fontsize=12)
ax.set_ylim(bottom=0)
ax.legend()
# Set the ticks
ax.tick_params(which='minor', width=0.75, length=2.5)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.tick_params(axis='both', which='both', direction='in')
# Set the grid lines
ax.grid(b=True, which='major', linestyle=':')
ax.grid(b=True, which='minor', linestyle=':', alpha=0.3)
ax.set_title('Normalized BSFC Default')



## Mission evaluation
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

out = pd.DataFrame(data=func.missionSim(doc_chopper, mission), columns=['dist', 'fuel_rem', 'fuel_used'])
print('Default chopper range: {}'.format(out.dist.sum()))
print(f'Default chopper remaining fuel: {out.fuel_rem.iat[-1]:.2f}')

## Reduce the empty weight fraction
EW_factor = 0.95

# Empty weight fraction
EW_frac = 0.528
# Total Gross Weight
GW_total = 5000
# Crew Weight
w_crew = 200
# Trapped Fluids
w_fluids = 13

w_empty = EW_factor*EW_frac*GW_total + w_crew + w_fluids
# Our payload is still 6 people @ 213 lbs each
w_payload = 6*213
w_fuel = GW_total - w_empty - w_payload

lite_args = copy.copy(args)
lite_args[11] = w_empty
lite_args[12] = w_fuel
lite_args[13] = w_payload 

# Generate the new vehicle, with all other characteristics the same
lightweight = chopper_gen(lite_args)
out = pd.DataFrame(data=func.missionSim(lightweight, mission), columns=['dist', 'fuel_rem', 'fuel_used'])
print(f'Lite chopper range: {out.dist.sum()}')
print(f'Lite chopper remaining fuel: {out.fuel_rem.iat[-1]:.2f}')


## Reduce the MR_cd0
## Reduce the fe
cd0_factor = 0.95
fe_factor = 0.95

clean_args = copy.copy(args)
clean_args[5] = cd0_factor*clean_args[5]
clean_args[15] = fe_factor*clean_args[15]

clean_chopper = chopper_gen(clean_args)

out = pd.DataFrame(data=func.missionSim(clean_chopper, mission), columns=['dist', 'fuel_rem', 'fuel_used'])
print(f'Clean chopper range: {out.dist.sum()}')
print(f'Clean chopper remaining fuel: {out.fuel_rem.iat[-1]:.2f}')



## Reduce the Induced Power Factor
## Increase the fuel efficiency of the engine
eng_fac = 0.97

# Use this k_i when calling Helicopter.hover()
k_i = 1.05

efficient_chopper = copy.copy(doc_chopper)
efficient_chopper.bsfc_0 = eng_fac*efficient_chopper.bsfc_0
efficient_chopper.bsfc_1 = eng_fac*efficient_chopper.bsfc_1
efficient_chopper.bsfc_2 = eng_fac*efficient_chopper.bsfc_2
efficient_chopper.bsfc_3 = eng_fac*efficient_chopper.bsfc_3
efficient_chopper.bsfc_4 = eng_fac*efficient_chopper.bsfc_4
efficient_chopper.bsfc_5 = eng_fac*efficient_chopper.bsfc_5

# Since this one is a copy of the old one
# We've already burned all the fuel and unloaded
# it, so we need to reset the weight values.
efficient_chopper.refuel()
efficient_chopper.reload()

out = pd.DataFrame(data=func.missionSim(efficient_chopper, mission), columns=['dist', 'fuel_rem', 'fuel_used'])
print(f'Efficient chopper range: {out.dist.sum()}')
print(f'Efficient chopper remaining fuel: {out.fuel_rem.iat[-1]:.2f}')