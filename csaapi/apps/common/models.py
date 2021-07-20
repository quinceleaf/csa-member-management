from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy


import csv
from uuid import uuid4


from simple_history.models import HistoricalRecords
import ulid


def generate_ulid():
    return str(ulid.ULID())


class HistoryMixin(models.Model):
    history = HistoricalRecords(inherit=True)

    def get_history(self):
        return_data = []
        all_histories = self.history.all()
        for history in all_histories:
            delta = history.diff_against(history.prev_record)
            for change in delta.changes:
                if change.old:
                    comment = (
                        f"{change.field} changed from {change.old} to {change.new}"
                    )
                else:
                    comment = f"{change.field} set to {change.new}"
            return_data.append(
                {
                    "date": history.history_date,
                    "user": history.history_user,
                    "comment": comment,
                }
            )
        return return_data

    class Meta:
        abstract = True


class AbstractBaseModel(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=uuid4,
        unique=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in self.__class__._meta.fields
        ]

    class Meta:
        abstract = True


class ImmutableBaseModel(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=36,
        default=uuid4,
        unique=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self))
            for field in self.__class__._meta.fields
        ]

    class Meta:
        abstract = True


class AddressBaseModel(HistoryMixin, AbstractBaseModel):
    """Common Fields of Address Models"""

    POSTAL_STATE_CHOICES = (
        ("AL", "Alabama "),
        ("AK", "Alaska "),
        ("AZ", "Arizona "),
        ("AR", "Arkansas "),
        ("CA", "California "),
        ("CO", "Colorado "),
        ("CT", "Connecticut "),
        ("DC", "District of Columbia "),
        ("DE", "Delaware "),
        ("FL", "Florida "),
        ("GA", "Georgia "),
        ("HI", "Hawaii "),
        ("ID", "Idaho "),
        ("IL", "Illinois "),
        ("IN", "Indiana "),
        ("IA", "Iowa "),
        ("KS", "Kansas "),
        ("KY", "Kentucky "),
        ("LA", "Louisiana "),
        ("ME", "Maine "),
        ("MD", "Maryland "),
        ("MA", "Massachusetts "),
        ("MI", "Michigan "),
        ("MN", "Minnesota "),
        ("MS", "Mississippi "),
        ("MO", "Missouri "),
        ("MT", "Montana "),
        ("NE", "Nebraska "),
        ("NV", "Nevada "),
        ("NH", "New Hampshire "),
        ("NJ", "New Jersey "),
        ("NM", "New Mexico "),
        ("NY", "New York "),
        ("NC", "North Carolina "),
        ("ND", "North Dakota "),
        ("OH", "Ohio "),
        ("OK", "Oklahoma "),
        ("OR", "Oregon "),
        ("PA", "Pennsylvania "),
        ("RI", "Rhode Island "),
        ("SC", "South Carolina "),
        ("SD", "South Dakota "),
        ("TN", "Tennessee "),
        ("TX", "Texas "),
        ("UT", "Utah "),
        ("VT", "Vermont "),
        ("VA", "Virginia "),
        ("WA", "Washington "),
        ("WV", "West Virginia "),
        ("WI", "Wisconsin "),
        ("WY", "Wyoming "),
    )

    address_street = models.CharField(max_length=64)
    address_additional = models.CharField(max_length=64)
    address_city = models.CharField(max_length=48)
    address_state = models.CharField(
        max_length=2, choices=POSTAL_STATE_CHOICES, null=True, blank=True
    )
    address_zipcode = models.CharField(max_length=10)
    address_cross_streets = models.CharField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
