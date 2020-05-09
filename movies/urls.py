from rest_framework.routers import DefaultRouter

from movies.views import GhibliMovies

router = DefaultRouter()

router.register(r"", GhibliMovies, basename="movies")

urlpatterns = router.urls
