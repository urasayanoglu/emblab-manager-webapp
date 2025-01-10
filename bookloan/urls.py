from django.urls import path
from . import views

urlpatterns = [
    # Main bookloan page for both booking tables and loaning items
    path('', views.bookloan_view, name='bookloan'),

    # User-specific lists (only for logged-in users)
    path('my-bookings/', views.booking_list, name='booking-list'),
    path('my-loans/', views.loan_list, name='loan-list'),

    # Detailed views for individual bookings and loans (only for logged-in users)
    path('booking/<int:pk>/', views.booking_detail, name='booking-detail'),
    path('loan/<int:pk>/', views.loan_detail, name='loan-detail'),
    path('availability/<int:table_number>/<str:day>/', views.get_table_availability_view,
         name='get_day_availability'),  # TODO: AJAX view, needs further implementation

    # Edit and cancel bookings
    path('booking/edit/<int:pk>/', views.edit_booking, name='edit-booking'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel-booking'),

    # Edit, cancel, and return loans
    path('loan/edit/<int:pk>/', views.edit_loan, name='edit-loan'),
    path('loan/cancel/<int:pk>/', views.cancel_loan, name='cancel-loan'),
    path('loan/return/<int:pk>/', views.return_loan, name='return-loan'),
]
