from django.conf import settings
from django.db.models import Prefetch, Sum
from django.core.cache import cache
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related('user').only(
                'company_name',
                'user__email',
            )
        )
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data

        return response

    # мой вариант: один запрос
    # queryset = Subscription.objects.all().select_related(
    #     'client__user', 'plan',
    # ).prefetch_related('service').only(
    #     'plan_id',
    #     'client__company_name',
    #     'client__user__email',
    #     'service__full_price'
    # )
    serializer_class = SubscriptionSerializer
