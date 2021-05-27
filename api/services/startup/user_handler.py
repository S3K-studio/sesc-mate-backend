from api.models.user import User


class UserHandler:
    __user_id: int
    __user: User

    def __init__(self, user_id):
        self.__user_id = user_id

    def get_user_from_db(self) -> bool:
        try:
            self.__user = User.objects.get(vk_user_id=self.__user_id)
            return True
        except User.DoesNotExist:
            return False

    def get_group(self) -> int:
        return self.__user.group
