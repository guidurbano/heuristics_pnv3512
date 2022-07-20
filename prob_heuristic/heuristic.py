import numpy as np
import os
import time  # TODO: report time for processing
import math
import pandas as pd
import altair as vg

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


def cost(df_dist: pd.DataFrame,
         route: list) -> int:
    """Calculate cost of given route."""
    dist = 0
    for pre in range(0, len(route) - 1):
        pos = pre + 1
        if pos == len(route):
            pass
        else:
            dist = dist + df_dist.iloc[int(route[pre]), int(route[pos])]
    return dist


def main():
    total_cost = 0
    seed_nodes = []

    for j in range(0, m):  # Routine to define m seeds
        origin_dist = df_dist.iloc[0]
        if j == 0:  # first seed is farthest node
            new_seed = origin_dist.sort_values(
                ascending=False).index.tolist()[0]
        else:  # seeds maximize product of distances between each other
            seeds_dist_prod = df_dist.loc[
                df['number'].isin(seed_nodes),
                ~df_dist.columns.isin(seed_nodes)].prod(axis=0)
            prod = origin_dist.multiply(seeds_dist_prod)
            new_seed = prod.sort_values(
                        ascending=False).index.tolist()[0]
        seed_nodes.append(new_seed)

    print(f'Seeds: {seed_nodes}')

    clients = seed_nodes.copy()  # list of forbidden clients already dealt with
    clients.append('0')
    total_demands = list(np.zeros(m))

    #  TODO: if not possible, repeat algorithm increasing m = m+1
    #  TODO: Repeat heuristic 1000 times
    for num, i in enumerate(seed_nodes):  # for every route
        total_demand = 0
        print(f'{num + 1} client: {i}')
        route = ['0', i, '0']  # all routes has one candidate, starts and ends in depot
        clients.append(i)  # remove from clients not in line
        clients = list(set(clients))

        total_demand = total_demand + df.loc[df['number'] == i,
                                             'demand'].values[0]

        closest_clients = df_dist.loc[  # Closest nodes to route
            df['number'].isin(route),
            ~df_dist.columns.isin(clients)].min().squeeze().sort_values(
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
            dist = 10000000
            for position in range(2, len(route) - 1):
                route_eval = route.copy()
                route_eval.insert(position, rnd_closest)
                dist_2 = cost(df_dist, route_eval)

                if dist_2 < dist:
                    dist = dist_2
                    best_pos = position

            route.insert(best_pos, rnd_closest)

            print(f'{rnd_closest} inserted in {best_pos} position - Demand: {total_demand}')
            print(f'...Route: {route}')
        print('***************************************')
        print(f'{len(clients)} clients dealt with: {clients}\n')
        print('***************************************')
        total_demands[num] = total_demand
        total_cost = total_cost + dist
    print(f'Demands per vehicle: {total_demands}, Total = {sum(total_demands)}/{df.demand.sum()}')
    print(f'FO: {total_cost}')
        # TODO: total demand doesnt match demand attended.


if __name__ == "__main__":
    main()
