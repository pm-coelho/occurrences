# Occurrences [![Build Status](https://travis-ci.com/pm-coelho/occurrences.svg?branch=feature-dev)](https://travis-ci.com/pm-coelho/occurrences)

## How to run
```bash
git clone git@github.com:pm-coelho/occurrences.git
cd occurrences  
docker build .  
docker-compose build  
```

To test with a client fire up the container
```bash
docker-compose up
```

To run the tests
```bash
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

A postman collection and environment is provided to make testing easier

## Thoughts

  * Occurrence.author filed is set o PROTECT on_delete because there's a status resolve wich implies that even after resolved, the occurrence history should stay saved. In order to delete a user we should probably set it to inactive and don't show it.

  * User create endpoint was created to make it easier to create test users
  
  * Basic authentication is used to access private endpoints (To my understanding, implementation  of another method was out of scope)
  
## TODO
  * Swagger documentation
  
## Endpoints
### User
#### Create User - (POST) /api/user/
Creates a new user to facilitate testing

  * Authorization: public
```json
{
  "username": "alice",
  "password": "wonderland"
}
```

### Occurrence
```json
    {
        "id": 1,
        "description": "Bob the Builder, that's what I do",
        "author": 2,
        "state": "VALIDATED",
        "category": "CONSTRUCTION",
        "location": {
            "latitude": 48.8430,
            "longitude": 79.5395
        },
        "created_at": "2019-08-01T14:49:50.853768Z",
        "updated_at": "2019-08-01T14:52:06.268452Z"
    }
```

  * Enums:
    * Category: 
      * CONSTRUCTION: 'planed road work'
      * SPECIAL_EVENT: 'special events (fair, sport event, etc.)'
      * INCIDENT: 'accidents and other unexpected events'
      * WHEATHER_CONDITION: 'wheather condition affecting the road'
      * ROAD_CONDITION: 'status of the road that might affect travellers (potholes, bad pavement, etc)'
    
    * Status:
      * NOT_VALIDATED: 'not validated' - default on occurrence created
      * VALIDATED: 'validated'
      * RESOLVED: 'resolved'

#### Create Occurrence - (POST) /api/occurrence/

  * Authorization: admin / user
```json
{
  "description": "Bob the Builder, that's what I do",
  "category": "CONSTRUCTION",
  "location": {
    "latitude": 43.8430,
    "longitude": 79.5395
  }
}
```

#### Partial update Occurrence - (PATCH) /api/occurrence/<id>/

  * Authorization: admin
  * Any partial update, can be used to update the state
```json
{
  "state": "VALIDATED""
}
```
  
#### Update Occurrence - (PUT) /api/occurrence/<id>/

  * Authorization: admin
  ```json
    {
        "description": "Bob the Builder, that's what I do",
        "category": "CONSTRUCTION",
        "author": 2,
        "state": "RESOLVED",
        "location": {
        	"latitude": 43.8430,
        	"longitude": 79.5395
        }
    }
  ```
  
#### Get Occurrence list - (GET) /api/occurrence/

  * Authorization: admin / user
  * Listing with a user account only show user's occurrences
  
  * Query Filters:
    * author: filter by author
    * category: filter by category

    * latitude, longitude: filter by longitude, only works if both are sent
    * radius: radius related to the latitude and longitude fields

