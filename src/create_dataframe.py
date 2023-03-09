#old stuff
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler




#TO RUN: python3 create_dataframe.py amenities-vancouver.json.gz
def main():
	#get from file
	#osm_file = sys.argv[1]
	osm_file = "amenities-vancouver.json.gz"
	osm = pd.read_json(osm_file, lines=True)
	
	#remove amenities without tags
	osm = osm[osm['tags'].str.len() > 0]

	#sort by number of tags
	osm['num_tags'] = osm['tags'].str.len()
	osm = osm.sort_values(by=['num_tags'], ascending=False)
	
	#get just amenities with tag: tourism
	tourism = osm.copy(deep=True)
	tourism = tourism[tourism.tags.map(set(['tourism']).issubset)]
	osm = osm[~osm.isin(tourism)]
	
	#remove certain amenities (or separate into separate categories to find restaruants, bathroom, etc.)
	#definitely remove these
	osm = osm[osm['amenity'] != 'post_box']
	osm = osm[osm['amenity'] != 'telephone']
	osm = osm[osm['amenity'] != 'bench']
	osm = osm[osm['amenity'] != 'toilets']
	osm = osm[osm['amenity'] != 'vending_machine']
	osm = osm[osm['amenity'] != 'parking']
	osm = osm[osm['amenity'] != 'parking_entrance']
	osm = osm[osm['amenity'] != 'fuel']
	osm = osm[osm['amenity'] != 'bicycle_parking']
	osm = osm[osm['amenity'] != 'recycling']
	osm = osm[osm['amenity'] != 'waste_disposal']
	osm = osm[osm['amenity'] != 'car_wash']
	osm = osm[osm['amenity'] != 'dentist']
	osm = osm[osm['amenity'] != 'parking_space']
	osm = osm[osm['amenity'] != 'doctors']
	osm = osm[osm['amenity'] != 'waste_basket']
	osm = osm[osm['amenity'] != 'shelter']
	osm = osm[osm['amenity'] != 'clinic']	
	osm = osm[osm['amenity'] != 'atm']
	osm = osm[osm['amenity'] != 'bus_station']
	osm = osm[osm['amenity'] != 'kindergarten']
	osm = osm[osm['amenity'] != 'bicycle_rental']
	osm = osm[osm['amenity'] != 'drinking_water']
	osm = osm[osm['amenity'] != 'charging_station']
	osm = osm[osm['amenity'] != 'dojo']
	osm = osm[osm['amenity'] != 'car_rental']
	osm = osm[osm['amenity'] != 'car_sharing']
	osm = osm[osm['amenity'] != 'seaplane terminal']
	osm = osm[osm['amenity'] != 'bicycle_repair_station']
	osm = osm[osm['amenity'] != 'smoking_area']
	osm = osm[osm['amenity'] != 'locker']
	osm = osm[osm['amenity'] != 'letter_box']
	osm = osm[osm['amenity'] != 'veterinary']
	osm = osm[osm['amenity'] != 'prep_school']
	osm = osm[osm['amenity'] != 'bureau_de_change']
	osm = osm[osm['amenity'] != 'food_court']
	osm = osm[osm['amenity'] != 'animal_boarding']
	osm = osm[osm['amenity'] != 'police']
	osm = osm[osm['amenity'] != 'hospital']
	osm = osm[osm['amenity'] != 'loading_dock']
	osm = osm[osm['amenity'] != 'studio']
	osm = osm[osm['amenity'] != 'taxi']
	osm = osm[osm['amenity'] != 'music_school']
	osm = osm[osm['amenity'] != 'motorcycle_parking']
	osm = osm[osm['amenity'] != 'shower']
	osm = osm[osm['amenity'] != 'arts_centre']
	osm = osm[osm['amenity'] != 'stripclub']
	osm = osm[osm['amenity'] != 'vacuum_cleaner']
	osm = osm[osm['amenity'] != 'research_institute']
	osm = osm[osm['amenity'] != 'construction']
	osm = osm[osm['amenity'] != 'boat_rental']
	osm = osm[osm['amenity'] != 'healthcare']
	osm = osm[osm['amenity'] != 'social_centre']
	osm = osm[osm['amenity'] != 'conferance_centre']
	osm = osm[osm['amenity'] != 'karaoke_box']
	osm = osm[osm['amenity'] != 'compressed_air']
	osm = osm[osm['amenity'] != 'driving_school']
	osm = osm[osm['amenity'] != 'conference_centre']
	osm = osm[osm['amenity'] != 'family_centre']
	osm = osm[osm['amenity'] != 'sanitary_dump_station']
	osm = osm[osm['amenity'] != 'training']
	osm = osm[osm['amenity'] != 'parcel_locker']
	osm = osm[osm['amenity'] != 'motorcycle_rental']
	osm = osm[osm['amenity'] != 'bistro']
	osm = osm[osm['amenity'] != 'give_box']
	osm = osm[osm['amenity'] != 'language_school']
	osm = osm[osm['amenity'] != 'table']
	osm = osm[osm['amenity'] != 'animal_shelter']
	osm = osm[osm['amenity'] != 'money_transfer']
	osm = osm[osm['amenity'] != 'waste_basket;recycling']
	osm = osm[osm['amenity'] != 'animal_training']
	osm = osm[osm['amenity'] != 'dressing_room']
	osm = osm[osm['amenity'] != 'payment_terminal']
	osm = osm[osm['amenity'] != 'toy_library']
	osm = osm[osm['amenity'] != 'housing co-op']
	osm = osm[osm['amenity'] != 'EVSE']
	osm = osm[osm['amenity'] != 'vacuum']
	osm = osm[osm['amenity'] != 'first_aid']
	osm = osm[osm['amenity'] != 'hunting_stand']
	osm = osm[osm['amenity'] != 'internet_cafe']
	osm = osm[osm['amenity'] != 'cooking_school']
	osm = osm[osm['amenity'] != 'mortuary']
	osm = osm[osm['amenity'] != 'trash']
	osm = osm[osm['amenity'] != 'disused:restaurant']
	osm = osm[osm['amenity'] != 'ATLAS_clean_room']
	osm = osm[osm['amenity'] != 'workshop']
	osm = osm[osm['amenity'] != 'storage_rental']
	osm = osm[osm['amenity'] != 'laboratory']
	osm = osm[osm['amenity'] != 'nursing_home']
	osm = osm[osm['amenity'] != 'safety']
	osm = osm[osm['amenity'] != 'atm;bank']
	osm = osm[osm['amenity'] != 'ranger_station']
	osm = osm[osm['amenity'] != 'dive_centre']
	osm = osm[osm['amenity'] != 'waste_transfer_station']
	osm = osm[osm['amenity'] != 'post_office']
	osm = osm[osm['amenity'] != 'trolley_bay']
	osm = osm[osm['amenity'] != 'prison']
	osm = osm[osm['amenity'] != 'bear_box']
	osm = osm[osm['amenity'] != 'post_depot']
	osm = osm[osm['amenity'] != 'college']
	osm = osm[osm['amenity'] != 'fire_station']
	osm = osm[osm['amenity'] != 'weighbridge']

	#definitely don't remove
	#osm = osm[osm['amenity'] != 'fountain']
	#osm = osm[osm['amenity'] != 'public_building']
	#osm = osm[osm['amenity'] != 'theatre']
	#osm = osm[osm['amenity'] != 'clock']
	#osm = osm[osm['amenity'] != 'gambling']
	#osm = osm[osm['amenity'] != 'marketplace']	
	#osm = osm[osm['amenity'] != 'university']
	#osm = osm[osm['amenity'] != 'cinema']
	#osm = osm[osm['amenity'] != 'social_facility']
	#osm = osm[osm['amenity'] != 'binoculars']
	#osm = osm[osm['amenity'] != 'townhall']
	#osm = osm[osm['amenity'] != 'courthouse']
	#osm = osm[osm['amenity'] != 'lounge']
	#osm = osm[osm['amenity'] != 'lounger']
	#osm = osm[osm['amenity'] != 'water_point']
	#osm = osm[osm['amenity'] != 'Observation Platform']
	#osm = osm[osm['amenity'] != 'monastery']
	#osm = osm[osm['amenity'] != 'biergarten']
	
	#possibly remove these
	osm = osm[osm['amenity'] != 'public_bookcase']
	osm = osm[osm['amenity'] != 'restaurant']
	osm = osm[osm['amenity'] != 'bank']
	osm = osm[osm['amenity'] != 'fast_food']
	osm = osm[osm['amenity'] != 'bbq']
	osm = osm[osm['amenity'] != 'cafe']
	osm = osm[osm['amenity'] != 'pub']
	osm = osm[osm['amenity'] != 'ice_cream']
	osm = osm[osm['amenity'] != 'community_centre']
	osm = osm[osm['amenity'] != 'library']
	osm = osm[osm['amenity'] != 'ferry_terminal']
	osm = osm[osm['amenity'] != 'school']
	osm = osm[osm['amenity'] != 'bar']
	osm = osm[osm['amenity'] != 'pharmacy']
	osm = osm[osm['amenity'] != 'childcare']
	osm = osm[osm['amenity'] != 'nightclub']
	osm = osm[osm['amenity'] != 'place_of_worship']
	osm = osm[osm['amenity'] != 'meditation_centre']
	osm = osm[osm['amenity'] != 'spa']
	osm = osm[osm['amenity'] != 'hookah_lounge']
	osm = osm[osm['amenity'] != 'leisure']
	osm = osm[osm['amenity'] != 'events_venue']
	osm = osm[osm['amenity'] != 'playground']	
	osm = osm[osm['amenity'] != 'dance']
	osm = osm[osm['amenity'] != 'science']
	osm = osm[osm['amenity'] != 'casino']
	osm = osm[osm['amenity'] != 'lobby']
	
	#extract rows with wikidata or wikipedia
	#wikidata = osm.tags[osm.tags.map(set(['brand:wikidata']).issubset)]
	#wikidata = osm[osm.tags.map(set(['brand:wikidata']).issubset)]
	#wikipedia = osm[osm.tags.map(set(['brand:wikipedia']).issubset)]

	#add tourism tag rows
	osm = pd.concat([osm, tourism], ignore_index=True, sort=False)
	
	#reset index
	osm = osm[osm['lat'].notna()]
	osm = osm[osm['lon'].notna()]
	osm = osm.reset_index()
	osm = osm.set_index('index')
	
	#save
	osm.to_csv("landmarks_data.csv")

	#testing
	#print (osm)
	

if __name__ == '__main__':
	main()

