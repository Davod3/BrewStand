# BrewStand Application

## Overview
This is the definition of the REST API for the BrewStand application. With this API users will be able to 
create and obtain account tokens, view and compare beer types, as well as order beer in bulk from the
available types

## Requirements
Docker

Docker Compose

## Installation

To install this application simply clone this repository in your desired location. To clone the latest release use the following command, filling in your credentials as required:

```
git clone https://github.com/Davod3/BrewStand-CloudComputing-14.git --branch phase3
```

Afterwards, download the Brewery Operations and Market Analysis Dataset (https://www.kaggle.com/datasets/ankurnapa/brewery-operations-and-market-analysis-dataset) and rename it to dataset.csv.

Once you're done with that, simply create a folder called dataset in the root directory of the cloned repository and move the .csv file there, 
such that its path will be /dataset/datset.csv

Alternatively, you can create the /dataset folder and download the dataset into there from google cloud storage with the following command:

```
wget https://storage.googleapis.com/brewstand-datset/dataset.csv
```

## Usage
To run all the services locally, please execute the following from the root directory:

```
./start.sh
```

Keep in mind that the first time you run the application data might not be immediately available, as the dataset is still being loaded.

During this time, inventory_repository will stop and restart multiple times as it attempts to connect to the postgres db which takes a little longer to start up. This is completely normal.

If all the micro services started successfully, their APIs should be accessible as follows:

Inventory API:
```
http://localhost:3001/ui
```

User API:
```
http://localhost:3002/ui
```

Review API:
```
http://localhost:3003/ui
```

Order API:
```
http://localhost:3004/ui
```

Payment API:
```
http://localhost:3005/ui
```

If the application is being run on a google cloud vm, please replace localhost with the web preview url for the desired port followed by /ui, such as this example for port 3006:

```
https://3006-cs-866602736120-default.cs-europe-west1-iuzs.cloudshell.dev/ui/
```

To stop the execution run the following from the root directory:

```
./stop.sh
```

## Deployment

TODO
