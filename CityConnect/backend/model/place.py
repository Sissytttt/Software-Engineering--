import mysql.connector

class Place:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.name = None
        self.longitude = None
        self.latitude = None
        self.city = None

    # def Get_Name(self):
    #     return self.name
    def Get_Name(self, longitude, latitude):
        cursor = self.connection.cursor()
        query = """
        SELECT name FROM place 
        WHERE longitude = %s AND latitude = %s
        """
        cursor.execute(query, (longitude, latitude))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return "No place found with the provided coordinates."

    # def Get_location_longitude(self):
    #     return self.longitude
    def Get_location_longitude(self, name):
        cursor = self.connection.cursor()
        query = "SELECT longitude FROM place WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return "No place found with this name."

    def Get_location_latitude(self, name):
        cursor = self.connection.cursor()
        query = "SELECT latitude FROM place WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return "No place found with this name."

    def Get_city(self, name):
        cursor = self.connection.cursor()
        query = "SELECT city FROM place WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return "No place found with this name."

    def Set_Name(self, longitude, latitude, new_name):
        cursor = self.connection.cursor()
        query = """
        UPDATE place 
        SET name = %s 
        WHERE longitude = %s AND latitude = %s
        """
        cursor.execute(query, (new_name, longitude, latitude))
        self.connection.commit() 
        affected_rows = cursor.rowcount
        cursor.close()
        if affected_rows > 0:
            return "Name updated successfully."
        else:
            return "No place found with the provided coordinates."



# Example usage:
# Initialize the Place object with your MySQL database credentials
place = Place(host='127.0.0.1', user='root', password='', database='software_engineering')


# Access the details
name = place.Get_Name(longitude='31.2337000000', latitude='121.5050000000')
print(name)  # Shanghai Tower

longitude = place.Get_location_longitude("Shanghai Tower")
print(longitude) # 31.2337000000

latitude = place.Get_location_latitude("Shanghai Tower")
print(latitude) # 121.5050000000

city = place.Get_location_latitude("Shanghai Tower")
print(city) # Shanghai

place.Set_Name(longitude='31.2337000000', latitude='121.5050000000', new_name = 'Test_Update_Shanghai_Tower')
new_name = place.Get_Name(longitude='31.2337000000', latitude='121.5050000000')
print(new_name) # Test_Update_Shanghai_Tower