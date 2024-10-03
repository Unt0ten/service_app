from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    @staticmethod
    def get_price(instance):
        return instance.price

    # Вычисления на уровне питона, оптимизируются полем prefetch
    # @staticmethod
    # def get_price(instance):
    #     full_price = instance.service.full_price
    #     return full_price - full_price * (instance.plan.discount_percent / 100)

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
