from django.db.models import Prefetch, F, Sum
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
    ).annotate(
        price=F('service__full_price') - F('service__full_price') *
              F('plan__discount_percent') / 100.00
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
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
