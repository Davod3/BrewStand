# BrewStand Application

## Overview
This is the definition of the REST API for the BrewStand application. With this API users will be able to 
create and obtain account tokens, view and compare beer types, as well as order beer in bulk from the
available types

## Requirements
Docker
Docker Compose

## Usage
To run all the services locally, please execute the following from the root directory:

```
./start.sh
```

If all the micro services started successfully, their APIs should be accessible as follows:

User API:
```
http://localhost:3000/ui
```

Review API:
```
http://localhost:3003/ui
```

To stop the execution run the following from the root directory:

```
./stop.sh
```

## Deployment

TODO