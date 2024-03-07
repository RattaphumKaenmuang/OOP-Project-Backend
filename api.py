from main import *
import uvicorn
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/flight_instance_matches", tags=["1: Show + Get Flight Instance Matches"])
def get_flight_instances_matches(froml : str, to : str, depart_date : str, return_date : Optional[str] = None):
    return nokair.get_flight_instance_matches(froml, to, depart_date, return_date)

@app.get("/get_all_seats", tags=["1: Show + Get Flight Instance Matches"])
def get_all_seats(flight_number : str, date : str):
    return nokair.get_flight_instance(flight_number, date).flight_seat_list

@app.get("/get_all_services", tags=["1: Show + Get Flight Instance Matches"])
def get_all_services():
    return nokair.service_list

@app.get("/get_all_airports", tags=["1: Show + Get Flight Instance Matches"])
def get_all_airports():
    return nokair.airport_list

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")