import osmnx as ox

def create_graph(bbox):
	'''
	Function to create a NetworkX graph from coordinate bounding box.
    
	bbox: List of coordinates, [North, South, East, West]
	'''

	north, south, east, west = bbox

	# Create a graph from OSM within some bounding box.
	G = ox.graph_from_bbox(
		north, south, east, west, 
		network_type='walk', # "all_private", "all", "bike", "drive", "drive_service", "walk"
		simplify=False, 
		retain_all=False, 
		truncate_by_edge=False, 
		clean_periphery=True, 
		custom_filter=None)
	
	return G
	
if __name__=='main':
	
	# Create Graph
	bbox = [53.2763, 53.2691, -9.0456, -9.0644]	# Galway city
	galway = create_graph(bbox)

	ox.save_graphml(galway, 'galway.graphml')