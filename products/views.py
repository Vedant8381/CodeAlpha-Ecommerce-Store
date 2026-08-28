# pyright: reportMissingModuleSource=false

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db.models import Avg

from .models import (
    Product,
    CartItem,
    WishlistItem,
    Order,
    OrderItem,
    Review
)


# ==========================================
# HOME / SEARCH / FILTER / SORT
# ==========================================

def home(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    min_price = request.GET.get(
        "min_price",
        ""
    ).strip()

    max_price = request.GET.get(
        "max_price",
        ""
    ).strip()

    sort = request.GET.get(
        "sort",
        ""
    ).strip()


    products = Product.objects.all()


    # SEARCH

    if search_query:

        products = products.filter(
            name__icontains=search_query
        )


    # CATEGORY

    if selected_category:

        products = products.filter(
            category__iexact=selected_category
        )


    # MIN PRICE

    if min_price:

        try:

            products = products.filter(
                price__gte=float(min_price)
            )

        except ValueError:

            min_price = ""


    # MAX PRICE

    if max_price:

        try:

            products = products.filter(
                price__lte=float(max_price)
            )

        except ValueError:

            max_price = ""


    # SORT

    if sort == "price_low":

        products = products.order_by(
            "price"
        )

    elif sort == "price_high":

        products = products.order_by(
            "-price"
        )

    elif sort == "name_az":

        products = products.order_by(
            "name"
        )

    elif sort == "name_za":

        products = products.order_by(
            "-name"
        )

    else:

        products = products.order_by(
            "-created_at"
        )


    # CART COUNT

    cart_count = sum(
        item.quantity
        for item in CartItem.objects.all()
    )


    # WISHLIST COUNT

    wishlist_count = WishlistItem.objects.count()


    # WISHLIST PRODUCT IDS

    wishlist_ids = set(
        WishlistItem.objects.values_list(
            "product_id",
            flat=True
        )
    )


    # CATEGORY LIST

    categories = (
        Product.objects
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )


    return render(
        request,
        "products/home.html",
        {
            "products": products,

            "cart_count": cart_count,

            "wishlist_count": wishlist_count,

            "wishlist_ids": wishlist_ids,

            "categories": categories,

            "search_query": search_query,

            "selected_category":
                selected_category,

            "min_price": min_price,

            "max_price": max_price,

            "sort": sort,
        }
    )


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews = (
        product.reviews
        .all()
        .order_by("-created_at")
    )

    average_rating = (
        reviews.aggregate(
            average=Avg("rating")
        )["average"]
        or 0
    )

    total_reviews = reviews.count()


    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,

            "reviews": reviews,

            "average_rating": average_rating,

            "total_reviews": total_reviews,
        }
    )


# ==========================================
# ADD PRODUCT REVIEW
# ==========================================

def add_review(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        rating = request.POST.get(
            "rating",
            ""
        ).strip()

        comment = request.POST.get(
            "comment",
            ""
        ).strip()


        if (
            name
            and rating
            and comment
        ):

            try:

                rating = int(rating)


                if 1 <= rating <= 5:

                    Review.objects.create(
                        product=product,

                        name=name,

                        rating=rating,

                        comment=comment
                    )

            except ValueError:

                pass


    return redirect(
        "product_detail",
        product_id=product.id
    )


# ==========================================
# ADD TO CART
# ==========================================

def add_to_cart(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    if product.stock <= 0:

        return redirect("home")


    cart_item, created = (
        CartItem.objects.get_or_create(
            product=product
        )
    )


    if not created:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1


    cart_item.save()


    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# ==========================================
# CART
# ==========================================

def cart(request):

    cart_items = (
        CartItem.objects
        .select_related("product")
        .all()
    )


    total = sum(
        item.product.price *
        item.quantity

        for item in cart_items
    )


    cart_count = sum(
        item.quantity

        for item in cart_items
    )


    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,

            "total": total,

            "cart_count": cart_count,
        }
    )


# ==========================================
# INCREASE QUANTITY
# ==========================================

def increase_quantity(
    request,
    item_id
):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )


    if (
        cart_item.quantity
        < cart_item.product.stock
    ):

        cart_item.quantity += 1

        cart_item.save()


    return redirect("cart")


# ==========================================
# DECREASE QUANTITY
# ==========================================

def decrease_quantity(
    request,
    item_id
):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )


    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()


    return redirect("cart")


# ==========================================
# REMOVE FROM CART
# ==========================================

def remove_from_cart(
    request,
    item_id
):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )


    cart_item.delete()


    return redirect("cart")


# ==========================================
# CHECKOUT
# ==========================================

def checkout(request):

    cart_items = (
        CartItem.objects
        .select_related("product")
        .all()
    )


    if not cart_items.exists():

        return redirect("home")


    total = sum(
        item.product.price *
        item.quantity

        for item in cart_items
    )


    if request.method == "POST":

        customer_name = (
            request.POST.get(
                "customer_name"
            )

            or request.POST.get(
                "name"
            )

            or ""
        ).strip()


        email = (
            request.POST.get(
                "email"
            )

            or ""
        ).strip()


        phone = (
            request.POST.get(
                "phone"
            )

            or ""
        ).strip()


        address = (
            request.POST.get(
                "address"
            )

            or ""
        ).strip()


        city = (
            request.POST.get(
                "city"
            )

            or ""
        ).strip()


        pincode = (
            request.POST.get(
                "pincode"
            )

            or ""
        ).strip()


        payment_method = (
            request.POST.get(
                "payment_method"
            )

            or "Cash on Delivery"
        ).strip()


        # CREATE ORDER

        order = Order.objects.create(

            customer_name=customer_name,

            email=email,

            phone=phone,

            address=address,

            city=city,

            pincode=pincode,

            total_amount=total,

            payment_method=payment_method,

            status="Pending",
        )


        # CREATE ORDER ITEMS

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                product=item.product,

                product_name=item.product.name,

                price=item.product.price,

                quantity=item.quantity,
            )


        # REDUCE PRODUCT STOCK

        for item in cart_items:

            product = item.product


            if product.stock >= item.quantity:

                product.stock -= item.quantity

                product.save()


        # DELETE CART

        cart_items.delete()


        return render(
            request,
            "products/order_success.html",
            {
                "order": order
            }
        )


    return render(
        request,
        "products/checkout.html",
        {
            "cart_items": cart_items,

            "total": total,
        }
    )


# ==========================================
# MY ORDERS
# ==========================================

def my_orders(request):

    orders = (
        Order.objects
        .all()
        .order_by("-created_at")
    )


    return render(
        request,
        "products/my_orders.html",
        {
            "orders": orders
        }
    )


# ==========================================
# ORDER DETAIL
# ==========================================

def order_detail(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id
    )


    order_items = (
        order.items
        .select_related("product")
        .all()
    )


    return render(
        request,
        "products/order_detail.html",
        {
            "order": order,

            "order_items": order_items,
        }
    )


# ==========================================
# CANCEL ORDER
# ==========================================

def cancel_order(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id
    )


    if request.method == "POST":

        if order.status in [
            "Pending",
            "Confirmed"
        ]:

            order.status = "Cancelled"

            order.save()


    return redirect(
        "my_orders"
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin_dashboard(request):

    # ==============================
    # BASIC COUNTS
    # ==============================

    total_products = Product.objects.count()

    total_orders = Order.objects.count()


    # ==============================
    # CUSTOMERS
    # ==============================

    total_customers = (
        Order.objects
        .values("email")
        .distinct()
        .count()
    )


    # ==============================
    # INVENTORY STATUS
    # ==============================

    in_stock_products = Product.objects.filter(
        stock__gt=5
    ).count()


    low_stock_count = Product.objects.filter(
        stock__gt=0,
        stock__lte=5
    ).count()


    out_of_stock_products = Product.objects.filter(
        stock=0
    ).count()


    # LOW STOCK PRODUCT LIST

    low_stock_products = (
        Product.objects
        .filter(
            stock__gt=0,
            stock__lte=5
        )
        .order_by("stock")[:10]
    )


    # ==============================
    # ORDER STATUS
    # ==============================

    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()


    confirmed_orders = Order.objects.filter(
        status="Confirmed"
    ).count()


    shipped_orders = Order.objects.filter(
        status="Shipped"
    ).count()


    delivered_orders = Order.objects.filter(
        status="Delivered"
    ).count()


    cancelled_orders = Order.objects.filter(
        status="Cancelled"
    ).count()


    # ==============================
    # TOTAL SALES
    # ONLY DELIVERED ORDERS
    # ==============================

    total_sales = sum(

        order.total_amount

        for order in Order.objects.filter(
            status="Delivered"
        )
    )


    # ==============================
    # RECENT ORDERS
    # ==============================

    recent_orders = (
        Order.objects
        .all()
        .order_by("-created_at")[:10]
    )


    # ==============================
    # DASHBOARD
    # ==============================

    return render(
        request,
        "products/admin_dashboard.html",
        {

            "total_products":
                total_products,

            "total_orders":
                total_orders,

            "total_customers":
                total_customers,

            "in_stock_products":
                in_stock_products,

            "low_stock_count":
                low_stock_count,

            "out_of_stock_products":
                out_of_stock_products,

            "low_stock_products":
                low_stock_products,

            "pending_orders":
                pending_orders,

            "confirmed_orders":
                confirmed_orders,

            "shipped_orders":
                shipped_orders,

            "delivered_orders":
                delivered_orders,

            "cancelled_orders":
                cancelled_orders,

            "total_sales":
                total_sales,

            "recent_orders":
                recent_orders,
        }
    )


# ==========================================
# ADD TO WISHLIST
# ==========================================

def add_to_wishlist(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    WishlistItem.objects.get_or_create(
        product=product
    )


    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


# ==========================================
# REMOVE FROM WISHLIST
# ==========================================

def remove_from_wishlist(
    request,
    product_id
):

    WishlistItem.objects.filter(
        product_id=product_id
    ).delete()


    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "wishlist"
        )
    )


# ==========================================
# WISHLIST
# ==========================================

def wishlist(request):

    wishlist_items = (
        WishlistItem.objects
        .select_related("product")
        .order_by("-created_at")
    )


    wishlist_count = (
        WishlistItem.objects.count()
    )


    cart_count = sum(
        item.quantity

        for item in CartItem.objects.all()
    )


    return render(
        request,
        "products/wishlist.html",
        {
            "wishlist_items":
                wishlist_items,

            "wishlist_count":
                wishlist_count,

            "cart_count":
                cart_count,
        }
    )