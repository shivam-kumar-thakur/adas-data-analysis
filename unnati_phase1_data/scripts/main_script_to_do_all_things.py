import pandas as pd
import math
import functions_needed

def weekname(date):
    # Define a list of weekday names
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Get the day of the week as an integer (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    day_of_week = weekday_names[date.weekday()]
    return day_of_week

def alert_conc_with_hours():
    warn = ["data seperated on collisions\cas_fcw.csv", "data seperated on collisions\cas_hmw.csv",
            "data seperated on collisions\cas_ldw.csv", "data seperated on collisions\cas_pcw.csv"]

    # to create csv files based on timind and concenteration of co-ordinates.
    for i in warn:
        name = i[(i.find("\\") + 1):] + "data_conc_with_time" + ".csv"
        data_conc_with_time = functions_needed.generate_unique_coordinate_for_time(i)
        data_conc_with_time.to_csv(name, index=False)


def alert_conc_with_weekday():
    alerts_seperated_on_weekdays = ["alert seperated on collison with weekdays/cas_fcw.csv",
                                    "alert seperated on collison with weekdays/cas_hmw.csv",
                                    "alert seperated on collison with weekdays/cas_ldw.csv",
                                    "alert seperated on collison with weekdays/cas_pcw.csv"]
    for i in alerts_seperated_on_weekdays:
        name = i[(i.find("\\") + 1):] + "data_conc_with_time" + ".csv"
        data_conc_with_time = functions_needed.generate_unique_coordinate_for_weekday(i)
        data_conc_with_time.to_csv(name, index=False)

def add_places_count_in_conc_alerts():
    # To add count of Chennai data in each concentration
    datasets = [r"alert seperated on collision with week days concenterated points/cas_fcw.csv",
                r"alert seperated on collision with week days concenterated points/cas_hmw.csv",
                r"alert seperated on collision with week days concenterated points/cas_ldw.csv",
                r"alert seperated on collision with week days concenterated points/cas_pcw.csv"]

    for dataset_file in datasets:
        df = pd.read_csv(dataset_file)
        print(" Now we will add all counts of specific places around 1km area from points.")
        print("we are adding all the datas count on ", dataset_file)
        df['Chennai_colleges'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates\chennai+colleges.csv", 1.000),
            axis=1)
        df['Chennai_hotels'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/chennai_hotels.csv", 1.000),
            axis=1)
        df['Chennai_schools'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/education+chennai.csv", 1.000),
            axis=1)
        df['Chennai_hospitals'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/hospitalschennai.csv", 1.000),
            axis=1)
        df['Chennai_markets'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/markets+and+bazars.csv", 1.000),
            axis=1)
        df['Chennai_transport_stand'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/public+transport+stand.csv",
                                 1.000), axis=1)
        df['Chennai_religious_places'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/religious+places+chennai.csv",
                                 1.000), axis=1)
        df['Chennai_tourist_places'] = df.apply(
            lambda row: functions_needed.count_it(row['Lat'], row['Long'], "chennai data co-ordinates/tourist-places.csv", 1.000),
            axis=1)
        df.to_csv(dataset_file[(dataset_file.find("\\") + 1):], index=False)
        print("Data adding completed in ", dataset_file)

def to_add_weekday_in_dates():
    warn = ["data seperated on collisions\cas_fcw.csv", "data seperated on collisions\cas_hmw.csv",
            "data seperated on collisions\cas_ldw.csv", "data seperated on collisions\cas_pcw.csv"]
    for i in warn:
        name = i[(i.find("\\") + 1):]
        df = pd.read_csv(i)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Weekday"] = df.apply(lambda row: weekname(row["Date"]), axis=1)
        df.to_csv(name, index=False)


if __name__ == "__main__":
    arr=["1. to_add_weekday_in_dates","2. alert_conc_with_weekday","3. alert_conc_with_hours","4. add_places_count_in_conc_alerts"]
    print("These tasks can be perform using this script .")
    for i in range(4):
        print(arr[i])
    while 1:
        choice = int(input("Enter your choice 1,2,3,4 or 0 to exit"))
        if choice==0:
            break
        elif choice == 1:
            to_add_weekday_in_dates()
        elif choice == 2:
            alert_conc_with_weekday()
        elif choice == 3:
            alert_conc_with_hours()
        elif choice == 4:
            add_places_count_in_conc_alerts()



