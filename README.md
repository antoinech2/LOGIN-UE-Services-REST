# UE Services

## TP API REST

### IMT Atlantique Nantes - TAF LOGIN*

#### Nathan CLAEYS, Jean-Baptiste LAMBERTIN, Antoine CHEUCLE

## Projet description

The aim of this project is to illustrate the usage of REST APIs between multiple microservices.
This project is a simulation of a cinema management application (simplified). There are 4 interacting microservices:

- **movie**, which manages data on films being shown
- **showtime**, which manages data on film release dates
- **booking**, manages users' viewing reservations
- **user**, provides an API that can be used by the service's customers.

In this TP, all the APIs use REST to communicate.
All APIs documentation can be found in the OpenAPI YAML file in the root of each service.

## How to run

### Requirements

- Python 3

- Install modules (in `requirements.txt`)

### Automatic start (Windows)

To run all services automatically, simply run `run.bat` at the root of the project.
Close the window to stop services

### Manual start

Run individually all services:

- `python movie/movie.py`
- `python showtime/showtime.py`
- `python booking/booking.py`
- `python user/user.py`
