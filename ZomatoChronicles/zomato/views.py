
from django.shortcuts import render,redirect
from .menu import get_menu
import random

def display_menu(request):
    menu = get_menu()
    return render(request, 'menu.html', {'menu': menu})

All_orders = []

def add_dish(request):
    if request.method == 'POST':
        dish_id = len(get_menu()) + 1  # Generate a new dish ID
        dish_name = request.POST['name']
        dish_price = float(request.POST['price'])
        dish_available = request.POST.get('available') == 'on'
        
        new_dish = {
            'name': dish_name,
            'price': dish_price,
            'available': dish_available,
        }
        
        menu = get_menu()
        menu[dish_id] = new_dish
        
        return redirect('menu')  # Redirect back to the menu
    return render(request, 'add_dish.html')

def remove_dish(request, dish_id):
    menu = get_menu()
    if dish_id in menu:
        del menu[dish_id]
    return redirect('menu') 

def update_availability(request, dish_id):
    menu = get_menu()
    if dish_id in menu:
        menu[dish_id]['available'] = not menu[dish_id]['available']
    return redirect('menu') 

def take_order(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        dish_ids = request.POST.getlist('dish_ids')
        
        menu = get_menu()
        order = {
            'order_id':random.randint(1111,9999),
            'customer_name': customer_name,
            'dishes': [menu[int(dish_id)] for dish_id in dish_ids],
            'status': 'received',
        }
        All_orders.append(order)
        # Process the order and perform necessary operations
        
        return redirect('menu')  # Redirect back to the menu
    menu = get_menu()
    return render(request, 'take_order.html', {'menu': menu})

def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST['new_status']
        for data in All_orders:
            if data['order_id'] == order_id:
                data['status'] = new_status
                return redirect('menu')  # Redirect back to the menu
    menu = get_menu()
    return render(request, 'update_order_status.html', {'menu': menu, 'order_id': order_id})

def review_orders(request):
    if request.method == 'POST':
        filter_status = request.POST.get('new_status', 'all')
        if filter_status != 'all':
            filtered_orders = [order for order in All_orders if order['status'] == filter_status]
        else:
            filtered_orders = All_orders
    else:
        filtered_orders = All_orders

    return render(request, 'review_orders.html', {'all_orders': All_orders, 'filtered_orders': filtered_orders})
