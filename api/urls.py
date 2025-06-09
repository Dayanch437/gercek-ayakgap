from django.urls import include, path

urlpatterns = [
    path("users/", include("api.user.urls")),
    path("auth/", include("api.auth.urls")),
    path("store/", include("api.store.urls")),
    path("cart/", include("api.cart.urls")),
    path("contact/", include("api.contact.urls")),
]
