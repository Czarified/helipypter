import matplotlib.pyplot as plt
from matplotlib import __version__ as pltver
import matplotlib.ticker as ticker

import helipypter.vehicles as vh



def speed_power_polar(data):
    '''
    This function generates a standard speed-power polar plot.
    Input data must have columns following the standard naming
    convention of the helicopter class.
    
    ie. A dataframe output from the Helicopter.forward_flight method
    can be directly supplied.
    '''
    fig, ax = plt.subplots(figsize=(15,9))

    # Add the data and color it
    ax.plot(data.Airspeed, data.SHP_inst_req, color='orange', label='Installed Power', marker='o', markersize='4')
    ax.plot(data.Airspeed, data.SHP_uninst, color='green', label='Uninstalled Power', marker='o', markersize='4')
    ax.legend()

    # Axis labels
    ax.set_xlabel('Airspeed, $V$ [kts]', fontsize=12)
    ax.set_ylabel('Engine Power, $P$ [hp]', fontsize=12)
    ax.set_title('Speed-Power Polar\n', fontsize=18)

    # Move the axis and its label to the top
    # ax.xaxis.set_label_position('top')
    # ax.xaxis.tick_top()

    # Set the ticks
    # ax.xaxis.set_major_locator(ticker.FixedLocator([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
    ax.tick_params(which='minor', width=0.75, length=2.5)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='both', which='both', direction='in')

    # Set the grid lines
    ax.grid(b=True, which='major', linestyle=':')
    ax.grid(b=True, which='minor', linestyle=':', alpha=0.3)
    
    return fig, ax


def specific_range(data):
    '''
    This function generates a standard specific range plot.
    Input data must have columns following the standard naming
    convention of the helicopter class.
    
    ie. A dataframe output from the Helicopter.forward_flight method
    can be directly supplied.
    '''
    fig, ax = plt.subplots(figsize=(15,9))

    # Add the data and color it
    ax.plot(data.Airspeed, data.SR, color='orange', label='Specific Range', marker='o', markersize='4')
    ax.legend()

    # Axis labels
    ax.set_xlabel('Airspeed, $V$ [kts]', fontsize=12)
    ax.set_ylabel('Specific Range, $SR$ [nm/lb]', fontsize=12)
    ax.set_title('Specific Range Curve\n', fontsize=18)

    # Move the axis and its label to the top
    # ax.xaxis.set_label_position('top')
    # ax.xaxis.tick_top()

    # Set the ticks
    # ax.xaxis.set_major_locator(ticker.FixedLocator([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]))
    ax.tick_params(which='minor', width=0.75, length=2.5)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='both', which='both', direction='in')

    # Set the grid lines
    ax.grid(b=True, which='major', linestyle=':')
    ax.grid(b=True, which='minor', linestyle=':', alpha=0.3)
    
    return fig, ax


def roc(data):
    '''
    This function generates a standard rate of climb plot.
    Input data must have columns following the standard naming
    convention of the helicopter class.
    
    ie. A dataframe output from the Helicopter.forward_flight method
    can be directly supplied.
    '''
    fig, ax = plt.subplots(figsize=(15,9))

    # Add the data and color it
    ax.plot(data.Airspeed, data.ROC, color='orange', label='Rate of Climb', marker='o', markersize='4')
    ax.legend()

    # Axis labels
    ax.set_xlabel('Airspeed, $V$ [kts]', fontsize=12)
    ax.set_ylabel('Rate of Climb, $ROC$ [ft/min]', fontsize=12)
    ax.set_title('Forward Flight Rate of Climb\n', fontsize=18)

    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='both', which='both', direction='in')

    # Set the grid lines
    ax.grid(b=True, which='major', linestyle=':')
    ax.grid(b=True, which='minor', linestyle=':', alpha=0.3)
    
    return fig, ax


def missionSim(heli, mission) -> dict:
    '''
    This function runs a helicopter through a mission. For each point, 
    the fuel consumption is evaluated, and the flight distance is evaluated.

    :param heli: Helicopter to be analyzed.
    :type heli: :class:`~helipypter.vehicles.Helicopter`
    :param mission: Mission profile to be analyzed.
    :type mission: tuple(nametuple)

    :return: Mission data table
    :rtype: dict
    '''
    output = {'dist':[], 'fuel_rem':[], 'fuel_used':[]}

    for point in mission:
        d = 0
        if point.maneuver == 'idle':
            fuel = heli.idle()/60 * point.duration
            heli.burn(fuel)
        elif point.maneuver == 'hover':
            # Actually calculate the fuel cost for
            # hovering at an exact weight and altitude
            data = heli.HOGE(vh.Environment(point.altitude))
            fuel = data['sfc']*data['SHP_unins']*point.duration/60
            heli.burn(fuel)
        elif point.maneuver == 'loiter':
            data = heli.forward_flight(vh.Environment(point.altitude), point.speed)
            fuel = data.SHP_uninst[0]*data.bsfc[0]/60 * point.duration
            heli.burn(fuel)
        elif point.maneuver == 'IRP':
            # IRP is the engine rated limit
            sfc = heli.bsfc(100)
            fuel = sfc*1*heli.pwr_lim/60 * point.duration
            heli.burn(fuel)
        elif point.maneuver == 'MCP':
            # MCP is defined as 95% of IRP
            sfc = heli.bsfc(95)
            fuel = sfc*0.95*heli.pwr_lim/60 * point.duration
            heli.burn(fuel)
            d = 120*point.duration/60   # 120 kts has more ROC than 1000 TODO: Calculate this.
        elif point.maneuver == 'flight':
            data = heli.forward_flight(vh.Environment(point.altitude), point.speed)
            fuel = point.duration/data.SR[0]
            heli.burn(fuel)
            d = point.duration
        elif point.maneuver == 'unload':
            heli.unload(point.speed)
            fuel = heli.idle()/60 * point.duration
            heli.burn(fuel)

        output['dist'].append(d)
        output['fuel_rem'].append(heli.GW_fuel)
        output['fuel_used'].append(fuel)


    return output


