from django.test import TestCase
from django.http import HttpRequest
from django.test.client import Client
import uuid

from util.models.shortcuts import User
from account.auth import login, encrypt, Token
from account.serializers import UserSerializer
from counselling.models import Counsellor
from counselling.serializers import CounsellorSerializer

class BaseTestCase(TestCase):
    fixtures = ["sampleData.json"]
    user1_data = {
        "email": "topper.390903@example.com",
        "password": "topperlkfeowkfe"
    }
    user2_data = {
        "email": "sabji.mandi.3903029@example.com",
        "password": "slkvlwkefjoewfjkewlfje"
    }

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(**cls.user1_data, wallet={"activate_wallet": False})
        cls.user2 = User.objects.create_user(**cls.user2_data, wallet={"activate_wallet": False})

        return super().setUpTestData()



class UserAuthedTestCase(BaseTestCase):
    authed_user_data = {
        "email": "pompa",
        "password": "pompa"
    }


    @classmethod
    def setUpTestData(cls):
        cls.authed_user = User.objects.create_user(**cls.authed_user_data, wallet={"activate_wallet": False})
        cls.auther_user_serialized_data = UserSerializer(cls.authed_user) 

        *_, data = login(HttpRequest(), cls.authed_user, in_body=True, in_cookie=False)
        cls.access_token = data.get("access_token")
        cls.refresh_token = data.get("refresh_token")
        cls.auth_header = f"Bearer {cls.access_token}"

        cls.authed_client = Client(HTTP_AUTHORIZATION=cls.auth_header)
        cls.authed_client.cookies[Token.TOKEN_REFRESH_KEY] = encrypt(cls.refresh_token)

    def create_user(self, data=None):
        data = data or {
            "email": uuid.uuid4().__str__() + "@example.com",
            "password": uuid.uuid4().__str__()
        }

        # Create User
        user = User.objects.create_user(**data, wallet={"activate_wallet": False})
        return user

    def get_auth_client(self, user):
        *_, data = login(HttpRequest(), user, in_body=True, in_cookie=False)
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        auth_header = f"Bearer {access_token}"

        client = Client(HTTP_AUTHORIZATION=auth_header)
        client.cookies[Token.TOKEN_REFRESH_KEY] = encrypt(refresh_token)

        return (client, access_token, refresh_token, auth_header)




class CounsellorAuthedTestCase(UserAuthedTestCase):
    
    ABOUT_DATA_TEMPLATE = {
        "introduction": "I am a dedicated counsellor with over 5 years of experience in helping individuals navigate personal and professional challenges.",
        "qualification": "Master's Degree in Psychology, Certified Cognitive Behavioral Therapist (CBT)",
        "speciality": "Career Guidance, Mental Health Support, Relationship Counselling",
        "methodology": "I use a client-centered approach, integrating Cognitive Behavioral Therapy (CBT) and solution-focused techniques to provide personalized guidance."
    }


    SLOTS_DATA_TEMPLATE = [    
        {
            "from_time": "10:00",
            "duration": "02:00:00",
            "fee": 100,
            "days": 127,
        },
        {
            "from_time": "20:00",
            "duration": "00:33:00",
            "fee": 93,
            "days": 127,
        },
        {
            "from_time": "23:00",
            "duration": "01:00:00",
            "fee": 250,
            "days": 127,
        },
    ] 
    
    counsellor1_data = {
        "user": {
            "email": "monosita.320930@exmaple.com",
            "password": "flwlkejlfkweflewkjflkewj"
        },
        "about": {
            "introduction": "I am a dedicated counsellor with over 5 years of experience in helping individuals navigate personal and professional challenges.",
            "qualification": "Master's Degree in Psychology, Certified Cognitive Behavioral Therapist (CBT)",
            "speciality": "Career Guidance, Mental Health Support, Relationship Counselling",
            "methodology": "I use a client-centered approach, integrating Cognitive Behavioral Therapy (CBT) and solution-focused techniques to provide personalized guidance."
        },
        "slots": [
            {
                "fee": 3560,
                "from_time": "10:00",
                "duration": 60
            },
            {
                "fee": 1000,
                "from_time": "11:30",
                "duration": 30
            },
            {
                "fee": 200,
                "from_time": "20:00",
                "duration": 20
            }
        ]
    }

    @classmethod
    def setUpTestData(cls):
        cls.counsellor_user = User.objects.create_user(**cls.counsellor1_data.get("user"), wallet={"activate_wallet": False})
        cls.counsellor = Counsellor.objects.create_counsellor(cls.counsellor_user, cls.counsellor1_data.get("about"))
        cls.create_slots(cls, cls.counsellor, cls.counsellor1_data.get("slots", []))

        (
            cls.authed_counsellor_client, cls.authed_access_token,
            cls.counsellor_refresh_token, cls.counsellor_auth_header
        ) = cls.get_auth_client(cls, cls.counsellor_user)
        
        return super().setUpTestData()

    def create_counsellor(self, user_data=None, counsellor_data=None):
        user = self.create_user(user_data)

        counsellor = Counsellor.objects.create_counsellor(user, self.ABOUT_DATA_TEMPLATE)

        return counsellor

    def create_slots(self, counsellor, slots=None):
        slots = slots or self.SLOTS_DATA_TEMPLATE

        for slot in slots:
            slot["duration"] = str(int(slot["duration"]) * 60)
            counsellor.create_slot(**slot)
            # counsellor.save()
        return counsellor



class BaseAuthedTestCase(CounsellorAuthedTestCase):
    pass