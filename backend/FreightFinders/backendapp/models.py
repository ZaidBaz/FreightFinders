from django.db import models

# Create your models here.
class LoadStop(models.Model):
    stop_id = models.CharField(max_length=255, primary_key=True)  # Assuming stop_id is unique and primary key
    id = models.BigIntegerField()  # If you want to keep this field, but Django auto-generates 'id' by default
    load_id = models.CharField(max_length=255)
    stop_sequence = models.SmallIntegerField()
    stop_type = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)
    appointment_from = models.DateTimeField()
    appointment_to = models.DateTimeField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    time_zone = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    appointment_state = models.CharField(max_length=255)

    class Meta:
        db_table = 'load_stop' 

    def __str__(self):
        return f"LoadStop {self.stop_id} for Load {self.load_id}"

class LoadPosting(models.Model):
    id = models.BigAutoField(primary_key=True)  # Assuming 'id' is the primary key
    load_id = models.CharField(max_length=255)
    posting_status = models.CharField(max_length=255)
    source_system = models.CharField(max_length=255)
    has_appointments = models.BooleanField()
    is_hazardous = models.BooleanField()
    is_high_value = models.BooleanField()
    is_temperature_controlled = models.BooleanField()
    total_distance = models.FloatField()
    distance_uom = models.CharField(max_length=10)
    total_weight = models.FloatField()
    weight_uom = models.CharField(max_length=10)
    number_of_stops = models.IntegerField()
    transport_mode = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    managed_equipment = models.BooleanField()
    load_number_alias = models.CharField(max_length=255)
    is_carb = models.BooleanField()
    fpc = models.BooleanField()
    fpo = models.BooleanField()
    division = models.CharField(max_length=255)

    class Meta:
        db_table = 'load_posting' 

    def __str__(self):
        return f"LoadPosting {self.load_id}"