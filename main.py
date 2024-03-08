from datetime import datetime
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
            
    def paid_by_qr(self, reservation):
        payment_method = Qr()
        transaction = Transaction(payment_method)
        self.create_reservation_for_paid(reservation, transaction)
        return "success"

    def pay_by_credit_card(self, card_number, cardholder_name, expiry_date, cvv, reservation_data):
        reservation = self.__create_reservation_for_paid(reservation_data)
        if reservation:
            payment_method = CreditCard(card_number, cardholder_name, expiry_date, cvv)
            reservation.transaction = Transaction(payment_method)
            self.__reservation_list.append(reservation)
            return "success"
        return "error"

    def create_reservation_for_paid(self, reservation, transaction):
        reservation = Reservation()
        flight_instance_list = reservation[0]
        passenger_list  = reservation[1]
        flight_seats_list = reservation[2]
        
        #0 = title, 1 = first_name, 2 = middle_name, 3 = last_name, 4 = birthday, 5 = phone_number, 6 = email
        for passenger_data in passenger_list:
            passenger = Passenger(passenger_data[0], passenger_data[1], passenger_data[2], passenger_data[3], passenger_data[4], passenger_data[5], passenger_data[6])
            reservation.add_passenger(passenger)
        
        #0 = flight_number, 1 = date
        for flight_instance_data in flight_instance_list:
            flight_instance = self.get_flight_instance(flight_instance_data[0], flight_instance_data[1])
            reservation.add_flight_instance(flight_instance)
        
        for index, flight_instance in enumerate(reservation.flight_instances_list):
            new_flight_seat_list = []
            
            for flight_seat_number in flight_seats_list[index]:
                flight_seat = flight_instance.get_flight_seat(flight_seat_number)
                if flight_seat.occupied:
                    return None
                flight_seat.occupied = True
                new_flight_seat_list.append(flight_seat)
                
            reservation.add_flight_seat(new_flight_seat_list)
        return reservation

    def add_service():
        pass

class Reservation:
    def __init__(self):
        self.__booking_reference = None
        self.__flight_instance_list = []
        self.__passenger_list = []
        self.__flight_seat_list = []
        self.__total_cost = 0                                                                                                   
        self.__transaction = None
        self.__boarding_passes_list = []
        
    @property
    def flight_instances_list(self):
        return self.__flight_instance_list

    @property
    def transaction(self):
        return self.__transaction
    
    def add_passenger(self, passenger):
        self.__passenger_list.append(passenger)
    
    def add_flight_seat(self, flight_seat):
        self.__flight_seat_list.append(flight_seat)
        
    def add_flight_instance(self, flight_instance):
        self.__flight_instance_list.append(flight_instance)
    
class User:
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        self.__title = title
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__birthday = birthday
        self.__phone_number = phone_number
        self.__email = email

class Passenger(User):
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        super().__init__(title, first_name, middle_name, last_name, birthday, phone_number, email)
        self.__extra_services = []

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

    def get_flight_seat(self, seat_number):
        for flight_seat in self.__flight_seat_list:
            if flight_seat.seat_number == seat_number:
                return flight_seat
    
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


class PaymentMethod:
    def __init__(self):
        self.__payment_fee = 0
        
    @property
    def payment_fee(self):
        return self.__payment_fee


class CreditCard(PaymentMethod):
    def __init__(self, card_number, cardholder_name, expiry_date, cvv):
        self.__card_number = card_number
        self.__cardholder_name = cardholder_name
        self.__expiry_date = expiry_date
        self.__cvv = cvv
        self.__payment_fee = 240
    

class Qr(PaymentMethod):
    pass

class Transaction:
    def __init__(self, payment_method: PaymentMethod):
        self.__paid_time = datetime.now()
        self.__payment_method = payment_method

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

print(nokair.get_flight_instance_matches("Don Mueang", "Chiang Mai", "01-01-2000", "02-01-2000"))