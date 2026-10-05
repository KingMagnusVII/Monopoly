import pandas as pd
import numpy as np
import PATH

PATH= PATH.path #path file addition

#chance data


csv_chance = PATH + 'Data-Files\\chance.csv'

df = pd.read_csv(csv_chance)

data_array = df.to_numpy()

chance = []
for i in range(len(data_array)):
    chance.append(data_array[i][0])

chance_amount = []
for i in range(len(data_array)):
    chance_amount.append(data_array[i][1])

chance_image = []
for i in range(len(data_array)):
    chance_image.append(data_array[i][2])


#community chest data

csv_community = PATH+ 'Data-Files\\community.csv'

df = pd.read_csv(csv_community)

data_array = df.to_numpy()

community = []
for i in range(len(data_array)):
    community.append(data_array[i][0])

community_amount = []
for i in range(len(data_array)):
    community_amount.append(data_array[i][1])

community_image = []
for i in range(len(data_array)):
    community_image.append(data_array[i][2])
