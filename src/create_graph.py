import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.pyplot as plt

#new
import osmnx as ox
import networkx as nx
import folium

#adapted from https://stackoverflow.com/questions/60578408/is-it-possible-to-draw-paths-in-folium
#folium syntax/guide https://python-visualization.github.io/folium/quickstart.html
#https://snyk.io/advisor/python/osmnx/functions/osmnx.get_nearest_node
#https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=nearest_node#osmnx.distance.nearest_nodes
#https://osmnx.readthedocs.io/en/stable/osmnx.html#module-osmnx.folium

#TO RUN: python3 create_graph.py
def main():

	ox.settings.log_console=True
	ox.settings.use_cache=True
	G = ox.graph_from_place('Vancouver, British Columbia, Canada',network_type='walk') #assumes walking, can change # save this ahead of time? takes a minute to create Graph
	
	#create graph
	ox.save_graph_xml(G, filepath='./graph.osm')
	

if __name__ == '__main__':
	main()



















	# test multiple routes
	#fig, ax = ox.plot_graph_routes(G, [route, route])
	
