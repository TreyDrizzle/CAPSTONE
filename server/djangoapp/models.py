from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarMake(models.Model):
    # - Name
    name = models.CharField(null=False, max_length=50)
    # - Description
    description = models.CharField(null=True, max_length=500)
    # - Any other fields you would like to include in car make model
    # - __str__ method to print a car make object
    def __str__(self):
        return self.name


class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    make = models.ForeignKey('CarMake', on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='SampleModel')
    CAR_CHOICES = (
    ("SEDAN", "Sedan"),
    ("SUV", "SUV"),
    ("TRUCK", "Truck"),
    ("CONVERTABLE", "Convertable"),
    ("VAN", "Van"),
    )
    car = models.CharField(max_length=11, choices=CAR_CHOICES, default="SEDAN")
    dealerid = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f'{self.name},{self.make},{self.year}'

#CarDealer Class
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, id, review, sentiment, **kwargs):
        
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.sentiment = sentiment
        
        if purchase:
            self.purchase_date = kwargs["purchase_date"]
            self.car_make = kwargs["car_make"]
            self.car_model = kwargs["car_model"]
            self.car_year = kwargs["car_year"]
        
        
    def __str__(self):
        return "Review: " + self.review



