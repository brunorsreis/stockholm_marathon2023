#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gpxpy
import matplotlib.pyplot as plt

# Read the GPX file
gpx_file = open('Stockholm_Marathon_2023.gpx', 'r')
gpx = gpxpy.parse(gpx_file)


# Extract track data
tracks = gpx.tracks
if len(tracks) > 0:
    track = tracks[0]  # Assuming only one track in the GPX file
    segments = track.segments
    if len(segments) > 0:
        segment = segments[0]  # Assuming only one segment in the track
        points = segment.points

        # Extract latitude, longitude, elevation, and time data
        lats = [point.latitude for point in points]
        lngs = [point.longitude for point in points]
        elevations = [point.elevation for point in points]
        times = [point.time for point in points]

        # Visualize the data in different ways
        # Plotting the elevation profile
        #plt.figure(figsize=(10, 5))
        #plt.plot(times, elevations)
        #plt.xlabel('Time')
        #plt.ylabel('Elevation (m)')
        #plt.title('Elevation Profile')
        #plt.show()

        # Plotting the route on a map
        plt.figure(figsize=(8, 8))
        plt.plot(lngs, lats, color='blue')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Route on Map')
        plt.axis('equal')
        plt.show()

        # Scatter plot of elevation over distance
        distances = [point.distance_2d(points[i-1]) if i > 0 else 0 for i, point in enumerate(points)]
        plt.figure(figsize=(10, 5))
        plt.scatter(distances, elevations, s=5)
        plt.xlabel('Distance (m)')
        plt.ylabel('Elevation (m)')
        plt.title('Elevation Variation over Distance')
        plt.show()
    else:
        print('No segments found in the GPX file.')
else:
    print('No tracks found in the GPX file.')



# In[2]:


# Display information at each kilometer
total_distance = 0
prev_point = None
kilometer_count = 1

for point in points:
    if prev_point is not None:
        distance = point.distance_2d(prev_point)
        total_distance += distance

        if total_distance >= 1000:  # Check if the total distance is equal to or greater than 1 kilometer
            print("One kilometer reached - Kilometer", kilometer_count)
            print("Latitude:", point.latitude)
            print("Longitude:", point.longitude)
            print("Elevation:", point.elevation)
            print("Time:", point.time)
            print()  # Empty line for separation
            
            total_distance = 0  # Reset the total distance
            kilometer_count += 1  # Increment the kilometer count
            
    prev_point = point


# In[3]:


import gpxpy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Plot the GPS points
plt.scatter(lngs, lats, c='blue', alpha=0.5)

# Perform clustering for visualization
kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as desired
kmeans.fit(list(zip(lats, lngs)))

# Plot the cluster centers
plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 0], c='red', marker='x')

# Display the plot
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Visualization of GPS Points with Cluster Centers')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[4]:


# Establish a connection
import cx_Oracle
import os

# Set the environment variable for the wallet location
os.environ["TNS_ADMIN"] = "/Users/brunotechdatabasket/Downloads/Wallet_marathondb"

# Set the TNS entry in tnsnames.ora
with open(os.path.join(os.environ["TNS_ADMIN"], "tnsnames.ora"), "w") as tns_file:
    tns_file.write("ORACLEDB =\n"
                   "(DESCRIPTION =\n"
                   "  (ADDRESS = (PROTOCOL = TCPS)(HOST = adb.eu-stockholm-1.oraclecloud.com)(PORT = 1522))\n"
                   "  (CONNECT_DATA =\n"
                   "    (SERVER = DEDICATED)\n"
                   "    (SERVICE_NAME = g114b7e420dfb56_marathondb_tpurgent.adb.oraclecloud.com)\n"
                   "  )\n"
                   "  (SECURITY =\n"
                   "    (SSL_SERVER_DN_MATCH = YES)\n"
                   "  )\n"
                   ")\n")

# Set the SSL options in sqlnet.ora
with open(os.path.join(os.environ["TNS_ADMIN"], "sqlnet.ora"), "w") as sqlnet_file:
    sqlnet_file.write("WALLET_LOCATION =\n"
                      "  (SOURCE =\n"
                      "    (METHOD = FILE)\n"
                      "    (METHOD_DATA =\n"
                      "      (DIRECTORY = /Users/brunotechdatabasket/Downloads/Wallet_marathondb)\n"
                      "    )\n"
                      "  )\n")

# Test the connection using Oracle Wallet Manager
try:
    cx_Oracle.connect("/", mode=cx_Oracle.SYSDBA)
    print("Wallet connection test successful.")
except cx_Oracle.DatabaseError as e:
    print("Error occurred while testing wallet connection:", e)

# Establish a connection
connection = cx_Oracle.connect(
    "ADMIN",
    "yourpasswordhere",
    "ORACLEDB"
)

# Create a cursor
cursor = connection.cursor()

# Create a table (if necessary)
cursor.execute("CREATE TABLE marathon_data2023 (latitude NUMBER, longitude NUMBER, elevation NUMBER, time TIMESTAMP)")

# Insert data into the table
for point in points:
    cursor.execute("INSERT INTO marathon_data2023 VALUES (:1, :2, :3, :4)",
                   (point.latitude, point.longitude, point.elevation, point.time))

# Commit the changes
connection.commit()


# Select data from the table
cursor.execute("SELECT * FROM marathon_data2023")
result = cursor.fetchall()

# Print the selected data
for row in result:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()


# In[5]:


#Connection to Amazon Web Services (AWS) using Amazon RDS (Relational Database Service):
import pymysql

# Establish a connection
connection = pymysql.connect(host='your_host', user='your_user', password='your_password', db='your_database')

# Create a cursor
cursor = connection.cursor()

# Create a table (if necessary)
cursor.execute("CREATE TABLE marathon_data (latitude FLOAT, longitude FLOAT, elevation FLOAT, time TIMESTAMP)")

# Insert data into the table
for point in points:
    cursor.execute("INSERT INTO marathon_data VALUES (%s, %s, %s, %s)",
                   (point.latitude, point.longitude, point.elevation, point.time))

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()



# In[ ]:


#Connecting to Google Cloud Platform (GCP) using Cloud SQL (MySQL):

from google.cloud import bigquery

# Set up authentication credentials (if required)
# ...

# Establish a connection
client = bigquery.Client()

# Create a dataset (if necessary)
dataset_ref = client.create_dataset('my_dataset')

# Create a table
table_ref = dataset_ref.table('marathon_data')
schema = [
    bigquery.SchemaField('latitude', 'FLOAT'),
    bigquery.SchemaField('longitude', 'FLOAT'),
    bigquery.SchemaField('elevation', 'FLOAT'),
    bigquery.SchemaField('time', 'TIMESTAMP'),
]
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)

# Insert data into the table
rows_to_insert = []
for point in points:
    rows_to_insert.append({'latitude': point.latitude, 'longitude': point.longitude,
                           'elevation': point.elevation, 'time': point.time})
client.insert_rows(table, rows_to_insert)



# In[ ]:


#Microsoft Azure using Azure SQL Database:

import pyodbc

# Establish a connection
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=your_server;Database=your_database;UID=your_username;PWD=your_password')

# Create a cursor
cursor = connection.cursor()

# Create a table (if necessary)
cursor.execute("CREATE TABLE marathon_data (latitude FLOAT, longitude FLOAT, elevation FLOAT, time DATETIME)")

# Insert data into the table
for point in points:
    cursor.execute("INSERT INTO marathon_data VALUES (?, ?, ?, ?)",
                   (point.latitude, point.longitude, point.elevation, point.time))

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

