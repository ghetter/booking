from django.urls import path
from booking.views import AudienceListView, CampusListView, AudienceDetailView


urlpatterns = [
    path('', CampusListView.as_view(), name='campus_list_view'),
    path('<int:campus>/', AudienceListView.as_view(), name='audience_list_view'),
    path('<int:campus>/<int:audience_id>', AudienceDetailView.as_view(), name='audience_detail'),
]