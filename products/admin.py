from django.contrib import admin  # pyright: ignore[reportMissingModuleSource]

try:
    from django.utils.html import format_html  # pyright: ignore[reportMissingModuleSource]
except ImportError:  # pragma: no cover
    def format_html(format_string, *args, **kwargs):
        if args or kwargs:
            return format_string.format(*args, **kwargs)
        return format_string

from .models import (
    Product,
    CartItem,
    WishlistItem,
    Order,
    OrderItem,
)


# =========================================================
# PRODUCT ADMIN
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "product_name",
        "category",
        "price_display",
        "stock_display",
        "created_at",
    )

    list_display_links = (
        "product_name",
    )

    search_fields = (
        "name",
        "category",
        "description",
    )

    list_filter = (
        "category",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
    )

    fieldsets = (

        (
            "📦 Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                )
            }
        ),

        (
            "💰 Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                )
            }
        ),

        (
            "🖼️ Product Image",
            {
                "fields": (
                    "image",
                )
            }
        ),

        (
            "🕒 System Information",
            {
                "fields": (
                    "created_at",
                )
            }
        ),

    )

    @admin.display(
        description="Product"
    )
    def product_name(self, obj):

        return format_html(
            '<strong>{}</strong>',
            obj.name
        )

    @admin.display(
        description="Price",
        ordering="price"
    )
    def price_display(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.price
        )

    @admin.display(
        description="Stock",
        ordering="stock"
    )
    def stock_display(self, obj):

        if obj.stock == 0:

            return format_html(
                '<span class="stock-badge stock-out">'
                'Out of Stock'
                '</span>'
            )

        elif obj.stock <= 5:

            return format_html(
                '<span class="stock-badge stock-low">'
                '{} left'
                '</span>',
                obj.stock
            )

        return format_html(
            '<span class="stock-badge stock-good">'
            '{} available'
            '</span>',
            obj.stock
        )


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(
    admin.TabularInline
):

    model = OrderItem

    extra = 0

    can_delete = False

    readonly_fields = (
        "product",
        "product_name",
        "price",
        "quantity",
        "item_total",
    )

    fields = (
        "product_name",
        "price",
        "quantity",
        "item_total",
    )

    @admin.display(
        description="Total"
    )
    def item_total(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.price * obj.quantity
        )


# =========================================================
# ORDER ADMIN
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_display",
        "city",
        "total_display",
        "status_badge",
        "payment_display",
        "created_display",
    )

    list_display_links = (
        "order_number",
        "customer_display",
    )

    search_fields = (
        "customer_name",
        "email",
        "phone",
        "city",
        "pincode",
    )

    list_filter = (
        "status",
        "payment_method",
        "city",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    date_hierarchy = "created_at"

    inlines = (
        OrderItemInline,
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (

        (
            "📦 Order Information",
            {
                "fields": (
                    "status",
                    "payment_method",
                    "total_amount",
                    "created_at",
                )
            }
        ),

        (
            "👤 Customer Information",
            {
                "fields": (
                    "customer_name",
                    "email",
                    "phone",
                )
            }
        ),

        (
            "📍 Delivery Address",
            {
                "fields": (
                    "address",
                    "city",
                    "pincode",
                )
            }
        ),

    )

    @admin.display(
        description="Order"
    )
    def order_number(self, obj):

        return format_html(
            '<strong>#{}</strong>',
            obj.id
        )

    @admin.display(
        description="Customer"
    )
    def customer_display(self, obj):

        return format_html(
            '<strong>{}</strong><br>'
            '<small>{}</small>',
            obj.customer_name,
            obj.email
        )

    @admin.display(
        description="Total",
        ordering="total_amount"
    )
    def total_display(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.total_amount
        )

    @admin.display(
        description="Status",
        ordering="status"
    )
    def status_badge(self, obj):

        status_classes = {
            "Pending": "status-pending",
            "Confirmed": "status-confirmed",
            "Shipped": "status-shipped",
            "Delivered": "status-delivered",
            "Cancelled": "status-cancelled",
        }

        css_class = status_classes.get(
            obj.status,
            "status-pending"
        )

        return format_html(
            '<span class="order-status {}">'
            '{}'
            '</span>',
            css_class,
            obj.status
        )

    @admin.display(
        description="Payment"
    )
    def payment_display(self, obj):

        return format_html(
            '<span class="payment-badge">'
            '💵 {}'
            '</span>',
            obj.payment_method
        )

    @admin.display(
        description="Created",
        ordering="created_at"
    )
    def created_display(self, obj):

        return obj.created_at.strftime(
            "%d %b %Y, %I:%M %p"
        )


# =========================================================
# CART ITEM ADMIN
# =========================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "quantity",
        "cart_total",
    )

    search_fields = (
        "product__name",
    )

    list_filter = (
        "product",
    )

    @admin.display(
        description="Cart Total"
    )
    def cart_total(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.product.price * obj.quantity
        )


# =========================================================
# WISHLIST ADMIN
# =========================================================

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "created_at",
    )

    search_fields = (
        "product__name",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# ORDER ITEM ADMIN
# =========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product_name",
        "price",
        "quantity",
        "item_total",
    )

    search_fields = (
        "product_name",
        "order__customer_name",
        "order__email",
    )

    list_filter = (
        "order__status",
    )

    readonly_fields = (
        "order",
        "product",
        "product_name",
        "price",
        "quantity",
    )

    @admin.display(
        description="Total"
    )
    def item_total(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.price * obj.quantity
        )