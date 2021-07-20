from django.contrib.postgres.fields import ArrayField
from django.db import models


from apps.common import models as common_models
from apps.users import models as users_models


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# PRODUCT
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Season(common_models.HistoryMixin, common_models.AbstractBaseModel):

    name = models.CharField(max_length=32, help_text="Brief descriptive name of season")
    date_deliveries_begin = models.DateField(
        "First Delivery Week", null=True, blank=True
    )
    date_deliveries_end = models.DateField("Last Delivery Week", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "date_deliveries_begin",
        ]


class Product(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Product available for member selection"""

    name = models.CharField(
        max_length=32, help_text="Brief descriptive name of product"
    )
    weeks_available = ArrayField(models.PositiveSmallIntegerField(default=0))
    cost = models.DecimalField(
        "Cost",
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "name",
        ]


class Menu(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Available products for season"""

    name = models.CharField(max_length=48)

    products = models.ManyToManyField(Product, blank=True)
    season = models.OneToOneField(Season, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["season"]


class Subscription(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Order by Member for season's deliveries"""

    DELIVERY_CHOICES = (("MEMBER", "Member Address"), ("LOCATION", "Location"))

    STATUS_CHOICES = (
        ("CURRENT", "Current"),
        ("OUTSTANDING", "Outstanding"),
        ("PAID", "Paid-in-Full"),
    )

    deliver_to = models.CharField(
        max_length=12, choices=DELIVERY_CHOICES, default="MEMBER"
    )

    remaining_balance = models.DecimalField(
        "Remaining subscription balance",
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="CURRENT")
    total_charges = models.DecimalField(
        "Total subscription charges",
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )

    products = models.ManyToManyField(Product, blank=True)
    season = models.ForeignKey(
        Season, on_delete=models.RESTRICT, related_name="subscriptions"
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscriptions",
    )
    user = models.ForeignKey(
        users_models.User, on_delete=models.RESTRICT, related_name="subscriptions"
    )

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "season",
            "user",
        ]


class SubscriptionAddress(common_models.AddressBaseModel):
    """Address for deliveries (location or user)"""

    subscription = models.OneToOneField(
        Subscription, on_delete=models.CASCADE, related_name="address"
    )

    def __str__(self):
        return f"{self.subscription}"

    class Meta:
        ordering = [
            "subscription",
        ]


class Installment(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Partial payment for subscription"""

    date_due = models.DateField(null=False, blank=False)
    charges_due = models.DecimalField(
        "Installment due",
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )

    datetime_paid = models.DateTimeField(null=False, blank=False)
    charges_paid = models.DecimalField(
        "Installment paid",
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )
    transaction_reference = models.CharField(max_length=48, null=True, blank=True)

    subscription = models.ForeignKey(
        Subscription, on_delete=models.RESTRICT, related_name="installments"
    )

    def __str__(self):
        return f"{self.subscription}, {self.date_due.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "subscription",
            "datetime_paid",
        ]


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# LOCATION
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Location(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Distribution point for shares"""

    name = models.CharField(max_length=48)
    open_to_public = models.BooleanField(default=False)
    open_only_to = models.CharField(max_length=96, null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(
        default=100, help_text="Maximum number of members allowed to pickup shares"
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "name",
        ]


class LocationSubscribedCount(
    common_models.HistoryMixin, common_models.AbstractBaseModel
):
    """Count of members signed up for location, per season"""

    count = models.PositiveSmallIntegerField(default=0)
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="subscribed_count_by_location"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="subscribed_count_by_season"
    )

    def __str__(self):
        return f"{self.location.name} member count, {self.season}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "location",
        ]


class LocationAddress(common_models.AddressBaseModel):
    """Address of Location"""

    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, related_name="address"
    )

    def __str__(self):
        return f"{self.location.name}"

    class Meta:
        ordering = [
            "location",
        ]


class LocationCoordinates(common_models.HistoryMixin, common_models.AbstractBaseModel):
    """Coordinates of Location"""

    coordinates_resolved = models.BooleanField(default=False)
    coordinate_longitude = models.DecimalField(
        "Longitude",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        default=0.000000,
    )
    coordinate_latitude = models.DecimalField(
        "Latitude",
        max_digits=8,
        decimal_places=6,
        null=True,
        blank=True,
        default=0.000000,
    )

    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, related_name="coordinates"
    )

    def __str__(self):
        return f"{self.location.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "location",
        ]


class LocationDelivery(common_models.HistoryMixin, common_models.AbstractBaseModel):
    CHOICES = (("YES", "Yes"), ("NO", "No"), ("UNKNOWN", "Unknown"))

    completed = models.BooleanField(default=False)

    deliver_to_address_street = models.TextField(null=True, blank=True)
    is_dock = models.BooleanField(default=False)
    delivery_hours = models.CharField(max_length=36, null=True, blank=True)
    dock_restrictions = models.TextField(default="", blank=True)
    provide_security_with_license_for_driver = models.BooleanField(
        "Do we need to provide truck driver's license?",
        max_length=7,
        choices=CHOICES,
        default="UNKNOWN",
    )
    service_elevator_restrictions = models.TextField(default="", blank=True)
    stairs_for_delivery_pickup = models.BooleanField(
        "Does delivery/pickup have to negotiate stairs?",
        max_length=7,
        choices=CHOICES,
        default="UNKNOWN",
    )
    stairs_for_delivery_pickup_number = models.CharField(
        max_length=32, null=True, blank=True
    )

    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, related_name="delivery_details"
    )

    def __str__(self):
        return str(self.location.name)

    class Meta:
        verbose_name_plural = "Location delivery details"


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# DELIVERIES
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Order(common_models.HistoryMixin, common_models.AbstractBaseModel):

    date_delivery = models.DateField(null=False, blank=False)

    location = models.ForeignKey(
        Location, on_delete=models.RESTRICT, related_name="orders"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.RESTRICT, related_name="orders"
    )

    def __str__(self):
        return f"{self.user.full_name or self.user.username}, {self.date_delivery.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "date_delivery",
            "subscription",
        ]


class OrderLine(common_models.HistoryMixin, common_models.AbstractBaseModel):
    quantity = models.PositiveSmallIntegerField(default=1)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="lines"
    )

    def __str__(self):
        return f"{self.order.date_delivery} {self.order.product} {self.order.subscription.user}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["order", "product"]


class Delivery(common_models.HistoryMixin, common_models.AbstractBaseModel):
    date = models.DateField()

    orders = models.ManyToManyField(Order, blank=True, related_name="delivery_detail")

    def __str__(self):
        return str(self.location.name)

    class Meta:
        verbose_name_plural = "Deliveries"


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# SETTINGS
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


class Settings(common_models.AbstractBaseModel):
    """Public site settings"""

    def __str__(self):
        return f"Settings for Farm app"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Settings"
