from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, ConversationMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    ConversationMessageSerializer
)
from app1.models import User

class ConversationsListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
        return Response({'data':serializer.data }, status=status.HTTP_200_OK)
    

# class ConversationsDetail(APIView):
#     def get(self, request, pk):

#         conversation = request.user.conversations.get(pk=pk)
#         conversation_serializer = ConversationDetailSerializer(conversation, many=False)
#         messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)

#         return Response({
#             'conversation': conversation_serializer.data,
#             'messages': messages_serializer.data
#         })

# class ConversationsDetail(APIView):
#     def get(self, request, pk):
       
#         conversation = request.user.conversations.get(pk=pk)
#         conversation_serializer = ConversationDetailSerializer(conversation)
#         print(conversation_serializer.data)
#         messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
#         print('----------------',conversation.messages)
#         return Response({
#             'conversation': conversation_serializer.data,
#             'messages': messages_serializer.data
#         })
class ConversationsDetail(APIView):
    def get(self, request, pk):
        try:
            conversation = request.user.conversations.get(pk=pk)
            conversation_serializer = ConversationDetailSerializer(conversation,many=False)
            print("Conversation data:", conversation_serializer.data)

            messages = conversation.messages.all()
            print("Conversation messages:", messages)

            messages_serializer = ConversationMessageSerializer(messages, many=True)
            
            return Response({
                'conversation': conversation_serializer.data,
                'messages': messages_serializer.data
            })
        except Exception as e:
            print("Error:", e)  
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class send_message(APIView):
      def post(self, request):
        try:
            # Assuming you have authenticated the user and retrieved the authenticated user object
            sent_by = request.user
            
            # Get body, conversation_id, and sent_to_id from the request data
            body = request.data.get('body')
            conversation_id = request.data.get('conversation_id')
            sent_to_id = request.data.get('sent_to_id')
            
            # Check if sent_to_id exists and is not empty
            if not sent_to_id:
                return Response({'error': 'sent_to_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the Conversation corresponding to conversation_id
            conversation = Conversation.objects.get(pk=conversation_id)
            
            # Retrieve the user corresponding to sent_to_id
            sent_to = User.objects.get(pk=sent_to_id)
            
            # Create the ConversationMessage instance
            message = ConversationMessage.objects.create(
                body=body,
                conversation=conversation,
                sent_to=sent_to,
                created_by=sent_by
            )
            
            # Serialize the created message
            message_serializer = ConversationMessageSerializer(message)
            
            return Response({'success': True, 'message': message_serializer.data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print("Error creating message:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# class ConversationsStart(APIView):
#     def get(self, request, user_id):
#         conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

#         if conversations.exists():
#             conversation = conversations.first()
#             return Response({'success': True, 'conversation_id': conversation.id})
#         else:
#             try:
#                 user = User.objects.get(pk=user_id)
#             except User.DoesNotExist:
#                 return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
#             conversation = Conversation.objects.create()
#             conversation.users.add(request.user)
#             conversation.users.add(user)
#             return Response({'success': True, 'conversation_id': conversation.id})

class ConversationsStart(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, uid=user_id)
            user_conversations = Conversation.objects.filter(users=request.user)
            user_conversations_ids = user_conversations.values_list('id', flat=True)

            # Find common conversations between request.user and the user with user_id
            conversations = Conversation.objects.filter(users=user).filter(id__in=user_conversations_ids)
            if conversations.exists():
                conversation = conversations.first()
                return Response({'success': True, 'conversation_id': conversation.id})
            else:
                conversation = Conversation.objects.create()
                conversation.users.add(request.user)
                conversation.users.add(user)
                return Response({'success': True, 'conversation_id': conversation.id})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)