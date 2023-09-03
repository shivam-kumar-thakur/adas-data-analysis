import pandas as pd
import math
import datetime

# Function to calculate the haversine distance between two coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance in kilometers
    distance = R * c
    return distance


# Function to find the number of points within a certain distance for all unique coordinates
def specific_co_ordintes(list_of_unique_coordinates, distance_circle_in_km):
    store_each_coordinta_count = []  # [[lat, long], total_count_inside_given_distance, avg_speed]

    # Loop through each unique coordinate
    for i in range(len(list_of_unique_coordinates)):
        lat1, lon1, speed1 = list_of_unique_coordinates[i]
        count = 0
        speed_total = 0

        # Compare with other unique coordinates
        for j in range(len(list_of_unique_coordinates)):
            if i != j:  # Avoid comparing the same coordinates
                lat2, lon2, speed2 = list_of_unique_coordinates[j]

                # Check if the haversine distance is within the given circle distance
                if haversine_distance(lat1, lon1, lat2, lon2) <= distance_circle_in_km:
                    count = count + 1
                    speed_total = speed_total + speed2

        # Calculate average speed and store information
        avg_speed = speed_total / count if count > 0 else 0  # Handle divide by zero
        store_each_coordinta_count.append([[lat1, lon1], count, round(avg_speed)])

    return store_each_coordinta_count

def specific_points(co_ordinates_count, reverse_value, sort_on_basis, circle_radius_in_km):
    # Sort coordinates based on criteria
    sorted_co_ordinates = sorted(co_ordinates_count, key=lambda x: x[sort_on_basis], reverse=reverse_value)
    final_specific_points = []

    if len(sorted_co_ordinates) != 0:
        for i in range(0, len(sorted_co_ordinates)):
            if i == 0:
                # For the first coordinate, calculate the count of coordinates within the circle radius
                accurate_count = 0
                lat2, lon2=sorted_co_ordinates[0][0]
                for j in range(0, len(sorted_co_ordinates)):
                    # Get the latitude and longitude of the current coordinate
                    latnow, lonnow =sorted_co_ordinates[j][0]

                    # Check if the haversine distance is within the given circle distance
                    if haversine_distance(lat2, lon2, latnow, lonnow) <= circle_radius_in_km:
                        accurate_count = accurate_count + 1

                # Update the count in the first coordinate
                sorted_co_ordinates[i][1] = accurate_count

                # Store the first element in final_specific_points
                final_specific_points = [sorted_co_ordinates[0]]

            else:
                # For subsequent coordinates, check if it's outside the circle radius from all points in final_specific_points
                store_data2 = sorted_co_ordinates[i]
                lat2, lon2 = store_data2[0]

                # Initialize a flag to check if the current coordinate is within the circle radius from any point in final_specific_points
                flag = True

                for j in final_specific_points:
                    lat1, lon1 = j[0]

                    # If the distance between two points is less than the circle radius, set the flag to False
                    if (haversine_distance(lat1, lon1, lat2, lon2) < circle_radius_in_km):
                        flag = False

                # If the flag is True, calculate the accurate count for the current coordinate
                if flag:
                    accurate_count = 0
                    for j in range(0, len(sorted_co_ordinates)):
                        store_data_inside = sorted_co_ordinates[i]
                        if i != j:
                            latnow, lonnow = sorted_co_ordinates[j][0]

                            # Check if the haversine distance is within the given circle distance
                            if haversine_distance(lat2, lon2, latnow, lonnow) <= circle_radius_in_km:
                                accurate_count = accurate_count + 1

                    # Update the count in the current coordinate
                    sorted_co_ordinates[i][1] = accurate_count

                    # Add the current coordinate to final_specific_points
                    final_specific_points.append(sorted_co_ordinates[i])

        return final_specific_points


# Function to convert selected coordinates to a DataFrame
def coordinate_dataframe(specific_points_coordinaes):
    data = pd.DataFrame(columns=["Lat", "Long", "Count", "Avg_speed"])

    # Loop through selected coordinates
    for i in range(len(specific_points_coordinaes)):
        cordinate, count, avg_speed = specific_points_coordinaes[i]
        lat, long = cordinate  # Extract latitude and longitude from the list
        data.loc[i] = [lat, long, count, avg_speed]  # Add data to DataFrame

    return data

def coordinate_dataframe_diff_time(specific_points_coordinaes,time_hour):
    data = pd.DataFrame(columns=["Time_hour","Lat", "Long", "Count", "Avg_speed"])

    # Loop through selected coordinates, and also remove if count is 1, since 1 in 500 meters is nothing.
    for i in range(len(specific_points_coordinaes)):
        cordinate, count, avg_speed = specific_points_coordinaes[i]
        if count<2:
            continue
        lat, long = cordinate  # Extract latitude and longitude from the list
        data.loc[i] = [time_hour,lat, long, count, avg_speed]  # Add data to DataFrame

    return data

def coordinate_dataframe_diff_weekday(specific_points_coordinaes,weekday):
    data = pd.DataFrame(columns=["Weekday","Lat", "Long", "Count", "Avg_speed"])

    # Loop through selected coordinates, and also remove if count is 0, since just one point  in 500 meters is nothing.
    for i in range(len(specific_points_coordinaes)):
        cordinate, count, avg_speed = specific_points_coordinaes[i]
        if count<1:
            continue
        lat, long = cordinate  # Extract latitude and longitude from the list
        data.loc[i] = [weekday,lat, long, count, avg_speed]  # Add data to DataFrame

    return data

def extract_hour(time_str):
    return int(time_str.split(':')[0])

def generate_unique_coordinate_for_time(address):
    # Read the CSV file into a DataFrame
    print("Currently working on : ", address)
    df = pd.read_csv(address, dtype={'Lat': float, 'Long': float})
    df["Time"] = df['Time'].apply(extract_hour)
    print(df)
    data_conc_with_time=pd.DataFrame(columns=["Time_hour","Lat", "Long", "Count", "Avg_speed"])
    for i in range(23):
        data = df[(df["Time"] >= i) & (df["Time"] < (i + 1))]
        total_warnings = data.shape[0]
        print("total warnigs from ", i, " to ", i + 1, " = ", total_warnings)
        if total_warnings:
            # Find unique coordinates and calculate average speed
            unique = data[['Lat', 'Long']].drop_duplicates()
            arr_to_store_unique_coord_with_avgspeed = []

            for index, row in unique.iterrows():
                lat = row['Lat'].round(8)
                long = row['Long'].round(8)

                matching_rows = data[(data['Lat'] == lat) & (data['Long'] == long)]
                avg_speed = matching_rows['Speed'].mean()
                arr_to_store_unique_coord_with_avgspeed.append([lat, long, avg_speed])

            # Calculate specific coordinates within a certain distance and their statistics
            co_ordinates_count = specific_co_ordintes(arr_to_store_unique_coord_with_avgspeed, 0.500)

            # Select specific points based on criteria
            specific_points_coordinaes = specific_points(co_ordinates_count, True, 1, 0.500)

            # Convert selected points to a DataFrame, with time also
            final_data = coordinate_dataframe_diff_time(specific_points_coordinaes,i)
            final_data_sorted = final_data.sort_values(by='Count', ascending=False)

            data_conc_with_time=pd.concat([data_conc_with_time,final_data_sorted],ignore_index=True)

    return data_conc_with_time

def generate_unique_coordinate_for_weekday(address):
    # Read the CSV file into a DataFrame
    print("Currently working on : ", address)
    df = pd.read_csv(address, dtype={'Lat': float, 'Long': float})
    df["Time"] = df['Time'].apply(extract_hour)
    print(df)
    data_conc_with_time=pd.DataFrame(columns=["Weekday","Lat", "Long", "Count", "Avg_speed"])
    # Define a list of weekday names
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in weekday_names:
        data = df[df["Weekday"]==i]
        total_warnings = data.shape[0]
        print("Working on total warning on ",i," it is nearly ",total_warnings)
        if total_warnings:
            # Find unique coordinates and calculate average speed
            unique = data[['Lat', 'Long']].drop_duplicates()
            arr_to_store_unique_coord_with_avgspeed = []

            for index, row in unique.iterrows():
                lat = row['Lat'].round(8)
                long = row['Long'].round(8)

                matching_rows = data[(data['Lat'] == lat) & (data['Long'] == long)]
                avg_speed = matching_rows['Speed'].mean()
                arr_to_store_unique_coord_with_avgspeed.append([lat, long, avg_speed])

            # Calculate specific coordinates within a certain distance and their statistics
            co_ordinates_count = specific_co_ordintes(arr_to_store_unique_coord_with_avgspeed, 0.500)

            # Select specific points based on criteria
            specific_points_coordinaes = specific_points(co_ordinates_count, True, 1, 0.500)

            # Convert selected points to a DataFrame, with time also
            final_data = coordinate_dataframe_diff_weekday(specific_points_coordinaes,i)
            final_data_sorted = final_data.sort_values(by='Count', ascending=False)

            data_conc_with_time=pd.concat([data_conc_with_time,final_data_sorted],ignore_index=True)

    return data_conc_with_time


def count_it(Lat,Long,area_coordinates_csv,distance_in_km):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(area_coordinates_csv, dtype={'Lat': float, 'Long': float})
    # Find unique coordinates and calculate average speed
    unique = df[['Lat', 'Long']].drop_duplicates()
    count=0
    for index, row in unique.iterrows():
        lat1 = row['Lat'].round(8)
        long1 = row['Long'].round(8)
        if haversine_distance(lat1, long1, Lat, Long)<=distance_in_km:
            count=count+1
    return count

if __name__=="__main__":
    pass