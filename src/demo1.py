from route import route

#TO RUN: python3 demo.py
def main():
	print("DEMO BEGIN: python3 route.py landmarks_data.csv graph.osm 49.26348236022651 -123.20673804503969 49.26751502457303 -123.07181219914847 output 5 1.5 5")
	route("landmarks_data.csv", "graph.osm", 49.26348236022651, -123.20673804503969, 49.26751502457303, -123.07181219914847, "output", 5, 1.5, 5)
	print("DEMO COMPLETE: CHECK OUTPUT FOLDER")
	


	

if __name__ == '__main__':
	main()




