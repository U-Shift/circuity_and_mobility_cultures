#!python
"""
#
# @file: 05-simulate_routes.py
# @version: see __version__
# @created: 2022-03-22
# @author: mncosta
# @brief: simulate routes using openrouteservice between two points
# ---
# @website:
# @repo:
# Description goes here
# ---
"""
__version__ = "v0.00.00 | 2022-03-22"


import argparse
import folium
import geojson
from math import radians
import ntpath
import openrouteservice as ors
import os
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from tqdm import tqdm, trange


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

ors_profiles = [
    'driving-car',
    'foot-walking',
    'cycling-regular',]

color_dict = {
    'driving-car': '#FF643C',
    'foot-walking': '#328BCF',
    'cycling-regular': '#45B747',
}


class ORS(object):
    def __init__(self, server_addr=None, ors_key=None, profiles=ors_profiles):
        self.profiles = profiles
        if server_addr is None:
            self.server = ors.Client(key=ors_key)
        else:
            self.server = ors.Client(base_url=server_addr)

    def compute_route(self, profile, coordinates):
        route = self.server.directions(
            coordinates=coordinates,
            profile=profile,
            format='geojson',
            extra_info=["steepness", "suitability", "surface", "waycategory", "waytype", "tollways", "traildifficulty",
                        "osmid", "roadaccessrestrictions", "countryinfo", "green", "noise"],
            validate=False)
        try:
            route_distance = route['features'][0]['properties']['summary']['distance']
            route_duration = route['features'][0]['properties']['summary']['duration']
        except:
            route_distance = 0
            route_duration = 0

        # print(profile, '\n==Distance:', route_distance, '\n==Duration:', route_duration, '\n')

        return route, route_distance, route_duration

    def compute_haversine_distance(self, point_a, point_b):
        """Computes the Haversine (Great Circle) distance between pointA and pointB."""

        point_a_in_radians = [radians(_) for _ in point_a]
        point_b_in_radians = [radians(_) for _ in point_b]
        result = haversine_distances([point_a_in_radians, point_b_in_radians])
        result = result * 6371000 / 1000  # to get km

        return result[0, 1]


def read_points(file):
    if not os.path.exists(file):
        print('File {} does not exist to read points from. Please recheck the file\'s path'.format(file))
    points = []

    data = pd.read_csv(file, index_col=0)
    # data['point_A'] = data['point_A'].str[1:-1].str.split(", ").apply(lambda x: (list(map(float, x))))
    # data['point_B'] = data['point_B'].str[1:-1].str.split(", ").apply(lambda x: (list(map(float, x))))

    #with trange(data.shape[0]) as t:
    #    for i in t:
    #        point_a = [data['Latitude_A'], data['Longitude_A']] #data['point_A'][i]
    #        point_b = [data['Latitude_B'], data['Longitude_B']] #data['point_B'][i]

    #        points.append([point_a, point_b])

    points = data.values.tolist()
            
    center_lat = data['Latitude_A'].mean()
    center_lon = data['Longitude_A'].mean()

    return points, center_lat, center_lon


def create_dir(dirpath):
    try:
        os.mkdir(dirpath)
    except Exception:
        pass


def setup_arguments():
    parser = argparse.ArgumentParser(
        prog='',
        description=''
    )
    parser.add_argument('--output_dir', type=str, required=True,
                        help='')
    parser.add_argument('--input_points', type=str, required=True,
                        help='')

    return parser.parse_args()


def main():
    print("--- ORS Simulate Routes |", __version__, "---")

    args = setup_arguments()
    print('')

    # we use a local server for ORS
    server_addr = 'http://10.0.28.126:10020/ors'

    dataset = os.path.splitext(ntpath.basename(args.input_points))[0].split('_')[1]
    print(color.BOLD + 'Dataset:' + color.END, dataset, '\n')

    output_dir = os.path.join(args.output_dir, dataset.lower())
    print('Writing output to: {}'.format(output_dir))
    create_dir(args.output_dir)
    create_dir(output_dir)
    create_dir(os.path.join(output_dir, 'routes'))
    create_dir(os.path.join(output_dir, 'maps'))

    print('Reading previous selected points\n')
    points, center_lat, center_lon = read_points(args.input_points)

    print('Connecting to ORS server\n')
    ors_obj = ORS(server_addr=server_addr)

    print('Creating output pd.Dataframe\n')
    columns = ['point_A', 'point_B', 'haversine_dist']
    for profile in ors_profiles:
        columns.append(profile + '_dist')
        columns.append(profile + '_time')
    data = pd.DataFrame(columns=columns)

    print('Iterating over points...')

    with trange(len(points)) as t:
        for i in t:
            t.set_description('Point %i' % (i + 1))

            m = folium.Map(location=[center_lat, center_lon].copy()[::-1], tiles='cartodbpositron', zoom_start=13)

            point_a = points[i][0:2]
            point_b = points[i][2:4]
            
            coordinates = [point_a, point_b]
            data_row = {'point_A': point_a, 'point_B': point_b}

            for profile in ors_profiles:
                try:
                    route, route_distance, route_duration = ors_obj.compute_route(profile, coordinates)
                    data_row[profile + '_dist'] = route_distance
                    data_row[profile + '_time'] = route_duration
                    # folium.PolyLine(locations=[list(reversed(coord))
                    #                            for coord in route['features'][0]['geometry']['coordinates']],
                    #                 color=color_dict[profile]).add_to(m)

                    # Save routes
                    route_file = os.path.join(output_dir, 'routes', str(i) + '_' + profile + '.geojson')
                    with open(route_file, 'w') as f:
                        geojson.dump(route, f)

                except ors.exceptions.ApiError:
                    continue

            data_row['haversine_dist'] = ors_obj.compute_haversine_distance(coordinates[0].copy()[::-1], coordinates[-1].copy()[::-1])

            data = data.append(data_row, ignore_index=True, sort=False)

            # Save maps
            # m.save(os.path.join(output_dir, 'maps', 'map_{}.html'.format(i)))
            
    # Save final data
    data.to_csv(os.path.join(output_dir, 'data.csv'))
    print('Completed! File shape:', data.shape)


if __name__ == "__main__":
    main()

