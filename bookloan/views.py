from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse
# For complex queries in Django ORM, it might be necessary to use Q objects
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Table, TableBooking, LoanItem
from inventory.models import InventoryItem, Category
from datetime import datetime, timedelta


@login_required
def get_table_availability_view(request, table_number, day):
    """
    View to retrieve availability slots for a specific table on a given day.
    """
    table = get_object_or_404(Table, number=table_number)
    try:
        day_date = datetime.strptime(day, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format.'}, status=400)

    available_slots = get_table_availability(table, day_date)
    slots_data = [{'start': str(slot[0]), 'end': str(slot[1])}
                  for slot in available_slots]
    return JsonResponse({'available_slots': slots_data})


def get_table_availability(table, day):
    """
    Helper function to determine available time slots for a table on a given day.
    """
    opening_time = table.bookable_start_time
    closing_time = table.bookable_end_time

    # Get all bookings for the table on the given day
    bookings = TableBooking.objects.filter(
        table=table,
        booking_start__date=day
    ).order_by('booking_start')

    # Generate available slots (each slot is one hour)
    available_slots = []
    current_time = datetime.combine(day, opening_time)
    closing_datetime = datetime.combine(day, closing_time)

    while current_time < closing_datetime:
        next_time = current_time + timedelta(hours=1)
        # Check if the slot is available (not overlapping with any booking)
        if not bookings.filter(
            booking_start__lt=next_time,
            booking_end__gt=current_time
        ).exists():
            available_slots.append((current_time.time(), next_time.time()))
        current_time = next_time

    return available_slots


def bookloan_view(request):
    """
    View for handling table bookings and inventory item loans.
    """
    today = timezone.now().date()
    selected_day = today

    if request.method == "GET" and 'selected_day' in request.GET:
        selected_day_str = request.GET.get('selected_day')
        try:
            selected_day = datetime.strptime(
                selected_day_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date selected.")
            selected_day = today

    # Validate that selected day is not in the past
    if selected_day < today:
        messages.error(request, "You cannot select a past day.")
        selected_day = today

    # Validate that selected day is not on a weekend
    if selected_day.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
        messages.error(request, "You cannot select a weekend day.")
        selected_day = today

    # Fetch all active tables and their availability
    tables = Table.objects.filter(is_active=True)
    tables_availability = [
        {
            'table': table,
            'availability': get_table_availability(table, selected_day),
            'color': 'green' if get_table_availability(table, selected_day) else 'red'
        }
        for table in tables
    ]

    # Handle table booking request
    if request.method == "POST" and 'table_number' in request.POST:
        table_number = request.POST.get('table_number')
        booking_start = datetime.strptime(
            request.POST.get('booking_start'), '%Y-%m-%dT%H:%M')
        booking_end = datetime.strptime(
            request.POST.get('booking_end'), '%Y-%m-%dT%H:%M')

        # Make datetime objects timezone aware if ajax is used to dynamically update the booking times of a future date
        booking_start = timezone.make_aware(
            booking_start, timezone.get_current_timezone())
        booking_end = timezone.make_aware(
            booking_end, timezone.get_current_timezone())

        # Check if the booking is for a past date
        if booking_start < timezone.now():
            messages.error(request, "You cannot book a table in the past.")
            return redirect('bookloan')

        # Check if booking is on a weekend
        if booking_start.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
            messages.error(
                request, "You cannot book a table on a weekend day.")
            return redirect('bookloan')

        if booking_end <= booking_start:
            messages.error(request, "End time must be after start time.")
            return redirect('bookloan')

        # Ensure booking is on the same day
        if booking_start.date() != booking_end.date():
            messages.error(
                request, "Booking must start and end on the same day.")
            return redirect('bookloan')

        # Get the selected table object
        table = get_object_or_404(Table, number=table_number)

        # Ensure that the booking is valid
        try:
            new_booking = TableBooking(
                table=table,
                user=request.user,
                booking_start=booking_start,
                booking_end=booking_end
            )
            new_booking.clean()  # Validation check
            new_booking.save()
            messages.success(request, f"Table {table.number} booked successfully from {
                             booking_start} to {booking_end}.")
            return redirect('bookloan')
        except ValidationError as e:
            messages.error(request, e)

    # Handle loaning item request
    if request.method == "POST" and 'item_id' in request.POST:
        item_id = request.POST.get('item_id')
        loan_start_str = request.POST.get('loan_start')
        return_due_str = request.POST.get('return_due')

        try:
            loan_start = datetime.strptime(loan_start_str, '%Y-%m-%d').date()
            return_due = datetime.strptime(return_due_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid loan start or return date.")
            return redirect('bookloan')

        # Validate that the loan start date is not in the past
        if loan_start < today:
            messages.error(request, "You cannot loan an item in the past.")
            return redirect('bookloan')

        if return_due <= loan_start:
            messages.error(
                request, "Return due date must be after the loan start date.")
            return redirect('bookloan')

        # Get the selected item object
        item = get_object_or_404(InventoryItem, id=item_id)

        # Check if item is available for loan
        if item.quantity <= 0:
            messages.error(request, f"Item '{
                           item.name}' is currently unavailable for loan due to insufficient quantity.")
            return redirect('bookloan')

        # Ensure that the loan is valid
        try:
            new_loan = LoanItem(
                item=item,
                user=request.user,
                loan_start=loan_start,
                return_due=return_due
            )
            new_loan.save()

            # Decrement item quantity
            item.quantity -= 1
            item.save()

            messages.success(request, f"Item '{item.name}' loaned successfully from {
                             loan_start} to {return_due}.")
            return redirect('bookloan')
        except ValidationError as e:
            messages.error(request, e)

    # Variables for loaning items
    categories = Category.objects.filter(parent_category__isnull=True)
    selected_category_slug = request.GET.get('category', None)
    selected_item_id = request.GET.get('item', None)
    search_query = request.GET.get('search', None)

    subcategories = []
    items = InventoryItem.objects.none()  # Initialize as empty QuerySet
    selected_item = None

    # If a category is selected, filter by that category
    if selected_category_slug:
        selected_category = get_object_or_404(
            Category, slug=selected_category_slug)
        subcategories = selected_category.subcategories.all()
        items = InventoryItem.objects.filter(
            category=selected_category, can_be_loaned=True, quantity__gt=0)

    # Handle item search
    if search_query:
        search_query = search_query.strip()
        items_by_name = InventoryItem.objects.filter(
            name__icontains=search_query, can_be_loaned=True)
        items_by_category = InventoryItem.objects.filter(
            category__name__icontains=search_query, can_be_loaned=True)

        # Combine items found by name and by category, avoiding duplicates by using union
        items = items_by_name.union(items_by_category)

    # Handle selected table booking
    selected_table_number = request.GET.get('table_number', None)
    if selected_table_number:
        try:
            selected_table_number = int(
                selected_table_number)  # Convert to integer
        except ValueError:
            selected_table_number = None

    # Handle selected item details
    if selected_item_id:
        selected_item = get_object_or_404(InventoryItem, id=selected_item_id)

    context = {
        'tables_availability': tables_availability,
        'categories': categories,
        'subcategories': subcategories,
        'items': items,
        'selected_item': selected_item,
        'search_query': search_query,
        'selected_table_number': selected_table_number,
        'selected_day': selected_day
    }

    return render(request, 'bookloan/bookloan.html', context)


@login_required
def booking_list(request):
    """
    View to list the logged-in user's bookings.
    """
    bookings = TableBooking.objects.filter(
        user=request.user).order_by('-booking_start')
    return render(request, 'bookloan/booking-list.html', {'bookings': bookings, 'now': now()})


@login_required
def loan_list(request):
    """
    View to list the logged-in user's loans.
    """
    loans = LoanItem.objects.filter(user=request.user).order_by('-loan_start')
    return render(request, 'bookloan/loan-list.html', {'loans': loans})


@login_required
def booking_detail(request, pk):
    """
    View to display details of a specific booking only for the logged-in user.
    """
    booking = get_object_or_404(TableBooking, pk=pk)
    if booking.user != request.user and not request.user.is_staff:
        messages.error(
            request, "You do not have permission to view this booking.")
        return redirect('booking-list')
    return render(request, 'bookloan/booking-detail.html', {'booking': booking})


@login_required
def loan_detail(request, pk):
    """
    View to display details of a specific loan only for the logged-in user.
    """
    loan = get_object_or_404(LoanItem, pk=pk)
    if loan.user != request.user and not request.user.is_staff:
        messages.error(
            request, "You do not have permission to view this loan.")
        return redirect('loan-list')
    return render(request, 'bookloan/loan-detail.html', {'loan': loan})


@login_required
def edit_booking(request, pk):
    """
    View to edit a booking only for the logged-in user.
    """
    booking = get_object_or_404(TableBooking, pk=pk)
    if booking.user != request.user:
        messages.error(
            request, "You do not have permission to edit this booking.")
        return redirect('booking-list')
    if booking.booking_start < timezone.now():
        messages.error(
            request, "You cannot edit a booking that has already passed.")
        return redirect('booking-list')

    if request.method == "POST":
        booking_start = datetime.strptime(
            request.POST.get('booking_start'), '%Y-%m-%dT%H:%M')
        booking_end = datetime.strptime(
            request.POST.get('booking_end'), '%Y-%m-%dT%H:%M')
        try:
            booking.booking_start = booking_start
            booking.booking_end = booking_end
            booking.clean()  # Validation check
            booking.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('booking-list')
        except ValidationError as e:
            messages.error(request, e)

    return render(request, 'bookloan/edit-booking.html', {'booking': booking})


@login_required
def cancel_booking(request, pk):
    """
    View to cancel a booking only for the logged-in user.
    """
    booking = get_object_or_404(TableBooking, pk=pk)
    if booking.user != request.user:
        messages.error(
            request, "You do not have permission to cancel this booking.")
        return redirect('booking-list')
    if booking.booking_start < timezone.now():
        messages.error(
            request, "You cannot cancel a booking that has already passed.")
        return redirect('booking-list')

    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('booking-list')


@login_required
def edit_loan(request, pk):
    """
    View to edit a loan only for the logged-in user.
    """
    loan = get_object_or_404(LoanItem, pk=pk)
    if loan.user != request.user:
        messages.error(
            request, "You do not have permission to edit this loan.")
        return redirect('loan-list')
    if loan.is_confirmed:
        messages.error(
            request, "You cannot edit a loan that has already been confirmed.")
        return redirect('loan-list')

    if request.method == "POST":
        loan_start = datetime.strptime(
            request.POST.get('loan_start'), '%Y-%m-%d').date()
        return_due = datetime.strptime(
            request.POST.get('return_due'), '%Y-%m-%d').date()
        loan.loan_start = loan_start
        loan.return_due = return_due
        loan.save()
        messages.success(request, "Loan updated successfully.")
        return redirect('loan-list')

    return render(request, 'bookloan/edit-loan.html', {'loan': loan})


@login_required
def cancel_loan(request, pk):
    """
    View to cancel a loan only for the logged-in user.
    """
    loan = get_object_or_404(LoanItem, pk=pk)
    if loan.user != request.user:
        messages.error(
            request, "You do not have permission to cancel this loan.")
        return redirect('loan-list')
    if loan.is_confirmed:
        messages.error(
            request, "You cannot cancel a loan that has already been confirmed.")
        return redirect('loan-list')

    loan.item.quantity += 1
    loan.item.save()

    loan.delete()
    messages.success(request, "Loan cancelled successfully.")
    return redirect('loan-list')


@login_required
def return_loan(request, pk):
    """
    View to return a loan only for the logged-in user.
    """
    loan = get_object_or_404(LoanItem, pk=pk)
    if loan.user != request.user:
        messages.error(
            request, "You do not have permission to return this loan.")
        return redirect('loan-list')
    if not loan.is_confirmed:
        messages.error(
            request, "You cannot return a loan that has not been confirmed.")
        return redirect('loan-list')

    loan.is_returned = True
    loan.item.quantity += 1
    loan.item.save()
    loan.save()
    messages.success(request, "Loan returned successfully.")
    return redirect('loan-list')
