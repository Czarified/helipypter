from helipypter import *

## Build the Project Helicopter
heli = Helicopter(name='Project Helicopter Spec',
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
print(heli)


## What is the basic hover performance?
atm = Environment(0)
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
print('{:^45}'.format('Results - HOGE'))
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in heli.HOGE(atm).items():
    print('{:>17}:  {:>7.4}'.format(k, v))
    


print('\n\n-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
print('{:^45}'.format('Results - HIGE'))
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in heli.HIGE(atm).items():
    print('{:>17}:  {:>7.4}'.format(k, v))


speeds = list(np.linspace(20, 150, num=28))
data = heli.forward_flight(atm, speeds)

with pd.option_context('display.max_columns', 100):
    print(data.set_index('Airspeed'))


## Plot stuff
fig, ax = specific_range(data)
fig.savefig('Specific_Range.png')
fig, ax = speed_power_polar(data)
fig.savefig('Speed_Power_Polar.png')
fig, ax = roc(data)
fig.savefig('Rate_of_Climb.png')


## Mission Creation

# A mission is a set of misson points, where each point has: a maneuver, an altitude, and a duration (length/range or time).
# Maneuver types include: Idle, Hover, MCP, Flight, Load, or Unload
# Each maneuver type corresponds to a Helicopter class-method.
Point = namedtuple('MissionPoint', ['maneuver', 'altitude', 'duration', 'speed'])
startup = Point('idle', 0, 1, 0)
hover_0 = Point(maneuver='hover', altitude=0, duration=1, speed=0)
climb_0 = Point('MCP', 0, 5, 1000)
cruise_0 = Point('flight', 5000, 165, 120)
hover_1 = Point('hover', 0, 1, 0)
unload = Point('unload', 0, 5, 1278)
ground = Point('idle', 0, 1, 0)


mission = (startup, hover_0,
           climb_0, cruise_0,
           hover_1, unload, hover_1,
           climb_0, cruise_0,
           hover_0, ground
          )