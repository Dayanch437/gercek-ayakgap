from django.urls import path, include

urlpatterns = [
    path("users/",include("api.user.urls")),
    path('auth/', include("api.auth.urls")),
    path('store/', include("api.store.urls")),
    path('cart/', include("api.cart.urls")),
]

