import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import os


os.chdir ("D:/documents/CS 241/Data Analisis Project/nba_data")


players= pd.read_csv("players.csv", low_memory=False)

master=pd.read_csv("master.csv", low_memory=False)

print (players[players.points > 1200])
#Get the mean and the median points.
mean = players.points.mean()
median=players.points.median()

print (mean)

print (median)

#The highest number of point in a single season. 
nba= pd.merge(players,master, how="left", left_on="playerID", right_on="bioID")

HigherPoint_Row= nba[["year", "useFirst", "lastName", "points"]].sort_values("points", ascending =False).head(1)

print ( "The highest number of points recorded in a single season was {}, by {} {} in the year {}.".format(HigherPoint_Row.iloc[0][3],HigherPoint_Row.iloc[0][1],HigherPoint_Row.iloc[0][2],HigherPoint_Row.iloc[0][0] ))


#boxplot for the points, rebunds and assists

Boxplot= sns.boxplot(data=nba[["points", "rebounds", "assists"]])

plt.show()

#A plot that shows how the number of points scored has changed over time by showing the median of points scored per year, over time. 

yearsVSpoint= nba[["year", "points"]][nba.points >0].groupby("year",as_index=False).median()

print (yearsVSpoint) 

yearsVSpoint = yearsVSpoint.reset_index()

sns.regplot(data=yearsVSpoint, x="year", y="points").set_title("Median points per Year")

plt.show()

#Making a table to show the eficciency of the players in the differets kind of goal. 

#Concatenate two columns to get a full name of the players
nba.insert(nba.columns.get_loc("playerID")+1, "NameComplete", nba["useFirst"] +" "+ nba["lastName"]  )

#Make a column with the efficiency % of the Field Goal. Usign : made/Attempted *100
nba.insert(nba.columns.get_loc("fgMade") + 1 , "FGEfficiency",nba["fgMade"] / nba["fgAttempted"] * 100 )

#Make a column with the efficiency of the Free Throw. Usign : made/Attempted *100
nba.insert(nba.columns.get_loc("ftMade") + 1 , "FTEfficiency",nba["ftMade"] / nba["ftAttempted"] * 100 )

#Make a column with the efficiency of the Three Throw. Usign : made/Attempted *100
nba.insert(nba.columns.get_loc("threeMade") + 1 , "ThreeEfficiency",nba["threeMade"] / nba["threeAttempted"] * 100 )

#Make a column with the average of  efficiency. So we summ the differents Throw or goal Efficiency  and divide per three

nba.insert(nba.columns.get_loc("ThreeEfficiency")+1, "AverageEfficiency", (nba["FGEfficiency"] + nba["FTEfficiency"] + nba["ThreeEfficiency"]) /3)

N_Player=5

playerEfficiency=nba[["NameComplete","points","FGEfficiency","FTEfficiency","ThreeEfficiency", "AverageEfficiency"]][nba.threeMade >0 ] [nba.threeAttempted>0] .groupby("NameComplete",as_index=False).median().sort_values("points", ascending=False).head(N_Player)


print (playerEfficiency)

#---------------------------------------------------------------------------------------------------
Eficiency_list= ["FGEfficiency","FTEfficiency","ThreeEfficiency"]
colors = ['green', 'red', 'blue']
numerical = [[x for x in playerEfficiency.FGEfficiency],[x for x in playerEfficiency.FTEfficiency],[x for x in playerEfficiency.ThreeEfficiency] ]
average= [x for x in playerEfficiency.AverageEfficiency]
points = [x for x in playerEfficiency.points]
Better_Names = [x for x in playerEfficiency.NameComplete]
points_name= zip(points, Better_Names)
final_list= ["{}({})".format(y,str(x)) for x,y in points_name]
    
sns.set(style="white", rc={"lines.linewidth": 3})
number_groups = len(Eficiency_list) 
bin_width = 1.0/(number_groups+1)
fig, ax1 = plt.subplots(figsize=(6,6))
ax2 = ax1.twinx()
for i in range(number_groups):
    ax1.bar(x=np.arange(N_Player) + i*bin_width, 
           height=numerical[i],
           width=bin_width,
           color=colors[i],
           align='center')
ax1.set_xticks(np.arange(len(playerEfficiency.NameComplete)) + number_groups/(2*(number_groups+1)))
# number_groups/(2*(number_groups+1)): offset of xticklabel

ax1.set_xticklabels(playerEfficiency.NameComplete)
ax1.legend(Eficiency_list, facecolor='w')

sns.lineplot(x=final_list, 
             y=average,
             color='y',
             marker="o",
             ax=ax2)

plt.show()



#_________________________________________________________________________________________--
#Three throw


yearsVSThree= nba[["year", "threeMade"]][nba.threeMade>0].groupby("year",as_index=False).median()

print (yearsVSThree) 

yearsVSThree = yearsVSThree.reset_index()

sns.regplot(data=yearsVSThree, x="year", y="threeMade").set_title("Three Made per Year")

plt.show()

print (nba.columns)
GOAT= nba[["NameComplete","points","assists","steals","rebounds", "blocks"]].groupby("NameComplete",as_index=False).median().sort_values("points", ascending=False).head(N_Player)
GOAT.insert(GOAT.columns.get_loc("NameComplete")+1, "NamePoint", GOAT["NameComplete"] +" - "+ GOAT["points"].astype(str)  )

print (GOAT)
#--------------------------------------------------------------------------------------------------

Row_dict={}
GOAT_list= ["assists","steals","rebounds", "blocks"]


for index, rows in GOAT.iterrows():
   Row_dict[rows.NamePoint] = [rows.assists,rows.steals, rows.rebounds, rows.blocks]


fig, ax1 = plt.subplots(figsize=(8.2, 5.4))
for key in Row_dict:
        ax1.plot(GOAT_list, Row_dict[key], label=key)
    

ax1.legend()
#ax1.set_ylabel('Percentage (%)')
ax1.set_title('Greatest Of All Time ')
plt.show()

#-----------------------------------------------------------------------------------------------------------


