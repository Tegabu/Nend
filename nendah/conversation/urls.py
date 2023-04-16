from django.urls import path


from .import views

app_name = 'conversation'


urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.chat, name='chat'),
    path('new/<int:listing_pk>/', views.new_conversation, name='new')
]
