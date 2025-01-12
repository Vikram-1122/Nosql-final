# Nosql-final

      Travel and Tourism Platform

Overview

The Travel and Tourism Platform is a comprehensive web-based application designed to help users explore travel destinations worldwide. The platform integrates MongoDB, Neo4j, and Redis databases to provide detailed destination information, relationships between countries and destinations, and real-time updates.

  Features
Streamlit Web Interface: Interactive user interface to select countries and explore destinations.
Database Integration:
MongoDB: Stores structured data about destinations, such as accommodations, itineraries, and travel tips.
Neo4j: Manages relationships between countries and their destinations.
Redis: Provides real-time updates, including weather and booking data.
Dynamic Updates: Fetches live data from Redis to display current popularity and weather.
  
  Architecture
MongoDB: Stores destination data in JSON format.
Neo4j: Creates graph relationships between countries and destinations using Cypher queries.
Redis: Uses key-value storage for real-time data updates.
Streamlit: Python-based frontend for data visualization and interaction.

  Prerequisites
Python 3.x
MongoDB Server
Neo4j Server
Redis Server
 
  Required Python Libraries:
streamlit
pymongo
neo4j
redis
