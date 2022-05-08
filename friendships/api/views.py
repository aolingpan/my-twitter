from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from friendships.models import Friendship
from django.contrib.auth.models import User
from friendships.api.serializers import (
    FollowerSerializer,
    FollowingSerializer,
    FriendshipSerializerForCreate,
)


class FriendshipViewSet(viewsets.GenericViewSet):
    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all()
    # serializer_class = FriendshipSerializerForCreate(queryset, many=True)

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowerSerializer(friendships, many=True)
        return Response(
            {
                'followers': serializer.data
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        serializer = FollowingSerializer(friendships, many=True)
        return Response(
            {'followings': serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        # self.get_object()
        # if Friendship.objects.filter(from_user=request.user, to_user=pk).exists():
        #     return Response(
        #         {
        #             'success': True,
        #             'duplication': True,
        #         }, status=status.HTTP_201_CREATED
        #     )
        serializer = FriendshipSerializerForCreate(
            data={'from_user_id': request.user.id,
                  'to_user_id': pk,
                  }
        )
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST
            )
        instance = serializer.save()
        return Response(
            FollowingSerializer(instance).data, status=status.HTTP_201_CREATED
        )

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        unfollow_user = self.get_object()
        if request.user.id == unfollow_user.id:
            return Response({
                'success': False,
                'message': 'You can not unfollow yourself',
            }, status=status.HTTP_400_BAD_REQUEST)
        print(pk)
        deleted, _ = Friendship.objects.filter(from_user=request.user, to_user=pk,).delete()
        return Response({
            'succcess': True,
            'deleted': deleted
        })

    def list(self, request):
        return Response({'message': 'this is friendships home page'})