from rest_framework import serializers

from counselling.serializers.AboutSerializer import AboutSerializer
from counselling.models import Counsellor
from account.serializers import UserSerializer

class CounsellorSerializer(serializers.ModelSerializer):
    about = AboutSerializer()
    user = UserSerializer()
    
    class Meta:
        model = Counsellor
        fields = [
            "id",
            'user', 'about'
        ]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        from counselling.models import Counsellor

        counsellor = Counsellor.objects.create_counsellor(**validated_data)
        return counsellor