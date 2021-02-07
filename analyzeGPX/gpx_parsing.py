import fiona as fi
import pandas as pd
import numpy as np
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import os
import csv
#from geopy import distance
#from shapely.geometry import shape
#import geopandas as gpd


def main():
    path = '/media/peterad/GARMIN/Garmin/GPX/Archive/' #'/home/peter/Documents/gpx/'
    analyse_gpx(path,'/home/peterad/Documents/report.csv' )
    # filename = '2020-09-06 08.23.15 Day.gpx'#'2020-06-23 17.53.34 Day.gpx' #'2020-06-05 06.53.50 Day.gpx'
    # fn = "2019-09-04 07.02.30 Day.gpx"
    # fname = path + fn
    # data = parse_gpx(fname)
    # data = data.drop(data.loc[data['dist'] >= 0.3].index, axis=0)
    # tot_dst = data['dist'].sum()              
    # tot_time = (data.index[-1] - data.index[0]).seconds
    # mv_time = data.loc[data['speed'] > 5,'dtim'].sum()
    # av_spd = 3600*data['dist'].sum()/data['dtim'].sum()
    # mv_spd = 3600*data.loc[data['speed'] > 5,'dist'].sum()/mv_time
    # g40 = data.loc[data['speed']>=40,'dist'].sum()
    # t35_40 = data.loc[((data['speed']>=35)&(data['speed']<40)),'dist'].sum()
    # t30_35 = data.loc[((data['speed']>=30)&(data['speed']<35)),'dist'].sum()
    # t25_30 = data.loc[((data['speed']>=25)&(data['speed']<30)),'dist'].sum()
    # t20_25 = data.loc[((data['speed']>=20)&(data['speed']<25)),'dist'].sum()
    # t15_20 = data.loc[((data['speed']>=15)&(data['speed']<20)),'dist'].sum()
    # t10_15 = data.loc[((data['speed']>=10)&(data['speed']<15)),'dist'].sum()
    # l10 = data.loc[data['speed']<10,'dist'].sum()
    # print(fn.split('.g')[0], tot_dst,sec_to_hms(tot_time),\
    #     sec_to_hms(mv_time),av_spd,mv_spd,
    #     g40,t35_40,t30_35,t25_30,t20_25,t15_20,t10_15,l10)
    

def sec_to_hms(t):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return str(int(h))+':'+str(int(m))+':'+str(int(s))

def haversine(lon1, lat1, lon2, lat2):
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

def analyse_gpx(path,outputfile):
    files = [fn for fn in os.listdir(path)
              if fn.endswith('.gpx')]
    outputdf = None
    if os.path.isfile(outputfile):
        outputdf = pd.read_csv(outputfile, index_col=0)
    else:
        outputdf = pd.DataFrame(columns=['gpx', 'distance', 'tot_tim', 'mov_time',\
            'avg_speed_ov','avg_speed_mo','>40km/h','35-40km/h','30-35km/h','25-30km/h',\
            '20-25km/h','15-20km/h','10_15km/h','<10km/h']) 
    # with open(outputfile, 'w') as csvfile:
        # filewriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # filewriter.writerow(['gpx', 'distance', 'tot_tim', 'mov_time','avg_speed_ov',\
        #     'avg_speed_mo','>40km/h','35-40km/h','30-35km/h','25-30km/h','20-25km/h',\
        #     '15-20km/h','10_15km/h','<10km/h'])
    outputdata = []         # initialize two-dim. list
    for fn in files:
        #print (fn)
        name = fn.split('.g')[0]
        if (name not in outputdf['gpx'].values):
            fname = path + fn
            data = parse_gpx(fname)
            data = data.drop(data.loc[data['dist'] >= 0.3].index, axis=0)
            tot_dst = data['dist'].sum()              
            tot_time = (data.index[-1] - data.index[0]).seconds
            mv_time = data.loc[data['speed'] > 5,'dtim'].sum()
            av_spd = 3600*data['dist'].sum()/data['dtim'].sum()
            mv_spd = 3600*data.loc[data['speed'] > 5,'dist'].sum()/mv_time
            g40 = data.loc[data['speed']>=40,'dist'].sum()
            t35_40 = data.loc[((data['speed']>=35)&(data['speed']<40)),'dist'].sum()
            t30_35 = data.loc[((data['speed']>=30)&(data['speed']<35)),'dist'].sum()
            t25_30 = data.loc[((data['speed']>=25)&(data['speed']<30)),'dist'].sum()
            t20_25 = data.loc[((data['speed']>=20)&(data['speed']<25)),'dist'].sum()
            t15_20 = data.loc[((data['speed']>=15)&(data['speed']<20)),'dist'].sum()
            t10_15 = data.loc[((data['speed']>=10)&(data['speed']<15)),'dist'].sum()
            l10 = data.loc[data['speed']<10,'dist'].sum()
            outputdata.append([fn.split('.g')[0], tot_dst,sec_to_hms(tot_time),\
                                sec_to_hms(mv_time),av_spd,mv_spd,\
                                g40,t35_40,t30_35,t25_30,t20_25,t15_20,t10_15,l10])
    newdf = pd.DataFrame(outputdata, columns=['gpx', 'distance', 'tot_tim', 'mov_time',\
            'avg_speed_ov','avg_speed_mo','>40km/h','35-40km/h','30-35km/h','25-30km/h',\
            '20-25km/h','15-20km/h','10_15km/h','<10km/h']) 
 
    outputdf = outputdf.append(newdf).reset_index(drop=True)
    outputdf.to_csv(outputfile)
        # print ("Totale afstand : {} km".format(data['dist'].sum()))
        # overallsnelheid = 3600*data['dist'].sum()/data['dtim'].sum()
        # beweegtijd = data.loc[data['speed'] > 5,'dtim'].sum()
        # beweegsnelheid = 3600*data.loc[data['speed'] > 5,'dist'].sum()/beweegtijd
        # print ("Gemiddelde snelheid, overall: {} km/u, bewogen : {} km/u".\
        #         format(overallsnelheid, beweegsnelheid)) 
        # dt =  #(data.iloc[-1].index.dt - data.iloc[0].index.dt).seconds

        # print ("Verstreken tijd: {} uur, beweegtijd: {}".format(dt,beweegtijd/3600)) 
        # meerdan35 = data.loc[data['speed']>35,'dist'].sum()
        # meerdan30 = data.loc[((data['speed']>30)&(data['speed']<=35)),'dist'].sum()
        # meerdan25 = data.loc[((data['speed']>25)&(data['speed']<=30)),'dist'].sum()
        # langzaam = data.loc[data['speed']<=25,'dist'].sum()
        # print("{} km > 35, {} km > 30km/u, {} km > 25km/u, {} km langzaam".\
        #       format(meerdan35, meerdan30,meerdan25,langzaam))

def open_gpx_track(path, layer='tracks'):
    """
    Opens a gpx file and returns a given layer.
    
    path: path to the gpx file
    layer: the layer in the gpx to open (default = 'tracks')
    Possible values for layer are: 'waypoints', 'routes', 'tracks', 'route_points', 'track_points'
    """
    #print(fi.listlayers(path))
    return fi.open(path, layer=layer)
    
def parse_gpx(path):
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
                    datetime.strptime(point['properties']['time'], "%Y-%m-%dT%H:%M:%S"),\
                    np.nan,\
                    np.nan,
                    np.nan])
        if (len(data) > 1):
            idx = len(data)-1
            data[idx][4]=haversine(data[idx][0],data[idx][1],data[idx-1][0],data[idx-1][1])
            data[idx][6]=(data[idx][3]-data[idx-1][3]).seconds
            data[idx][5]=3600*data[idx][4]/data[idx][6]
            
            
    df_gpx = pd.DataFrame(data,columns=['lon', 'lat', 'alt', 'time', 'dist', 'speed','dtim'])
    df_gpx = df_gpx.set_index("time") 
    return df_gpx

def show_gpx_info(tracks):
    print("Projection= {}, Boundary= {}".format(tracks.crs, tracks.bounds))
    print("Number of tracks = {}".format(len(list(tracks.items()))))
    geom = tracks[0]
    print ("Geom type = {}, Geom keys = {}".format(type(geom), geom.keys()))
    print ("geom(type)={}, geom(id) = {}, geom(properties)= {}".format(geom['type'],geom['id'],geom['properties']))

def add_dist(df):
    df['lon_1'] = df['lon'].shift(1)
    df['lat_1'] = df['lat'].shift(1)
    df['dist'] = df.apply(lambda row: haversine(row['lon_1'],row['lat_1'],\
                                                row['lon'],row['lat']),axis=1)
    df = df.drop(['lon_1','lat_1'],axis=1)
    return df

if __name__ == "__main__":
    main()