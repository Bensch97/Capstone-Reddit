# Generated by Django 2.1.4 on 2019-01-07 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Djeddit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='moderators',
        ),
        migrations.AddField(
            model_name='subreddit',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='mod_subscriptions', to='Djeddit.Profile'),
        ),
    ]
