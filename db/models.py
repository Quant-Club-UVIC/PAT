from datetime import date
from django.db import models
import uuid

class Currency(models.Model):
    fid = models.CharField(max_length=3, primary_key=True)
    countryOfIssue = models.CharField(max_length=50)

class Instrument(models.Model):
    iid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    currencyOfIssue= models.CharField(max_length=50)

    name= models.CharField(max_length=50)
    ticker= models.CharField(max_length=50)
    
    instrument_type= models.CharField(max_length=50)
    start_date=models.DateField(auto_now_add=False)
    end_date=models.DateField(auto_now_add=False)

class Company(models.Model):
    cid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    ticker = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    sector= models.CharField(max_length=50)
    industry= models.CharField(max_length=50)

class CorporateAction(models.Model):
    action_id=models.AutoField(primary_key=True)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)
    action_date=models.DateField(auto_now_add=True)
    action_type=models.CharField(max_length=50)
    value = models.DecimalField(max_digits=15,decimal_places=2)
    detail=models.CharField(max_length=50)

class ETF(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )


class ETFConstituent(models.Model):
    const_id
    etf_id = models.OneToOneField(ETF)
    iid = models.ForeignKey(Instrument)
    start_date=models.DateField()
    end_date=models.DateField()
    weight = models.DecimalField(max_digits=1,decimal_places=6)

class Equity(models.Model):
    iid = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)



class FX(models.Model):
    instrument = models.OneToOneField(
        Instrument,
        on_delete=models.CASCADE,
        primary_key=True    
    )
    fid = models.ForeignKey(Currency,on_delete=models.CASCADE)

class PriceAction(models.Model):
    price_id =models.BigIntegerField(primary_key=True)
    price_timestamp=models.DateTimeField(db_index=True)
    price_open =models.DecimalField(decimal_places=2)
    price_high =models.DecimalField(decimal_places=2)
    price_low =models.DecimalField(decimal_places=2)
    price_close=models.DecimalField(decimal_places=2)
    volume=models.DecimalField(max_digits=15,decimal_places=2,null=True)

class FinancialStatement(models.Model):
    statement_id = models.BigAutoField(primary_key=True)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)
    statement_type= models.CharField(max_length=50)
    period_type=models.CharField(max_length=50)
    fiscal_year=models.IntegerField()
    statement_date=models.DateField()

class FinancialMetric(models.Model):
    metric_id = models.IntegerField(primary_key=True)
    statement_id = models.ForeignKey(FinancialStatement,on_delete=models.CASCADE)
    cid = models.ForeignKey(Company,on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=50)
    metric_value=models.DecimalField(max_digits=15,decimal_places=2)

