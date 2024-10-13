from django.db import models

# Create your models here.
class LoadPosting(models.Model):
    id = models.IntegerField()
    load_id = models.TextField(primary_key=True)
    posting_status = models.TextField()
    source_system = models.TextField()
    has_appointment = models.BooleanField()
    is_harzardous = models.BooleanField()
    is_high_value = models.BooleanField()
    is_temperature_controlled = models.BooleanField()
    total_distance = models.FloatField()
    distance_uom = models.TextField()
    total_weight = models.FloatField()
    weight_uom = models.TextField()
    number_of_stops = models.IntegerField()
    transport_mode = models.TextField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    managed_equipment = models.TextField()
    load_number_alias = models.TextField()
    is_carb = models.BooleanField()
    fpc = models.TextField()
    fpo = models.TextField()
    division = models.TextField()

    

    def __str__(self):
        return self.load_id

class LoadStop(models.Model):
    id = models.IntegerField()
    load_id = models.TextField(primary_key=True)
    stop_id = models.TextField()
    stop_sequence = models.IntegerField()
    stop_type = models.TextField()
    activity_type = models.TextField()
    appointment_from = models.DateTimeField()
    appointment_to = models.DateTimeField()
    city = models.TextField()
    state = models.TextField()
    postal_code = models.TextField()
    time_zone = models.TextField()
    country = models.TextField()
    created_date = models.DateTimeField()
    created_date = models.DateTimeField()
    appointement_state = models.TextField()




    def __str__(self):
        return self.stop_id
