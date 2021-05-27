from typing import Dict
from .user_handler import UserHandler


class ResponseJson:
    setup_didnt_completed: Dict[str, bool] = {
        'success': True,
        'setupCompleted': False
    }

    missing_headers: Dict = {
        'success': False,
        'message': 'Missing headers'
    }

    invalid_signature: Dict = {
        'success': False,
        'message': 'Invalid signature'
    }

    bad_request = {
        'success': False,
        'message': 'Bad request'
    }

    @staticmethod
    def get_normal_response(user: UserHandler, schedule, announcements) -> Dict:
        return {
            'success': True,
            'setupCompleted': True,
            'groupId': user.get_group(),
            'timetable': schedule,
            'announcements':  announcements
        }
