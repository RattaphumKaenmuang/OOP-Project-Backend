#API
#1.show_reservation
#2.pay_by_credit_card
#3.pay_by_qr
#4.get_flight_instance_matches
#5.select_flight //return flight_instance + show flight seats
#6.get_all_services //return services_list
#7.check_in //return boarding pass
#8.create_flight
#9.create_flight_instance

class AirportSystem:                                     
    def __init__(self):
        self.__airport_list = []
        self.__aircraft_list = []
        self.__flight_list = []
        self.__flight_instance_list = []
        self.__service_list = []
        self.__reservation_list = []

    @property
    def airport_list(self):
        return self.__airport_list

    @property
    def aircraft_list(self):
        return self.__aircraft_list
        
    @property
    def flight_list(self):
        return self.__flight_list
    
    @property
    def flight_instance_list(self):
        return self.__flight_instance_list
    
    @property
    def service_list(self):
        return self.__service_list

    @service_list.setter
    def service_list(self, service):
        self.__service_list.append(service)
    
    def get_flight_instance_matches(self, starting_location, destination, date_depart, date_return = None):
        departing_flight_instance = []
        returning_flight_instance = []

        for flight_instance in self.__flight_instance_list:
            if flight_instance.starting_location.name == starting_location and flight_instance.destination.name == destination and flight_instance.date == date_depart:
                flight_instance_info = {"departure_time": flight_instance.departure_time,
                                        "arrival_time": flight_instance.arrival_time,
                                        "flight_number": flight_instance.flight_number,
                                        "aircraft_number": flight_instance.aircraft.aircraft_number,
                                        "cost": flight_instance.cost}
                
                departing_flight_instance.append(flight_instance_info)

        if date_return != None:
            for flight_instance in self.__flight_instance_list:
                if flight_instance.destination.name == starting_location and flight_instance.starting_location.name == destination and flight_instance.date == date_return:
                    flight_instance_info = {"departure_time": flight_instance.departure_time,
                                        "arrival_time": flight_instance.arrival_time,
                                        "flight_number": flight_instance.flight_number,
                                        "aircraft_number": flight_instance.aircraft.aircraft_number,
                                        "cost": flight_instance.cost}

                    returning_flight_instance.append(flight_instance_info)

        return (departing_flight_instance, returning_flight_instance)

    def get_flight_instance(self, flight_number, date):
        for flight_instance in self.__flight_instance_list:
            if flight_instance.flight_number == flight_number and flight_instance.date == date:
                return flight_instance
    
class Reservation:
    def __init__(self, flight_instances, passengers_list, flight_seats_list, payment_method):
        self.__booking_reference = None
        self.__flight_instances = flight_instances
        self.__passengers = passengers_list
        self.__flight_seats_list = flight_seats_list
        self.__total_cost = 0                                                                                                   
        self.__payment_method = payment_method
        self.__boarding_passes_list = []

class User:
    pass

class Passenger(User):
    pass

class Admin(User):
    pass

class BoardingPass:
    pass

class Flight:
    def __init__(self, starting_location, destination, flight_number):
        self.__starting_location = starting_location
        self.__destination = destination
        self.__flight_number = flight_number

    @property
    def flight_number(self):
        return self.__flight_number  
      
    @property
    def starting_location(self):
        return self.__starting_location
    
    @property
    def destination(self):
        return self.__destination

class FlightInstance(Flight):
    def __init__(self, flight, departure_time, arrival_time, aircraft, date, cost):
        super().__init__(flight.starting_location, flight.destination, flight.flight_number)
        self.__flight_seat_list = []
        for seat in aircraft.seat_list:
            self.__flight_seat_list.append(FlightSeat(seat))
        self.__departure_time = departure_time
        self.__arrival_time = arrival_time
        self.__aircraft = aircraft
        self.__date = date
        self.__cost = int(cost)
        
    @property
    def departure_time(self):
        return self.__departure_time
    
    @property
    def arrival_time(self):
        return self.__arrival_time
    
    @property
    def aircraft(self):
        return self.__aircraft
    
    @property
    def date(self):
        return self.__date
    
    @property
    def cost(self):
        return self.__cost

    @property
    def flight_seat_list(self):
        return self.__flight_seat_list
    
class Aircraft:
    def __init__(self, aircraft_number):
        self.__seat_list = self.__init_default_seat_list()
        self.__aircraft_number = aircraft_number

    @property
    def aircraft_number(self):
        return self.__aircraft_number
    
    @property
    def seat_list(self):
        return self.__seat_list
    
    def __init_default_seat_list(self):
        seats_data = []
        for r in range(1,6):
            for c in range(0,3):
                alphabets = "ABCDEF"
                seat_id = f"{alphabets[c]}{r}"
                seat_category = SeatCategory("normal_seat", 200)
                if r <= 2:
                    seat_category = SeatCategory("premium_seat", 600)
                if r <= 4:
                    seat_category = SeatCategory("happy_seat", 400)
                seats_data.append(Seats(seat_id, seat_category))
        return seats_data

class Airport:
    def __init__(self, name, short_name):
            self.__name = name
            self.__short_name = short_name
            
    @property
    def name(self):
            return self.__name

class Seats:
    def __init__(self, seat_number, seat_category):
        self.__seat_number = seat_number
        self.__seat_category = seat_category

    @property
    def seat_number(self):
        return self.__seat_number
    
    @property
    def seat_category(self):
        return self.__seat_category

class FlightSeat(Seats):
    def __init__(self, seat):
        super().__init__(seat.seat_number, seat.seat_category)
        self.__occupied = False
    
    @property
    def occupied(self):
        return self.__occupied
    
    @occupied.setter
    def occupied(self, occupied):
        self.__occupied = occupied
        return "Success"

class SeatCategory:
    def __init__(self, name, price_per_unit):
        self.__name = name
        self.__price = int(price_per_unit)

    @property
    def seat_price(self) :
        return self.__price


class Payment:
    pass


class CreditCard(Payment):
    pass


class Qr(Payment):
    pass


class Service:
    def __init__(self, service_name, price_per_unit):
        self.__service_name = service_name
        self.__price_per_unit = float(price_per_unit)

    @property
    def price_per_unit(self):
        return self.__price_per_unit

class Insurance(Service):
    def __init__(self, service_name, price_per_unit):
        super().__init__(service_name, price_per_unit)


class Baggage(Service):
    def __init__(self, service_name, price_per_unit, weight):
        super().__init__(service_name, price_per_unit)
        self.__weight = weight

    # def get_total_cost(self):
    #     return self.price_per_unit * self.__weight
    
    # @property
    # def bag_weight(self) :
    #     return self.__weight

nokair = AirportSystem()
nokair.airport_list.append(Airport("Don Mueang", "DMK"))
nokair.airport_list.append(Airport("Chiang Mai", "CNX"))
nokair.flight_list.append(Flight(nokair.airport_list[0], nokair.airport_list[1], "ABC"))
nokair.flight_list.append(Flight(nokair.airport_list[1], nokair.airport_list[0], "ABC"))

nokair.aircraft_list.append(Aircraft("101"))
nokair.flight_instance_list.append(FlightInstance(nokair.flight_list[0], "10:00", "12:00", nokair.aircraft_list[0], "01-01-2000", 1000))
nokair.flight_instance_list.append(FlightInstance(nokair.flight_list[1], "10:00", "12:00", nokair.aircraft_list[0], "02-01-2000", 1000))

nokair.service_list = Insurance("Insurance", 100)
nokair.service_list = Baggage("+5kg Baggage", 100, 5)
nokair.service_list = Baggage("+10kg Baggage", 100, 10)
nokair.service_list = Baggage("+15kg Baggage", 100, 15)