from rest_framework.routers import DefaultRouter
from .views import BookListView

router = DefaultRouter()
router.register(r'', BookListView, basename='books') 

app_name = 'books'

urlpatterns = router.urls