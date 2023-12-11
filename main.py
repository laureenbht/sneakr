import mysql.connector
import requests

db_config = {
    'user': 'root',
    'password': '2005Laba!',
    'host': 'localhost',
    'database': 'sneaker'
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

try:
    if connection.is_connected():
        print("Connexion à la base de données MySQL réussie.")
except mysql.connector.Error as err:
    print(f"Erreur de connexion à la base de données: {err}")

api_base_url = 'http://54.37.12.181:1337/api/sneakers'
total_pages = 49214

for page in range(1, total_pages + 1):
    api_url = f'{api_base_url}?pagination[page]={page}'

    response = requests.get(api_url)

    if response.status_code == 200:
        api_data = response.json()['data']

        for product_data in api_data:
            data = product_data["attributes"]
            values = (
                product_data["id"],
                data["brand"],
                data["colorway"],
                data["estimatedMarketValue"],
                data["gender"],
                data["image"]["small"],
                data["image"]["original"],
                data["image"]["thumbnail"],
                data["links"]["goat"],
                data["links"]["stockX"],
                data["links"]["flightClub"],
                data["links"]["stadiumGoods"],
                data["name"],
                data["releaseYear"],
                data["retailPrice"],
                data["silhouette"],
                data["sku"],
                data["story"],
                data["UID"]
            )

            query = """
                INSERT INTO products (
                    id, brand, colorway, estimatedMarketValue, gender,
                    small_image_url, original_image_url, thumbnail_image_url,
                    goat_link, stockx_link, flightclub_link, stadiumgoods_link,
                    name, releaseYear, retailPrice, silhouette,
                    sku, story, UID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, values)

        connection.commit()

        print(f"Données de la page {page} insérées dans la base de données.")
    else:
        print(f"Erreur lors de la requête à l'API (page {page}). Code d'erreur : {response.status_code}")

cursor.close()
connection.close()