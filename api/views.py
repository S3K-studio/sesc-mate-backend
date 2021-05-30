from logging import getLogger

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from vk_api import VkApi

from utils import group_choices
from .models import User, CustomAnnouncement
from .serializers import UserSerializer
from .services.cache import get_parsed_schedule, get_parsed_announcements
from .services.startup.header_handler import HeaderHandler
from .services.startup.response_json import ResponseJson
from .services.startup.user_handler import UserHandler

logger = getLogger('logdna')
vk_api = VkApi(token=settings.VK_API_SECRET_KEY)


class ScheduleView(APIView):
    """Получение расписания"""

    def get(self, request: Request) -> Response:
        """Возвращаем расписание. В запросе параметрами должны быть переданы Класс и День недели"""
        if 'day' in request.query_params and 'group' in request.query_params and \
                request.query_params['day'].isdigit() and request.query_params[
            'group'].isdigit() and 1 <= int(request.query_params['day']) <= 7 and int(
            request.query_params['group']) in group_choices.groups_dict:
            force_update = 'force_update' in request.query_params and request.query_params[
                'force_update'] == '1'
            schedule = get_parsed_schedule(
                request.query_params['day'],
                request.query_params['group'],
                force_update
            )

            try:
                return Response(schedule, status=status.HTTP_200_OK)
            except Exception as e:
                logger.exception(e)
                return Response({
                    'success': False,
                    'message': type(e).__name__
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WeekScheduleView(APIView):
    """Получение расписания на неделю"""

    def get(self, request: Request) -> Response:
        """Возвращаем расписание. В запросе параметрами должен быть передан Класс"""
        if 'group' in request.query_params and request.query_params['group'].isdigit() and int(
                request.query_params['group']) in group_choices.groups_dict:
            force_update = 'force_update' in request.query_params and request.query_params[
                'force_update'] == '1'
            schedule = [
                get_parsed_schedule(
                    day,
                    request.query_params['group'],
                    force_update
                ) for day in range(1, 7)
            ]

            try:
                return Response(schedule, status=status.HTTP_200_OK)
            except Exception as e:
                logger.exception(e)
                return Response({
                    'success': False,
                    'message': type(e).__name__
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def post(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        if not ('group' in request.data and request.data['group'] in group_choices.groups_dict):
            return Response(response_json.bad_request, status=status.HTTP_400_BAD_REQUEST)

        """Working with user"""
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if not is_user_in_db:
            serializer = UserSerializer()
            params = {
                'user_ids': user_id,
                'fields': 'photo_100,sex'
            }
            try:
                user_data_from_vk = vk_api.method('users.get', params)[0]
            except Exception as e:
                logger.exception(e)
                return Response({
                    'success': False,
                    'message': type(e).__name__
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            validated_data = {
                'vk_user_id': user_id,
                'group': request.data['group'],
                'first_name': user_data_from_vk['first_name'],
                'last_name': user_data_from_vk['last_name'],
                'sex': user_data_from_vk['sex'],
                'profile_picture_url': user_data_from_vk['photo_100']
            }
            try:
                serializer.create(validated_data=validated_data)
                return Response(validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.exception(e)
                return Response({
                    'success': False,
                    'message': type(e).__name__
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'success': False,
                'message': 'User already in db'
            }, status=status.HTTP_409_CONFLICT)

    def put(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        if not ('group' in request.data and request.data['group'] in group_choices.groups_dict):
            return Response(response_json.bad_request, status=status.HTTP_400_BAD_REQUEST)

        """Working with user"""
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if is_user_in_db:
            user_object_from_db = User.objects.get(
                vk_user_id=user_id)  # User object for serializing
            validated_data = {
                'vk_user_id': user_id,
                'group': request.data['group']
            }

            serializer = UserSerializer(
                user_object_from_db, data=validated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(validated_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Bad request'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        """Working with user"""
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if not is_user_in_db:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user_object_from_db = User.objects.get(vk_user_id=user_id)
        user_object = {
            'vk_user_id': user_object_from_db.vk_user_id,
            'group': user_object_from_db.group
        }
        return Response(user_object, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        response_json = ResponseJson()

        """Working with headers"""
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        """Working with user"""
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if not is_user_in_db:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user_object_from_db = User.objects.get(vk_user_id=user_id)
        user_object = {
            'vk_user_id': user_object_from_db.vk_user_id,
            'group': user_object_from_db.group
        }
        try:
            user_object_from_db.delete()
            return Response(user_object, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({
                'success': False,
                'message': type(e).__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StartupInfo(APIView):
    """Get startup info"""

    def get(self, request: Request) -> Response:
        response_json = ResponseJson()

        # Working with headers
        header_handler = HeaderHandler(request.META)

        if not header_handler.is_headers_valid():
            return Response(response_json.missing_headers, status=status.HTTP_400_BAD_REQUEST)

        if not header_handler.is_valid():
            return Response(response_json.invalid_signature, status=status.HTTP_401_UNAUTHORIZED)

        # Working with user
        user_id: int = int(header_handler.vk_header['vk_user_id'])
        user: UserHandler = UserHandler(user_id)
        is_user_in_db: bool = user.get_user_from_db()

        if 'day' not in request.query_params or not request.query_params['day'].isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        day: int = request.query_params['day']

        if not is_user_in_db:
            return Response(response_json.setup_didnt_completed, status=status.HTTP_200_OK)

        announcements = get_parsed_announcements()
        custom_announcements = CustomAnnouncement.objects.order_by(
            '-is_pinned')
        serialized_announcements = list(map(
            lambda announcement: {
                'header': announcement.header,
                'content': announcement.content,
                'trustedOrigin': True
            },
            custom_announcements
        ))

        force_update = 'force_update' in request.query_params and request.query_params[
            'force_update'] == '1'
        schedule = get_parsed_schedule(day, user.get_group(), force_update)
        try:
            return Response(response_json.get_normal_response(user, schedule,
                                                              serialized_announcements + announcements),
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({
                'success': False,
                'message': type(e).__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
