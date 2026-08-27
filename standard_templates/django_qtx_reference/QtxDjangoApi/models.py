import uuid
from django.db import models
from QtxDjangoApp import settings


# Create your models here.
class MerchantCodes(models.Model):
    mcc_code = models.AutoField(primary_key=True, db_column="mcc")
    mcc_description = models.TextField(db_column="description")

    class Meta:
        managed = False
        db_table = f"{settings.merchant_codes_table}"
