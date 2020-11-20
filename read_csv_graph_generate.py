#Import Libraries
import pandas as pd
import numpy as np
import datetime
import calendar
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Create a new figure.
fig = plt.figure()
#Add an Axes to the figure as part of a subplot arrangement where the first digit is
#the number of rows, second column and third index. 
ax1 = fig.add_subplot(4,2,1)
ax2 =fig.add_subplot(4,2,2)
ax3 = fig.add_subplot(4,2,5)
ax4 = fig.add_subplot(4,2,6)


def animate(i):
# Load csv file as a dataframe.
    dataframe = pd.read_csv("node1_data.csv")
#Select last 6 values from the dataframe.
    plotdata = pd.DataFrame(dataframe.tail(6), columns=["timestamp", "lpg (ppm)",
                                                        "carbon monoxide (ppm)", "smoke (ppm)",
                                                        "temperature (C)", "light (lux)",
                                                        "flame (y/n)"])
#Change timestamp column from string to datetime format.
    plotdata["timestamp"] = pd.to_datetime(plotdata["timestamp"])
#Get current date and weekname for plot title.   
    date_now = plotdata["timestamp"].dt.strftime("%d-%m-%Y").iloc[-1]
    weekday = plotdata["timestamp"].dt.strftime("%A").iloc[-1]
#Create a new time column for x-axis.    
    plotdata["time"] = plotdata["timestamp"].dt.strftime("%H:%M:%S")
#Create plot for Gas values.   
    ax1.clear()
    ax1.plot(plotdata["time"], plotdata["lpg (ppm)"], linestyle ="--")
    ax1.plot(plotdata["time"], plotdata["carbon monoxide (ppm)"], linestyle = "dashdot")
    ax1.plot(plotdata["time"], plotdata["smoke (ppm)"])
    ax1.legend(["lpg", "co", "smoke"])
    ax1.set_xlabel("time"), ax1.set_ylabel("ppm")
    ax1.set_title("Gas\n {} {} ".format(weekday, date_now))
#Create plot for Temperature value.
    ax2.clear()
    ax2.plot(plotdata["time"], plotdata["temperature (C)"])
    ax2.legend(["Temperature (°C)"])
    ax2.set_xlabel("time"), ax2.set_ylabel("Celsius")
    ax2.set_title("Temperature\n {} {} ".format(weekday, date_now))
#Create plot for Light value.
    ax3.clear()
    ax3.plot(plotdata["time"], plotdata["light (lux)"])
    ax3.legend(["light (lux)"])
    ax3.set_xlabel("time"), ax3.set_ylabel("Lux")
    ax3.set_title("Light\n {} {} ".format(weekday, date_now))
#Create plot for Flame value.
    ax4.clear()
    ax4.plot(plotdata["time"], plotdata["flame (y/n)"])
    ax4.legend(["flame"])
    ax4.set_xlabel("time"), ax4.set_ylabel("1=Y ,0=N")
    ax4.set_title("Flame\n {} {} ".format(weekday, date_now))
#Initiate dynamic graph.
ani_gas = animation.FuncAnimation(fig, animate, interval = 1000)
#show the plot.
plt.show()


