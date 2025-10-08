from datetime import date
from django.db import models
import uuid

class Instrument(models.Model):
    iid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name= models.CharField(max_length=50)
    ticker= models.CharField(max_length=50)
    currency= models.CharField(max_length=50)
    instrument_type= models.CharField(max_length=50)

class Company(models.Model):
    cid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    sector= models.CharField(max_length=50)
    industry= models.CharField(max_length=50)

class Equity(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)

class ETF(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )

class FX(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )

class Price(models.Model):
    price_id = 
    iid =models.ForeignKey(Instrument,on_delete=models.CASCADE)
    price_timestamp= models.
    open_price= models.DecimalField(decimal_places=2)
    high_price= models.DecimalField(decimal_places=2)
    low_price= models.DecimalField(decimal_places=2)
    close_price= models.DecimalField(decimal_places=2)
    volume