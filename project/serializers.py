from rest_framework import serializers
from project.models import Statistic


class StatisticSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        exclude = ()


class StatisticSerializer(serializers.ModelSerializer):
    def to_representation(self, i):
        new_data = dict()
        new_data['date'] = i.date
        new_data['views'] = i.views
        new_data['clicks'] = i.clicks
        new_data['cost'] = i.cost
        new_data['cpc'] = i.cost / i.clicks if i.cost and i.clicks and i.clicks != 0 else 0
        new_data['cpm'] = i.cost / i.views * 1000 if i.cost and i.views and i.views != 0 else 0
        return new_data
