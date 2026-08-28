from django.contrib import admin  # type: ignore[reportMissingModuleSource]
from django.urls import path  # type: ignore[reportMissingModuleSource]

from products import views


urlpatterns = [

    # ==========================================
    # DJANGO ADMIN
    # ==========================================

    path(
        "admin/",
        admin.site.urls
    ),


    # ==========================================
    # HOME
    # ==========================================

    path(
        "",
        views.home,
        name="home"
    ),


    # ==========================================
    # PRODUCT
    # ==========================================

    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    # ADD PRODUCT REVIEW
    path(
        "product/<int:product_id>/review/",
        views.add_review,
        name="add_review"
    ),


    # ==========================================
    # CART
    # ==========================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/increase/<int:item_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:item_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # ==========================================
    # CHECKOUT
    # ==========================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # ==========================================
    # ORDERS
    # ==========================================

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "order/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "cancel-order/<int:order_id>/",
        views.cancel_order,
        name="cancel_order"
    ),


    # ==========================================
    # DASHBOARD
    # ==========================================

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # ==========================================
    # WISHLIST
    # ==========================================

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/add/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

]