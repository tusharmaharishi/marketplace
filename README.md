# RideShare

[![Build Status](https://travis-ci.org/bryanchen18/marketplace.png?branch=master)](https://travis-ci.org/bryanchen18/marketplace)

### Setup
1. Make sure mysql is running, then `docker start mysql`
2. From the project root directory, `docker-compose up`
4. `http://localhost:8000`

### User Stories
- Story 1: As a user I want to be able to select a group to find a ride.
- Story 2: As a user I want to be able to view the details of a carpool I'm in.
- Story 3: As a user I want to be able to add a group I am part of. 
- Story 4: As a user I want to be able to choose whether I'm a passenger or driver. 
- Story 5: As a user I want to be able to filter locations to see all carpools available from my chosen starting location to my destination.
- Story 6: As a user I want to be able to view more details about a carpool and driver. 
- Story 7: As a user I want to be able to view my profile information and payment details as well as settings. 
- Story 8: As a user and driver I want to be able to create and advertise a carpool.
- Story 9: As a user I want to be able to search a carpool in the search bar.
- Story 10: As a user after searching I want to receive a search results page populated with results.
- Story 11: As a driver I want to be able to create a listing and then see it in search results.
- Story 12: As a producer/progammer I want to be able to put new listings into a Kafka queue.
- Story 13: As a producer/programmer I want to see the listings in the Kafka queue be added to the elastic search.
- Story 14: As a user I don't want to see register/log-in buttons after I've logged in.