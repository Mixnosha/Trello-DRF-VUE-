from rest_framework import serializers

from boardsApp.service import get_slug_board
from commentApp.models import Status
from commentApp.serializers import StatusViewSerializer
from workSpacesApp.models import WorkSpaces
from boardsApp.models import Boards
from userApp.models import CustomUser
from workSpacesApp.service import get_slug


class ViewBoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ['id', 'title', 'background']


class BoardCreateSerializer(serializers.ModelSerializer):
    """ Создание доски для рабочего пространства"""
    slug = serializers.CharField(required=False)
    status = StatusViewSerializer(required=False)

    class Meta:
        model = Boards
        fields = ['title', 'status', 'slug']

    def create(self, validated_data):
        adm_user = CustomUser.objects.get(user__username=self.context['request'].user)
        board = Boards.objects.create(
            **validated_data,
            slug=get_slug_board(validated_data.get('title'))
        )
        board.admin_users.add(adm_user.id)
        board.title = board.title
        board.save()
        wk = WorkSpaces.objects.get(id=self.context['request'].POST['wk_id'])
        wk.boards.add(board.id)
        wk.save()
        return board


class BoardViewSerializers(serializers.ModelSerializer):
    """Просмотр всех досок пользователя """

    class Meta:
        model = Boards
        fields = ['id', 'title', 'background']


class BoardUpdateSerializers(serializers.ModelSerializer):
    """ Обновление Доски """
    slug = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    status = StatusViewSerializer(required=False)

    class Meta:
        model = Boards
        fields = ['status', 'title', 'slug', 'description']

    def update(self, instance, validated_data):
        print(validated_data.get('status'))
        if (new_title := validated_data.get('title', instance.title)) != instance.title:
            instance.title = new_title
            instance.slug = get_slug_board(new_title)
        instance.description = validated_data.get('description', instance.description)
        if 'status' in validated_data:
            instance.status = Status.objects.get(title=validated_data['status']['title'])
        instance.save()
        return instance
