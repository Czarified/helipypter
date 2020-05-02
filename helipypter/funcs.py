import matplotlib.pyplot as plt
from matplotlib import __version__ as pltver
import matplotlib.ticker as ticker



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