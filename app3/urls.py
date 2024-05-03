
# urls.py
from django.urls import path
from .views import ConversationsListView,ConversationsDetail,ConversationsStart,send_message

urlpatterns = [
    path('ConversationsList/', ConversationsListView.as_view(), name='api_conversations_list'),
    path('start/<uuid:user_id>/', ConversationsStart.as_view(), name='api_conversations_start'),
    path('ConversationsDetail/<uuid:pk>/', ConversationsDetail.as_view(), name='ConversationsDetail'),
    path('messages/', send_message.as_view()),
]
