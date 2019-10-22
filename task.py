import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Read the cvs file into a pandas df.
df = pd.read_csv('metro-bike-share-trip-data.csv', low_memory=False)

# Get first rows of the df to get an idea of how the df looks.
# print (df.head(10))

def get_description(df):
    '''This function helps with getting some info about the df'''
    print ("-------------------------Get descriptions--------------------------")
    # Get shape of the df.
    print ('total nr of rows is:', df.shape[0], '\ntotal nr of columns is:', df.shape[1])
    # Get ndarray of all column names.
    print ('The columns are:', df.columns.values)
    # Get datatypes for all the columns.
    print ('Data types across the columns are:', df.dtypes)
    # Get total nr of elements in df col*rows.
    print ('Total nr of elements in df col*row', df.size)
    # Get a short description of data from the df. exclude categorical fields.
    print(df.describe(include=['int64', 'float']))
get_description(df)


# Drop NaNs.
df = df.dropna(axis=0)
# print (df.shape)
# After removing all the missing values see the shape of the df ((97825, 16)).

# Search for duplicates.
df = df.drop_duplicates(keep='first')
#print(df.shape) # None found, the shape was still (97825, 16).

'''After inspecting the data I saw that there are max values of 0.00 for
Starting Station Longitude and 0.00 for Ending Station Longitude. This
seems faulty (get a bike somewhre in California and leave it in Greenwich).
These needed to be removed. They also increased the std on these columns
to about 2 degress. The Longitude needs to be beyond -118 (it's very
unlikely the Long of a station will be some >55 miles away)'''

df = df[df['Starting Station Longitude'] < -118]
df = df[df['Ending Station Longitude'] < -118]
print("df shape after cleaning and removing NaNs", df.shape) # Currently have 97765 rows.

# Check metrics on new df. Now the std on Longitude columns (Staring, Ending)
# are in normal parameters, max in beyond -118.
#print(df.describe(include=['int64', 'float'])) 



def get_averages(df):
    '''calculates average duration trip, the interval of latitude and longitude
    for starting and ending station and the number of different bikes.'''
    print ("-------------------------Get avg values--------------------------")
    # Calculate vg on Duration column.
    duration_avg = df.Duration.mean()
    # Get nr of bikes by unique ID.
    nr_of_bikes = df['Bike ID'].nunique()
    # Get avg of lat interval.
    lat_avg = (abs(df['Starting Station Latitude'] - df['Ending Station Latitude'])).mean()
    # Get avg of long interval.
    long_avg = (abs(df['Starting Station Longitude'] - df['Ending Station Longitude'])).mean()
   
    print ("Avg duration of a trip is:", duration_avg)
    print ("Avg latitude interval in abs value:", lat_avg)
    print ("Avg longitude interval in abs value:", long_avg)
    print ('Nr of bikes:', nr_of_bikes)
#get_averages(df)


def group_by(df):
   print ("-------------------------Group by and plot avg duration--------------------------")
   # Group data by Passholder Type. Get avg.
   dur_by_pass =  df.groupby("Passholder Type")['Duration'].mean()

   # Group data by Plan Duration Type. Get avg - it seems that duration
   # by Plan Duration and Passholder Type is the same thing.
   dur_by_plan =  df.groupby("Plan Duration")['Duration'].mean()

   # Group data by Trip Route Category. Get avg.
   dur_by_trip_cat = df.groupby("Trip Route Category")['Duration'].mean()

   # Group data by Trip Route Category and Plan Duraion combined. Divide by 60 to get time in mins and round to the closest int.
   dur_mixed =  (df.groupby(["Trip Route Category", "Passholder Type"])['Duration'].mean()/60).round()
   
   # Unstack the df to get a good plotting of avg duration of trip route cat by passholder type.
   dur_mixed.unstack().plot.bar(rot=0).set_axisbelow(True)

   #Set grid for plot.
   plt.grid(True, color='w')

   #Set background for plot.
   plt.gca().patch.set_facecolor('0.8')
   
   # Print values.
   print ("Avg duration by", dur_by_pass)
   print ("Avg duration by", dur_by_plan)
   print ("Avg duration by", dur_by_trip_cat)
   print ("Avg duration by", dur_mixed)

   # Plot figure.
   plt.show()
   '''I noticed that the recevied plt had another element for
   Passholder Type - Staff Anual - that doesn't seem to appear in my dataset.
   That's why I have left the plot with only 3 dimensions:
   Trip Route Category, Passholder Type, Duration, as the 4th one - Plan Duration,
   that does make sense in the given plot, seems redundant for my dataset'''

#group_by(df)

def walk_up_vs_one_way(df):
   print ("-------------------------Plot Trip Category counts by Passholder Type--------------------------")
   '''This function plot the graphic of the total nr of one-way/round-trip
   bikes related to Passholder Type. Interestingly enough, it seems that
   most of the round-trips are made by single-rides,
   not by those who have a monthly/yearly subscription'''
   dur_by_pass =  df.groupby(["Passholder Type", "Trip Route Category"])['Passholder Type'].count()
   dur_by_pass.unstack().plot.bar(rot=0).set_axisbelow(True)
   plt.grid(True, color='w')
   plt.gca().patch.set_facecolor('0.8')
   plt.show()
   
#walk_up_vs_one_way(df)



'''
These function might be usefull, but don't really make plotting material.

def bad_bike(df):
   #bikes with the biggest running time
   dur_by_pass =  df.groupby(["Bike ID"])['Duration'].mean()
   print (dur_by_pass.sort_values().tail())
#bad_bike(df)

def most_popular(df):
   #the most popular start stations
   popular = df.groupby("Starting Station ID")['Passholder Type'].count()
   print (popular.sort_values().tail(10))
#most_popular(df)

'''
#making some predictions regarding the Passholder Type using the Duration of the trip, Plan duration and trip route

