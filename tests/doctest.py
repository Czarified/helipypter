from collections import namedtuple
import copy

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import helipypter.vehicles as vh
import helipypter.funcs as func





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

doc_chopper = vh.Helicopter(name='Documentation Helicopter Spec',
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
            GW_empty = w_empty,
                GW_fuel = w_fuel,
            GW_payload = w_payload,
            download = 0.03,
                    fe = 12.9,
                l_tail = 21.21,
                S_vt = 20.92,
                cl_vt = 0.22,
                AR_vt = 3
                    )

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

# Copy the previous vehicle, and modify the weights
lightweight = copy.copy(doc_chopper)
lightweight.GW_empty = w_empty
lightweight.GW_fuel = w_fuel
lightweight.GW_payload = w_payload
out = pd.DataFrame(data=func.missionSim(lightweight, mission), columns=['dist', 'fuel_rem', 'fuel_used'])

## Reduce the MR_cd0
## Reduce the fe

cd0_factor = 0.95
fe_factor = 0.95


clean_chopper = copy.copy(doc_chopper)
# GW Reset
w_empty = EW_frac*GW_total + w_crew + w_fluids
# Our payload is 6 people @ 213 lbs each
w_payload = 6*213
w_fuel = GW_total - w_empty - w_payload
clean_chopper.GW_fuel = w_fuel
clean_chopper.GW_payload = w_payload
clean_chopper.MR_cd0 = cd0_factor*clean_chopper.MR_cd0
clean_chopper.fe = fe_factor*clean_chopper.fe
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