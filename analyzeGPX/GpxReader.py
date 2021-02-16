
class GpxReader():
"""
Read information from GPX file. 


"""
    def __init(gpx_file)__:
        self df = self.__parse_gpx(gpx_file)

    def __parse_gpx(path):
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