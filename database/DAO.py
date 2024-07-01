from database.DB_connect import DBConnect
from model.location import Location


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getProvider():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct(nwhl.Provider) 
                    from nyc_wifi_hotspot_locations nwhl 
                    order by nwhl.Provider 
        """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Provider"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCollegamenti (provider):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select Location, avg(n.Latitude) as mLat, avg(n.Longitude) as mLon 
                    from nyc_wifi_hotspot_locations n
                    where Provider = %s
                    group by Location
                    order by Location asc 
        """
        cursor.execute(query, (provider,))
        for row in cursor:
            result.append(Location(row["Location"], row["mLat"], row["mLon"]))

        cursor.close()
        conn.close()
        return result

