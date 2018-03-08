from django.contrib.auth.models import User

from rest_framework import serializers

from human.models import Profile, Relationship


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'job', 'img', 'bio', 'birth_date', 'point')


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)

        # update Profile and User sametime
        instance.profile.nickname = profile_data.get(
            'nickname', instance.profile.nickname)
        instance.profile.job = profile_data.get('job', instance.profile.job)
        instance.profile.bio = profile_data.get('bio', instance.profile.bio)
        instance.profile.birth_date = profile_data.get(
            'birth_date', instance.profile.birth_date)
        instance.profile.img = profile_data.get('img', instance.profile.img)

        return instance


class RelationshipSerializer(serializers.ModelSerializer):
    # client = UserDetailsSerializer(required=True)
    performer = UserDetailsSerializer(required=True)

    class Meta:
        model = Relationship

        fields = ('performer', 'label', 'created')
        # fields = '__all__'
