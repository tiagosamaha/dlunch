from django.db import models


class PostgresBinaryField(models.Field):
    def db_type(self):
        return "bytea"
