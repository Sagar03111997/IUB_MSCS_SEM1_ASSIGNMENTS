#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: [(Ronakkumar Bhagchandani, rbhagcha , 2001077918), (Dwarakamai Mannemuddu, dwamanne, 2001096476), (Sagar Sahu, sdsahu, 2001078394)]
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#
import heapq
# !/usr/bin/env python3
import sys
import math



def get_route(start, end, cost):
    '''lets get information based on cost function'''

    def cost_function_get(cost_name, end, current_state, gps_data_dict, speed_max_lmt):
        if cost_name == 'segments':
            c_p, c_t, seg_counter, dist_counter, time_counter, del_counter = current_state
            return seg_counter + 1

        elif cost_name == 'distance':
            c_p, c_t, seg_counter, dist_counter, time_counter, del_counter = current_state
            source = c_p[-1]
            if source not in gps_data_dict.keys() or end not in gps_data_dict.keys():
                return 0

            cord_source = gps_data_dict.get(source)
            cord_destination = gps_data_dict.get(end)

            lat_source, long_source = cord_source
            lat_dest, long_dest = cord_destination

            # using euclidean algorithm
            covered_dist = math.sqrt(
                (float(lat_dest) - float(lat_source)) ** 2 + (float(long_dest) - float(long_source)) ** 2)
            return covered_dist + dist_counter

        elif cost_name == 'time':
            c_p, c_t, seg_counter, dist_counter, time_counter, del_counter = current_state
            source = c_p[-1]
            if source not in gps_data_dict.keys() or end not in gps_data_dict.keys():
                return 0

            cord_source = gps_data_dict.get(source)
            cord_destination = gps_data_dict.get(end)

            lat_source, long_source = cord_source
            lat_dest, long_dest = cord_destination

            # using euclidean algorithm
            dist = math.sqrt((float(lat_dest) - float(lat_source)) ** 2 + (float(long_dest) - float(long_source)) ** 2)
            time_covered = dist / speed_max_lmt
            return time_covered + time_counter

        elif cost_name == 'delivery':
            c_p, c_t, seg_counter, dist_counter, time_counter, del_counter = current_state
            source = c_p[-1]
            if source not in gps_data_dict.keys() or end not in gps_data_dict.keys():
                return 0

            cord_source = gps_data_dict.get(source)
            cord_destination = gps_data_dict.get(end)

            lat_source, long_source = cord_source
            lat_dest, long_dest = cord_destination

            # using euclidean algorithm
            dist = math.sqrt((float(lat_dest) - float(lat_source)) ** 2 + (float(long_dest) - float(long_source)) ** 2)
            time_covered = dist / speed_max_lmt

            return time_covered + del_counter

    '''Read Files'''
    # road segments
    segments_data = open('road-segments.txt', 'r')

    speed_lmt_lst = []
    segments_data_dict = {}
    # read each line and store into dictionary
    for data in segments_data.readlines():
        # split the string space wise
        temp_gps = data.split()

        # check if the key 'city' is in the dictionary else assign it with empty value
        source_city = temp_gps[0]
        destination_city = temp_gps[1]

        # for source city
        if segments_data_dict.get(source_city)==None:
            segments_data_dict[source_city] = {}

        # for destination city to source city
        if segments_data_dict.get(destination_city)==None:
            segments_data_dict[destination_city] = {}

        # source to destination
        segments_data_dict[source_city][destination_city] = (float(temp_gps[2]), float(temp_gps[3]), temp_gps[4])

        # get max speed limit hence creating a list
        speed_lmt_lst.append(float(temp_gps[3]))

        # even we are storing for destination to source
        # destination to source
        segments_data_dict[destination_city][source_city] = (float(temp_gps[2]), float(temp_gps[3]), temp_gps[4])



    # get max speed
    speed_maxi = max(speed_lmt_lst)

    # City GPS
    # read file
    gps_data = open('city-gps.txt','r')

    gps_data_dict = {}

    for data in gps_data.readlines():
        temp_data = data.split()
        gps_data_dict[temp_data[0]] = {float(temp_data[1]), float(temp_data[2])}



    '''Using Fringe to iterate over the cities'''
    # let assign a fringe list to iterate over to reach the goal state
    fringe_path = []

    # assign different cost value counter
    cost_seg_counter = 0
    cost_distance_counter = 0
    cost_time_counter = 0
    cost_delivery_counter = 0

    # current path and path taken
    current_path = [start]
    path_taken = []
    city_reached = []
    next_city_cost = {}


    fringe_path_initial = (current_path, path_taken, cost_seg_counter, cost_distance_counter, cost_time_counter,
                           cost_delivery_counter)
    # print(cost, end, fringe_path_initial,type(gps_data_dict), type(segments_data_dict), speed_maxi)
    cost_val = cost_function_get(cost, end, fringe_path_initial, gps_data_dict, speed_maxi)
    cost_temp = (cost_val, fringe_path_initial)
    heapq.heappush(fringe_path, cost_temp)

    # iterate over fringe
    while fringe_path:
        cost_val, (current_path, path_taken, cost_seg_counter, cost_distance_counter, cost_time_counter,
                   cost_delivery_counter) = heapq.heappop(fringe_path)

        if current_path[-1] == end:
            return {"total-segments": len(path_taken),
                    "total-miles": cost_distance_counter,
                    "total-hours": cost_time_counter,
                    "total-delivery-hours": cost_delivery_counter,
                    "route-taken": path_taken}

        if current_path[-1] not in city_reached:
            city_reached.append(current_path[-1])


        # attached cities
        attached_cities = segments_data_dict[current_path[-1]].keys()

        # to store the information about next city cost value
        next_city_cost[current_path[-1]] = cost_val

        # iterate over the cities to get the best path
        for c in attached_cities:
            miles, speed_c, highway_c = segments_data_dict[current_path[-1]][c]

            # using distance by speed formula to get time
            time_travel = miles/speed_c

            # check delivery speed limit stated in the question.
            if speed_c<50:
                distance = time_travel

            else:
                distance = time_travel + (time_travel + cost_time_counter) * 2 * math.tanh(miles / 1000)

            # updated cost functions value
            new_segment_temp = cost_seg_counter+1
            new_distance_temp = cost_distance_counter+miles
            new_time_temp = cost_time_counter+time_travel
            new_delivery_temp = cost_delivery_counter + distance

            # create new fringe after taking one step
            new_fringe = (current_path+[c], path_taken + [
                (str(c), str(highway_c) + " for " + str(miles) + " miles")
            ], new_segment_temp, new_distance_temp, new_time_temp, new_delivery_temp)

            # get the cost for the given selection.
            cost_val = cost_function_get(cost, end, new_fringe, gps_data_dict, speed_maxi)

            # if not visited
            if c not in city_reached:
                heapq.heappush(fringe_path, (cost_val, new_fringe))

            # if visited and not cost_function is not segment push the selected city details in the fringe for finding optimal path.
            else:
                if cost != 'segments' and cost_val < next_city_cost[c]:
                    heapq.heappush(fringe_path, (cost_val, new_fringe))
                    city_reached.remove(c)

    # if no route available return False.
    return False



# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
