import csv
import os.path


def correct_photo_format(photo):
    root, ext = os.path.splitext(photo)
    for ends in ('.jpg', '.jpeg', '.png', '.gif'):
        if ends == ext:
            return photo


class CarBase:
    """Basic class for all types of mashines"""

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext


class Car(CarBase):
    """Class of cars"""

    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.validate_value(passenger_seats_count))

    def validate_value(self, value):
        if value == '':
            value = 0
        return value


class Truck(CarBase):
    """Class for Trucks"""

    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = self.get_lwh(
            body_lwh)

    def get_lwh(self, body_lwh):
        try:
            length, width, height = (float(i) for i in body_lwh.split("x"))
        except Exception:
            length, width, height = 0.0, 0.0, 0.0
        return length, width, height

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    """Class for spechial transport"""

    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    csv.register_dialect('cars', delimiter=';')
    car_list = []
    cars = []

    with open(csv_filename, encoding='utf-8') as csv_fd:
        # csv.register_dialect('cars', delimiter=';')
        reader = csv.reader(csv_fd, dialect='cars')
        next(reader)
        for row in reader:
            if len(row) == 7:
                try:
                    car_list.append(row)
                except Exception:
                    pass
    for list in car_list:
        try:
            list[5] = float(list[5])
        except Exception:
            list[0] = ''
        if correct_photo_format(list[3]) is None:
            list[0] = ''
        if list[1] == '' or list[1] == ' ':
            list[0] = ''
    for list in car_list:
        if list[0] == 'car' and list[2] != '':
            car = Car(list[1], list[3], list[5], list[2])
            print(list)
            cars.append(car)
        elif list[0] == 'truck':
            truck = Truck(list[1], list[3], list[5], list[4])
            cars.append(truck)
        elif list[0] == 'spec_machine' and list[6] != '':
            cpec = SpecMachine(list[1], list[3], list[5], list[6])
            cars.append(cpec)
    return cars


if __name__ == "__main__":
    print(get_car_list("cars_coursera.csv"))
