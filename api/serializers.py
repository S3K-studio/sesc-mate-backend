from rest_framework import serializers

from .models.user import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    class Meta:
        fields = ('id', 'vk_user_id', 'group', 'first_name', 'last_name', 'profile_picture_url', 'sex')
        model = User

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance: User, validated_data):
        instance.vk_user_id = validated_data.get('vk_user_id', instance.vk_user_id)
        instance.group = validated_data.get('group', instance.group)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_picture_url = validated_data.get('profile_picture_url', instance.profile_picture_url)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.save()
        return instance
