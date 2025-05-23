from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls
#/api/notifications/               → List/create
#/api/notifications/?is_read=false → Unread only
#/api/notifications/<id>/mark_as_read/ → Mark one as read
