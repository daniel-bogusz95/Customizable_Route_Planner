from route import route

#TO RUN: python3 demo2.py
def main():
	print("DEMO BEGIN: python3 route.py landmarks_data.csv graph.osm 49.26386617578784 -123.2165250570788 49.24324979357316 -123.06820962360176 output 3 1.5 3")
	route("landmarks_data.csv", "graph.osm", 49.26386617578784, -123.2165250570788, 49.24324979357316, -123.06820962360176, "output", 3, 1.5, 3)
	print("DEMO COMPLETE: CHECK OUTPUT FOLDER")
	
	

if __name__ == '__main__':
	main()

