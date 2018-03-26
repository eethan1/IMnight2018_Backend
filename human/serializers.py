from django.contrib.auth.models import User

from human.models import Profile, Relationship
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('job', 'job_description',
                  'img', 'bio', 'birth_date', 'point')


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'profile')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)

        # update Profile and User sametime
        instance.profile.job = profile_data.get('job', instance.profile.job)
        instance.profile.bio = profile_data.get('bio', instance.profile.bio)
        instance.profile.birth_date = profile_data.get(
            'birth_date', instance.profile.birth_date)
        instance.profile.img = profile_data.get('img', instance.profile.img)

        return instance


class RelationshipSerializer(serializers.ModelSerializer):
    # client = UserDetailsSerializer(required=True)
    performer = UserDetailsSerializer(required=True)
    # 取得未讀的 message
    unread_msg_count = serializers.SerializerMethodField()

    class Meta:
        model = Relationship

        fields = ('performer', 'label', 'created', 'unread_msg_count')
        # fields = '__all__'

    def get_unread_msg_count(self, obj):
        # Message Model的ForeignKey的related_name='messages'
        return obj.messages.filter(readed=False).count()
