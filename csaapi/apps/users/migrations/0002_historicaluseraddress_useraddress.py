# Generated by Django 3.2.5 on 2021-07-20 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('addressbasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.addressbasemodel')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
            bases=('common.addressbasemodel',),
        ),
        migrations.CreateModel(
            name='HistoricalUserAddress',
            fields=[
                ('addressbasemodel_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='common.addressbasemodel')),
                ('id', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=36)),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Updated at')),
                ('address_street', models.CharField(max_length=64)),
                ('address_additional', models.CharField(max_length=64)),
                ('address_city', models.CharField(max_length=48)),
                ('address_state', models.CharField(blank=True, choices=[('AL', 'Alabama '), ('AK', 'Alaska '), ('AZ', 'Arizona '), ('AR', 'Arkansas '), ('CA', 'California '), ('CO', 'Colorado '), ('CT', 'Connecticut '), ('DC', 'District of Columbia '), ('DE', 'Delaware '), ('FL', 'Florida '), ('GA', 'Georgia '), ('HI', 'Hawaii '), ('ID', 'Idaho '), ('IL', 'Illinois '), ('IN', 'Indiana '), ('IA', 'Iowa '), ('KS', 'Kansas '), ('KY', 'Kentucky '), ('LA', 'Louisiana '), ('ME', 'Maine '), ('MD', 'Maryland '), ('MA', 'Massachusetts '), ('MI', 'Michigan '), ('MN', 'Minnesota '), ('MS', 'Mississippi '), ('MO', 'Missouri '), ('MT', 'Montana '), ('NE', 'Nebraska '), ('NV', 'Nevada '), ('NH', 'New Hampshire '), ('NJ', 'New Jersey '), ('NM', 'New Mexico '), ('NY', 'New York '), ('NC', 'North Carolina '), ('ND', 'North Dakota '), ('OH', 'Ohio '), ('OK', 'Oklahoma '), ('OR', 'Oregon '), ('PA', 'Pennsylvania '), ('RI', 'Rhode Island '), ('SC', 'South Carolina '), ('SD', 'South Dakota '), ('TN', 'Tennessee '), ('TX', 'Texas '), ('UT', 'Utah '), ('VT', 'Vermont '), ('VA', 'Virginia '), ('WA', 'Washington '), ('WV', 'West Virginia '), ('WI', 'Wisconsin '), ('WY', 'Wyoming ')], max_length=2, null=True)),
                ('address_zipcode', models.CharField(max_length=10)),
                ('address_cross_streets', models.CharField(blank=True, max_length=128, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user address',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]