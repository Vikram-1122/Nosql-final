import streamlit as st
from pymongo import MongoClient
from neo4j import GraphDatabase
import redis

# ==========================
# Database Connections
# ==========================

# MongoDB Connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["travel_platform"]
mongo_destinations = mongo_db["destinations"]

# Neo4j Connection
neo4j_driver = GraphDatabase.driver(
    "neo4j+s://b6fb340d.databases.neo4j.io",
    auth=("neo4j", "japoI-OjuxfoB1iXOThbea1PvUUqIzDBcz0sVu7foKQ")
)

# Redis Connection
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# ==========================
# Helper Functions
# ==========================

# MongoDB: Fetch destination details
def get_destination_details(destination_id):
    destination = mongo_destinations.find_one({"destination_id": destination_id})
    if destination:
        return {
            "name": destination["name"],
            "country": destination["country"],
            "best_season": destination["best_season"],
            "timezone": destination["timezone"],
            "weather": destination["weather"],
        }
    return None

# Neo4j: Fetch destinations for a country
def get_destinations_by_country(country_name):
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (c:Country {name: $country_name})-[:LOCATED_IN]->(d:Destination)
            RETURN d.name AS destinations
        """, country_name=country_name)
        return [record["destinations"] for record in result]

# Redis: Fetch real-time data
def get_real_time_data(destination_id):
    return {
        "popular": redis_client.get(f"{destination_id}:popular"),
        "weather": redis_client.get(f"{destination_id}:weather"),
        "bookings": redis_client.get(f"booking:{destination_id}")
    }

# ==========================
# Debugging Functions
# ==========================

# Debugging: Test MongoDB connection
def test_mongo_connection():
    print("Collections in MongoDB:", mongo_db.list_collection_names())
    print("Sample record from MongoDB:", mongo_destinations.find_one())

# Debugging: Print queried destination ID
def debug_destination_id(destination_id):
    print(f"Fetching destination with ID '{destination_id}' from MongoDB.")

# ==========================
# Streamlit App
# ==========================

st.title("Travel and Tourism Platform")
st.sidebar.header("Search Destinations")

# Input: Select Country
countries = ["France", "USA", "Australia", "India", "Japan", "Brazil", "Germany", "Canada", "South Africa", "Italy"]
selected_country = st.sidebar.selectbox("Select a Country", countries)

if selected_country:
    st.header(f"Destinations in {selected_country}")

    # Fetch Destinations from Neo4j
    destinations = get_destinations_by_country(selected_country)
    if destinations:
        selected_destination = st.selectbox("Select a Destination", destinations)

        if selected_destination:
            # Fetch Destination Details from MongoDB
            destination_id = selected_destination.lower().replace(" ", "_")
            debug_destination_id(destination_id)  # Debugging destination ID

            destination_details = get_destination_details(destination_id)

            if destination_details:
                st.subheader(f"Details for {destination_details['name']}")
                st.write(f"**Country:** {destination_details['country']}")
                st.write(f"**Best Season to Visit:** {destination_details['best_season']}")
                st.write(f"**Timezone:** {destination_details['timezone']}")
                st.write(f"**Weather:** {destination_details['weather']}")

                # Fetch Real-Time Data from Redis
                real_time_data = get_real_time_data(destination_id)
                st.subheader("Real-Time Information")
                st.write(f"**Popularity:** {real_time_data.get('popular', 'N/A')}")
                st.write(f"**Current Weather:** {real_time_data.get('weather', 'N/A')}")
                st.write(f"**Bookings:** {real_time_data.get('bookings', 'N/A')}")
            else:
                # Graceful handling for missing MongoDB data
                st.write(f"Details for {selected_destination} are not available yet in MongoDB.")
    else:
        # Graceful handling for missing destinations in Neo4j
        st.warning("No destinations found for the selected country.")

# ==========================
# Debugging Output
# ==========================

# Uncomment these lines for debugging if needed
# test_mongo_connection()

# ==========================
# Closing Connections
# ==========================

neo4j_driver.close()
mongo_client.close()
