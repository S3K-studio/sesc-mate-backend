import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.group_choices import reversed_groups_defaultdict

from .functions import *
from .models import AliceUser
from .messages import Messages


class AliceView(APIView):
    def post(self, request):
        messages = Messages()
        try:
            request: dict = json.loads(request.body.decode('utf-8'))
            print(request)
            user_id: str = request['session']['user']['user_id']
            intents = request['request']['nlu']['intents']
            user_is_new = is_new_user(user_id)

            if user_is_new['new']:
                user = AliceUser(user_id=user_id)
                user.save()
                return Response(create_response(messages.START, end=False))

            if 'set_group' in intents:
                set_group_intent = intents['set_group']

                raw_group = set_group_intent['slots']['group']['value'].replace(' ', '')

                if reversed_groups_defaultdict[raw_group] is None:
                    return Response(create_response(messages.UNEXISTING_GROUP, end=False))

                else:
                    group_number = reversed_groups_defaultdict[raw_group]

                    user = AliceUser.objects.get(user_id=user_id)
                    user.group_number = group_number
                    user.save()

                    return Response(create_response(messages.you_set_group(raw_group), end=False))

            if "schedule_with_group" in intents:
                schedule_intents = intents["schedule_with_group"]
                row_day: str = schedule_intents['slots']['day']['value']
                row_group: str = schedule_intents['slots']['group']['value'].replace(' ', '')

                return Response(create_response(messages.schedule_message(row_day, row_group), end=True))

            if 'my_schedule' in intents:
                user_group = user_has_group(user_id)
                my_schedule = intents["my_schedule"]
                raw_day: str = my_schedule['slots']['day']['value']

                if user_group:
                    return Response(create_response(messages.schedule_message(raw_day, user_group), end=True))
                else:
                    return Response(create_response(messages.NO_GROUP, end=False))

            if len(intents) == 0:
                raw_message = request['request']['command']
                if raw_message.strip() == '':
                    return Response(create_response(messages.START, end=False))

            print('no intends')
        except Exception as e:
            print(e)
