import fiona as fi
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime as dt
from math import radians, cos, sin, asin, sqrt

class GpxReader():
    """
    Read information from GPX file. 


    """

    def __init__(self,gpx_file):
        self.df = self.__parse_gpx(gpx_file)

    def __parse_gpx(self,path):
        """
        Reads all track point from a gpx file of which the path is given.
        Returns a data frame with: time(index), longitude, latitude, altitude, distance, speed
        Distance is calculated using the haversine function.
        
        path: path to the gpx file.
        """
        track_points = fi.open(path, layer='track_points')
        numpoints = len(list(track_points))
        data = []         # initialize two-dim. list
        for point in track_points:
            data.append([float(point['geometry']['coordinates'][0]),\
                        float(point['geometry']['coordinates'][1]),\
                        float(point['properties']['ele']),\
                        dt.strptime(point['properties']['time'], "%Y-%m-%dT%H:%M:%S"),\
                        np.nan,\
                        np.nan,
                        np.nan])
            if (len(data) > 1):
                idx = len(data)-1
                data[idx][4]=self.__haversine(data[idx][0],data[idx][1],data[idx-1][0],data[idx-1][1])
                data[idx][6]=(data[idx][3]-data[idx-1][3]).seconds
                data[idx][5]=3600*data[idx][4]/data[idx][6]
                
                
        df_gpx = pd.DataFrame(data,columns=['lon', 'lat', 'alt', 'time', 'dist', 'speed','dtim'])
        df_gpx = df_gpx.set_index("time") 
        return df_gpx

    def __haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6372.800  #6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

def main():

    home = str(Path.home())
    path = home + r'/Documents/gpx/2021-01-15 12.02.26 Day.gpx'
    gpx = GpxReader(path)


if __name__ == "__main__":
    main()