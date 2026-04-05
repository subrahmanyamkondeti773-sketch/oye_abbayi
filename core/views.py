from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Profile
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Product
    template_name = 'core/home.html'
    context_object_name = 'featured_products'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        cat_id = self.request.GET.get('category_id')
        
        queryset = Product.objects.all().order_by('-id')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if cat_id:
            queryset = queryset.filter(category_id=cat_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'core/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'core/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.stock < 1:
            messages.error(request, "Product is out of stock.")
            return redirect('home')

        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
            
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f"Only {product.stock} items available in stock.")
            
        cart_item.save()

        messages.success(request, f"{product.name} added to cart.")
        return redirect('cart')


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        action = request.POST.get('action')

        if action == 'increase':
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
        return redirect('cart')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('home')

        return render(request, 'core/checkout.html', {'cart': cart})

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('home')

        # Safe profile handling
        profile, created = Profile.objects.get_or_create(user=request.user)

        if not profile.address or not profile.phone_number:
            messages.warning(request, "Please update your profile before checkout.")
            return redirect('profile')

        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price(),
            address=profile.address,
            phone_number=profile.phone_number,
            pin_code=profile.pin_code
        )

        for item in cart.items.all():

            if item.product.stock < item.quantity:
                messages.error(
                    request,
                    f"Not enough stock for {item.product.name}"
                )
                return redirect('cart')

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Reduce stock safely
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_history')


class BuyNowView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.stock < 1:
            messages.error(request, "Product is out of stock.")
            return redirect('home')

        profile, _ = Profile.objects.get_or_create(user=request.user)

        order = Order.objects.create(
            user=request.user,
            total_amount=product.price,
            address=profile.address or '',
            phone_number=profile.phone_number or '',
            pin_code=profile.pin_code or ''
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

        product.stock -= 1
        product.save()

        return redirect('order_confirm', order_id=order.id)


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class OrderConfirmView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_confirm.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        # Only the order owner can see this
        return Order.objects.filter(user=self.request.user)


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        profile.address = request.POST.get('address', '')
        profile.phone_number = request.POST.get('phone_number', '')
        profile.pin_code = request.POST.get('pin_code', '')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    # Pre-fill form with existing data
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone_number': profile.phone_number,
        'address': profile.address,
        'pin_code': profile.pin_code,
    }
    form = UserProfileForm(initial=initial_data)

    return render(request, 'core/profile.html', {
        'profile': profile,
        'form': form,
    })

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        Profile.objects.update_or_create(
            user=user,
            defaults={
                'address': form.cleaned_data.get('address', ''),
                'phone_number': form.cleaned_data.get('phone_number', ''),
                'pin_code': form.cleaned_data.get('pin_code', ''),
            }
        )

        messages.success(self.request, "Account created successfully. Please login.")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')