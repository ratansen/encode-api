from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from bus.models import Bus, Driver


class BusDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"
        extra_kwargs = {
            'phone': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
        depth = 1


class BusSerializer(serializers.ModelSerializer):
    driver = BusDriverSerializer()

    class Meta:
        model = Bus
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        driver = validated_data.pop('driver')
        if not Driver.objects.filter(**driver):
            driver = Driver.objects.create(**driver)
        else:
            driver = Driver.objects.filter(**driver).first()
        bus = Bus.objects.create(driver=driver, **validated_data)
        bus.save()
        return bus
    
    def update(self, instance, validated_data):
        
        instance.destination_from = validated_data['destination_from']
        instance.destination_to = validated_data['destination_to']
        
        instance.date_of_departure = validated_data['date_of_departure']
        instance.time_of_departure = validated_data['time_of_departure']
        
        instance.date_of_arrival = validated_data['date_of_arrival']
        instance.time_of_arrival = validated_data['time_of_arrival']
        
        driver = validated_data.pop('driver')
        if not Driver.objects.filter(phone=driver['phone']):
            driver = Driver.objects.create(**driver)
        else:
            driver = Driver.objects.filter(**driver).first()
            
        instance.driver = driver

        return instance


