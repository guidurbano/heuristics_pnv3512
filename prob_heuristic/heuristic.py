import numpy as np
import os
import time  # TODO: report time for processing
import math
import pandas as pd

ROOT = os.path.expanduser('~/src/heuristics_pnv3512/prob_heuristic/')

# Import data
filepath = ROOT + 'R101.txt'
col_names = ['number', 'x', 'y', 'demand',
             'ready_time', 'due_date', 'service_time']
with open(filepath, 'r') as file:
    df = pd.read_csv(file, delimiter=" ", skiprows=9, names=col_names,
                     header=None, skipinitialspace=True)

df['number'] = df['number'].astype(str)

# Parameters
k = 25  # Vehicle Number
cap = 200  # Capacity of vehicle
vel = 1  # Velocity
p = 5  # number of size of neighborhood closest clients

# Calculate how many vehicles are necessary (ceiling)
m = math.ceil(df.demand.sum() / cap)

# Distance Matrix (discomment to generate distance matrix)

# df_dist = pd.DataFrame(index=df.number, columns=df.number)
# for i in df['number'].tolist():
#     cust_1_x = df.loc[df['number'] == i, 'x'].values[0]
#     cust_1_y = df.loc[df['number'] == i, 'y'].values[0]
#     for j in df['number'].tolist():
#         cust_2_x = df.loc[df['number'] == j, 'x'].values[0]
#         cust_2_y = df.loc[df['number'] == j, 'y'].values[0]
#         df_dist.loc[i, j] = np.sqrt(
#             (cust_1_x - cust_2_x)**2 + (cust_1_y - cust_2_y)**2)
# df_dist.to_csv(ROOT + 'distance.csv', index=False)

df_dist = pd.read_csv(ROOT + 'distance.csv')

candidates = df_dist.iloc[0].sort_values(ascending=False).index.tolist()[:m] # TODO: adicionar "e afastados entre si".
print(f'Route first clients: {candidates}')

clients = candidates.copy()  # list of forbidden clients already dealt with
clients.append('0')
total_demands = list(np.zeros(m))

#  TODO: if not possible, repeat algorithm increasing m = m+1
#  TODO: Repeat heuristic 1000 times and register cost value
for num, i in enumerate(candidates):  # for every route
    total_demand = 0
    print(f'{num + 1} client: {i}')
    route = ['0']  # all routes start at depot
    route.append(i)  # each route has one candidate
    route.append('0')  # return to depot
    clients.append(i)  # remove from clients not in line

    total_demand = total_demand + df.loc[df['number'] == i, 'demand'].values[0]

    closest_clients = df_dist.loc[
        df['number'] == i,
        ~df_dist.columns.isin(clients)].squeeze().sort_values(
            ascending=True).index.tolist()
    #print(closest_clients)

    print(f'route: {route}')

    while (total_demand < cap) & (  # while vehicle is not full
           len(closest_clients) != 0):  # and no more clients to attend
        rnd_closest = np.random.choice(closest_clients[:p])  # draw one from p closest
        closest_clients.remove(rnd_closest)
        clients.append(rnd_closest)  # remove from clients not in line

        delta_demand = df.loc[df['number'] == rnd_closest,
                              'demand'].values[0]
        if total_demand + delta_demand > cap:
            break
        else:
            total_demand = total_demand + delta_demand

        # Define best insertion position
        best_pos = 2
        delta_dist = 10000000
        for position in range(2, len(route) - 1):
            delta_dist_2 = 0
            route_eval = route.copy()
            route_eval.insert(position, rnd_closest)

            for pre in range(0, len(route_eval) - 1):  # cost function  #TODO: encapsulate
                pos = pre + 1
                if pos == len(route_eval):
                    pass
                else:
                    delta_dist_2 = delta_dist_2 + df_dist.iloc[int(route_eval[pre]),
                                                               int(route_eval[pos])]
            if delta_dist_2 < delta_dist:
                delta_dist = delta_dist_2
                best_pos = position

        route.insert(best_pos, rnd_closest)
        # TODO: caculate route cost with function created in order todo

        print(f'{rnd_closest} inserted in {best_pos} position - Demand: {total_demand}')
        print(f'route after insertion: {route}')
        print(f'demand after insertion: {total_demand}')
    print(f'clients dealt with: {clients}\n')
    total_demands[num] = total_demand
    print('***************************************')

    # TODO: not all vehicles are being used and total demand doesnt match....
