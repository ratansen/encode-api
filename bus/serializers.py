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
    
    # def update(self, instance, validated_data):
    #         # Update the  instance
    #     instance.destination_from = validated_data['destination_from']
    #     instance.save()

    #     # Delete any detail not included in the request
    #     owner_ids = [item['owner_id'] for item in validated_data['owners']]
    #     for owner in cars.owners.all():
    #         if owner.id not in owner_ids:
    #             owner.delete()

    #     # Create or update owner 
    #     for owner in validated_data['owners']:
    #         ownerObj = Owner.objects.get(pk=item['id'])
    #         if ownerObje:
    #             ownerObj.some_field=item['some_field']
    #             ....fields...
    #         else:
    #            ownerObj = Owner.create(car=instance,**owner)
    #         ownerObj.save()

    #     return instance


