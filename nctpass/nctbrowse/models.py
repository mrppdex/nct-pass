from django.db import models

# Create your models here.
class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(default=2000)
    total = models.IntegerField(default=0)
    passed = models.IntegerField(default=0)

    vehicle_and_safety_equipment = models.IntegerField(default=0)
    lighting_and_electrical = models.IntegerField(default=0)
    steering_and_suspension = models.IntegerField(default=0)
    braking_equipment = models.IntegerField(default=0)
    wheels_and_tyres = models.IntegerField(default=0)
    engine_noise_and_exhaust = models.IntegerField(default=0)
    chassis_and_body = models.IntegerField(default=0)
    side_slip_test = models.IntegerField(default=0)
    suspension_test = models.IntegerField(default=0)
    light_test = models.IntegerField(default=0)
    brake_test = models.IntegerField(default=0)
    emmissions = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    incompletable = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.make} {self.model} {self.year} {self.total}: {self.pass_rate}%"
