import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import sys
import matplotlib.pyplot as plt
import xml.etree.cElementTree as ET

from sklearn.linear_model import LinearRegression

#new
import osmnx as ox
import networkx as nx
import folium


#adapted from https://stackoverflow.com/questions/60578408/is-it-possible-to-draw-paths-in-folium
#folium syntax/guide https://python-visualization.github.io/folium/quickstart.html
#https://snyk.io/advisor/python/osmnx/functions/osmnx.get_nearest_node
#https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=nearest_node#osmnx.distance.nearest_nodes


#add pictures to points on map
#https://www.youtube.com/watch?v=clP6W7W79MM&ab_channel=Code%26Dogs

def ConvertToString(i):
	return str(i)

#not used
def serialize(x,y):
	return str(x) + " " + str(y)

def deserialize(s):
	arr = s.split()
	#arr = [int(x) for x in arr]
	return arr

def ResetRows(df):
	#note: always choose second because first will always be going to itself
	df['lon'] = df.iloc[0]['lon']
	df['lat'] = df.iloc[0]['lat']
	df['distance'] = df.iloc[0]['distance']
	df['points'] = df.iloc[0]['points']
	df['sorting_metric'] = df.iloc[0]['sorting_metric']

def AddNewPoint(temp,df, destination, distance, total_num_points, current_num_points):
	ideal_lat = temp.iloc[0]['lat'] + ((destination[0] - temp.iloc[0]['lat']) / (total_num_points - current_num_points))
	ideal_lon = temp.iloc[0]['lon'] + ((destination[1] - temp.iloc[0]['lon']) / (total_num_points - current_num_points))
	temp['points'] = temp['points'] + " " +  df['string_index']
	temp['sorting_metric'] =  np.square((df['lat'] - ideal_lat)**2 + (df['lon'] - ideal_lon)**2)
	temp['distance'] = df['distance']
	temp['lat'] = df['lat']
	temp['lon'] = df['lon']
	
def get_route(df, origin, destination,G, output,num_points,max_distance_mod,num_routes):
	#distance = from origin to destination
	distance = np.square((origin[0] - destination[0])**2 + (origin[1] - destination[1])**2)
	max_distance = distance * max_distance_mod
	
	#use linregress to drop nodes a certain distance from the line
	slope, intercept, r_value, p_value, std_err = stats.linregress(np.array([origin[1], destination[1]]),np.array([origin[0] , destination[0]]))
	df["distance"] = abs(df['lat'] - (intercept + slope * df['lon']))
	df = df[df['distance'] < max_distance * 100]
	df = df.drop(columns=['distance'])
	
	'''
	#testing: visualize the remaining possible destinations
	y = df['lat']
	x = df['lon']
	plt.plot(x, y, 'o', label='original data')
	plt.plot(x, intercept + slope*x, 'r', label='fitted line')
	plt.show()
	'''
	
	#calculate distance from each point to destination
	df['distance'] = np.square((df['lat'] - destination[0])**2 + (df['lon'] - destination[1])**2)
	
	#add points list
	df['points'] = ''
	
	
	routes = []
	#note: a loop here is not inefficient because the loop is not used to iterate through the dataframe
	route_num = 0
	for i in range (num_routes):
	
		#HAVE A TEMP DATA FRAME
		temp = df.copy()
		temp['lon'] = origin[1]
		temp['lat'] = origin[0]
		temp['distance'] = distance
		#temp = temp.drop(columns=['index'])
		temp = temp.drop(columns=['name'])
		temp['sorting_metric'] = distance/num_points
		
		#need to do this for each route
		original = df.copy(deep = True)
		
		#note: a loop here is not inefficient because the loop is not used to iterate through the dataframe
		for j in range(num_points):
			ResetRows(temp) #make all rows = first
			AddNewPoint(temp,df, destination, distance, num_points, j)#add each row of df to each row of temp
			temp = temp.sort_values(by=['sorting_metric']) #sort
			df = df[df['lat'] != temp.iloc[0]['lat']] #remove chosen point
			temp = temp.iloc[:-1 , :]#drop 1 from temp, does not matter which
		
		#deserialize points
		route = temp.iloc[0]
		route = route['points']
		route = deserialize(route)
		
		#generate names
		names = ['origin']
		for point in route:
			names.append(original[original['string_index'] == point].iloc[0]['amenity'])
		names.append('destination')
		
		#get lat/lon from points
		nodes = [(origin[0] , origin[1])]
		for point in route:
			lat = (original[original['string_index'] == point].iloc[0]['lat'])
			lon = (original[original['string_index'] == point].iloc[0]['lon'])
			nodes.append((lat, lon)) #note: this is backwards, don't know how they got reversed, but this works
		nodes.append((destination[0] , destination[1]))
		
		#create routes for ox
		route = []
		for i in range(len(nodes) - 1):
			origin1 = ox.nearest_nodes(G,nodes[i][1], nodes[i][0])
			destination1 = ox.nearest_nodes(G,nodes[i+1][1], nodes[i+1][0])
			route.append(nx.shortest_path(G,origin1,destination1,weight='length'))
		routes.append(route)
		
		#folium starts here
		node = nodes[0]
		m = folium.Map(location= node)
		route_map = folium.Map(location = node, width=1200, height=600)
		
		for i in range(len(nodes)):
			node = nodes[i]
			name = names[i]
			folium.Marker(node, popup=name).add_to(route_map)
		
		#add routes to folium map
		#note: no folium function exists to do all routes at once, so I must use a loop
		rc = ['red', 'green', 'blue', 'purple']
		for i in range(len(route)):
			ox.plot_route_folium(G, route[i], route_map = route_map, color=rc[route_num%len(rc)], opacity=0.5)

		route_map.save('./' + str(output) + '/route' + str(route_num + 1) + '.html')
		route_num = route_num + 1
	
	#return routes
	return routes
	
#TO RUN: python3 route.py landmarks_data.csv graph.osm 49.26348236022651 -123.20673804503969 49.26751502457303 -123.07181219914847 output 5 1.5 5
def route(df_file, G_file, origin_lat, origin_lon, destination_lat, destination_lon, output, num_points, max_distance_mod, num_routes):
	#load files
	df = pd.read_csv(df_file)
	G = ox.graph_from_xml(G_file)

	#remove unneeded data: this could be done sooner?
	df = df.drop(columns=['timestamp','tags', 'num_tags'])
	
	#need to do this for serializing
	df['string_index'] = df.apply(lambda row : ConvertToString(row['index']), axis = 1)
	
	#get location and destination from input
	origin = float(origin_lat),float(origin_lon)
	destination = float(destination_lat),float(destination_lon)
		
	#make 'routes' = vector of routes
	routes = get_route(df, origin, destination,G, output,num_points,max_distance_mod,num_routes)

#TO RUN: python3 route.py landmarks_data.csv graph.osm 49.26348236022651 -123.20673804503969 49.26751502457303 -123.07181219914847 output 5 1.5 5
def main():
	#get input
	df_file = sys.argv[1]
	G_file = sys.argv[2]
	
	origin_lat = float(sys.argv[3])
	origin_lon = float(sys.argv[4])
	destination_lat = float(sys.argv[5])
	destination_lon = float(sys.argv[6])

	output = sys.argv[7]

	num_points = int(sys.argv[8])
	max_distance_mod = float(sys.argv[9])
	num_routes = int(sys.argv[10])
		
	#begin program
	route(df_file, G_file, origin_lat, origin_lon, destination_lat, destination_lon, output, num_points, max_distance_mod, num_routes)
	
#TO RUN: python3 route.py landmarks_data.csv graph.osm 49.26348236022651 -123.20673804503969 49.26751502457303 -123.07181219914847 output 5 1.5 5
if __name__ == '__main__':
	main()






