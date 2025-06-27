from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.test.client import Client
from django.http.request import HttpRequest
import uuid
import pytz
from django.conf import settings
import copy
from django.db.models import Q, F

from util.models.shortcuts import User
from account.serializers import UserSerializer
from account.auth import login, Token, encrypt
from util.tests.baseTest import BaseTestCase, BaseAuthedTestCase


class CounsellorsTest(BaseAuthedTestCase):
    fixtures = ["sampleData.json"]
    PAGE_PARAMS = {"page": 1, "size": 5}

    def test_get_counsellors(self):
        response = self.authed_client.get(
            reverse("api:counsellors"), query_params=self.PAGE_PARAMS
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], self.PAGE_PARAMS["page"])
        self.assertEqual(json["size"], self.PAGE_PARAMS["size"])
        self.assertEqual(json["totalItems"], len(json["items"]))

    def test_unauth_get_counsellors(self):
        response = self.client.get(
            reverse("api:counsellors"),
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class CounsellorView(BaseAuthedTestCase):

    def test_get_counsellor(self):
        response = self.authed_client.get(
            reverse("api:counsellor", kwargs={"counsellor_id": self.counsellor.id})
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["id"], self.counsellor.id.__str__())

    def test_unauth_get_counsellor(self):
        response = self.client.get(
            reverse("api:counsellor", kwargs={"counsellor_id": self.counsellor.id})
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_invalid_counsellor(self):
        response = self.authed_client.get(
            reverse("api:counsellor", kwargs={"counsellor_id": uuid.uuid4()})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class CounsellorSlotsTest(BaseAuthedTestCase):
    QUERY_PARAMS = {
        "page": 1,
        "size": 10,
    }

    def test_get_slots(self):
        response = self.authed_counsellor_client.get(
            reverse("api:slots", args=[self.counsellor.id])
        )
        json = response.json()

        self.assertEqual(json["page"], 1)
        self.assertEqual(json["count"], len(json["items"]))

        slot_map = [
            id.__str__() for id in self.counsellor.slots.values_list("id", flat=True)
        ]
        for slot in json["items"]:
            self.assertIn(slot["id"], slot_map)

    def test_get_slots_2(self):
        response = self.authed_counsellor_client.get(
            reverse("api:slots", args=[self.counsellor.id]),
            query_params=self.QUERY_PARAMS,
        )
        json = response.json()

        self.assertEqual(json["page"], self.QUERY_PARAMS["page"])
        self.assertEqual(json["size"], self.QUERY_PARAMS["size"])
        self.assertEqual(json["count"], len(json["items"]))

        slot_map = [
            id.__str__() for id in self.counsellor.slots.values_list("id", flat=True)
        ]
        for slot in json["items"]:
            self.assertIn(slot["id"], slot_map)

    def test_unauth_get_slots(self):
        response = self.client.get(reverse("api:slots", args=[self.counsellor.id]))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_auth_get_slots(self):

        response = self.authed_client.get(
            reverse("api:slots", args=[self.counsellor.id])
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_invalid_counsellor_get_slots(self):
        response = self.authed_counsellor_client.get(
            reverse("api:slots", args=[uuid.uuid4().__str__()])
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_slots(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = self.SLOTS_DATA_TEMPLATE

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(json), counsellor.slots.count())

    def test_create_slots_2_times(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = self.SLOTS_DATA_TEMPLATE

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(json), counsellor.slots.count())

        # Try to create same slots again
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )

        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(len(json), counsellor.slots.count())

    def test_create_slots_in_invalid_order(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = self.SLOTS_DATA_TEMPLATE
        slots[0], slots[1] = slots[1], slots[0]

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(json), counsellor.slots.count())

    def test_create_conflicted_slots(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = [
            {
                "from_time": "11:10",
                "duration": "30",
                "fee": 1000,
            },
            {"from_time": "12:00", "duration": "90", "fee": 1500},
            {
                "from_time": "13:10",
                "duration": "5",
                "fee": 130,
            },
        ]

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )

        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)

    def test_create_slots_conflicts_in_db(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        db_slots = [
            {
                "from_time": "05:00",
                "duration": "60",
                "fee": 132,
            },
            {"from_time": "08:00", "duration": "180", "fee": 132},
        ]
        self.create_slots(counsellor, db_slots)

        slots = [
            {
                "from_time": "10:00",
                "duration": "90",
                "fee": 4302,
            },
            {"from_time": "05:45", "duration": "60", "fee": 300},
        ]

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # import ipdb;ipdb.set_trace()
        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        self.assertEqual(len(db_slots), counsellor.slots.count())

    def test_timezone_of_created_slots(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # change timezone for better clarity (no default behaviour)
        tokyo_tz = pytz.timezone("Asia/Tokyo")
        counsellor.timezone = tokyo_tz
        counsellor.save()

        # Create New slots
        slots = self.SLOTS_DATA_TEMPLATE

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(slots), len(json))

        for created_slot in json:
            self.assertEqual(created_slot["timezone"], tokyo_tz.zone)

    def test_alternate_timezone_of_created_slots(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # change timezone for better clarity (no default behaviour)
        tokyo_tz = pytz.timezone("asia/tokyo")
        counsellor.timezone = tokyo_tz
        counsellor.save()

        # Create New slots
        slots = [
            {
                "from_time": "10:00",
                "duration": "60",
                "fee": 4302,
            },
            {"from_time": "05:45", "duration": "60", "fee": 300},
        ]

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # import ipdb;ipdb.set_trace()
        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(slots), len(json))

        # Check if each one is in there
        for created_slot in json:
            self.assertEqual(created_slot["timezone"], tokyo_tz.zone)

        # Now change timezone
        karachi_tz = pytz.timezone("Asia/Karachi")
        counsellor.timezone = karachi_tz
        counsellor.save()

        new_slots = [{"from_time": "20:40", "duration": "30", "fee": 232}]

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=new_slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(new_slots), len(json))
        self.assertEqual(len(slots) + len(new_slots), counsellor.slots.count())

        # Check if each one is in there
        for created_slot in json:
            self.assertEqual(created_slot["timezone"], karachi_tz.zone)

    def test_alternate_timezone_of_created_slots_and_fetch(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # change timezone for better clarity (no default behaviour)
        tokyo_tz = pytz.timezone("Asia/Tokyo")
        counsellor.timezone = tokyo_tz
        counsellor.save()

        # Create New slots
        slots = [
            {
                "from_time": "10:00",
                "duration": "90",
                "fee": 4302,
            },
            {"from_time": "05:45", "duration": "40", "fee": 300},
        ]

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(slots), len(json))

        # Check if each one is in there
        for created_slot in json:
            self.assertEqual(created_slot["timezone"], tokyo_tz.zone)

        # Check by fetching slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "page": 1,
                "size": settings.MAX_PAGE_SIZE,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["count"], len(json["items"]))
        self.assertEqual(len(slots), json["totalItems"])

        for slot in json["items"]:
            self.assertEqual(slot["timezone"], tokyo_tz.zone)

        # Now change timezone
        karachi_tz = pytz.timezone("Asia/Karachi")
        counsellor.timezone = karachi_tz
        counsellor.save()

        new_slots = [{"from_time": "20:40", "duration": "30", "fee": 232}]

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=new_slots,
        )
        json = response.json()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(new_slots), len(json))
        self.assertEqual(len(slots) + len(new_slots), counsellor.slots.count())

        # Check if each one is in there
        for created_slot in json:
            self.assertEqual(created_slot["timezone"], karachi_tz.zone)

        # Check by fetching slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "page": 1,
                "size": settings.MAX_PAGE_SIZE,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["count"], len(json["items"]))
        self.assertEqual(len(new_slots), json["totalItems"])

        for slot in json["items"]:
            self.assertEqual(slot["timezone"], karachi_tz.zone)

    def test_invalid_payload_create_slots_1(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = copy.deepcopy(self.SLOTS_DATA_TEMPLATE)
        slots[-1]["from_time"] = "2027-03-13 10:00:00"

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(counsellor.slots.count(), 0)

    def test_invalid_payload_create_slots_2(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = copy.deepcopy(self.SLOTS_DATA_TEMPLATE)
        slots[-1]["duration"] = "00:1i0"

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(counsellor.slots.count(), 0)

    def test_invalid_payload_create_slots_3(self):
        # Create counsellor
        counsellor = self.create_counsellor()

        # Create New slots
        slots = copy.deepcopy(self.SLOTS_DATA_TEMPLATE)
        slots[-1]["fee"] = -5

        # Get authed client
        client, *_ = self.get_auth_client(counsellor.user)

        # Create Slots
        response = client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data=slots,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(counsellor.slots.count(), 0)

    def test_create_slots_by_unauth_user(self):

        last_count = self.counsellor.slots.count()
        response = self.client.post(
            reverse("api:slots", args=[self.counsellor.id]),
            content_type="application/json",
            data={"from_time": "01:00", "duration": "30", "fee": 300},
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(last_count, self.counsellor.slots.count())

    def test_create_slots_by_auth_user(self):

        last_count = self.counsellor.slots.count()
        response = self.authed_client.post(
            reverse("api:slots", args=[self.counsellor.id]),
            content_type="application/json",
            data={"from_time": "01:00", "duration": "30", "fee": 300},
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(last_count, self.counsellor.slots.count())

    def test_create_slots_by_different_counsellor(self):
        counsellor = self.create_counsellor()
        last_count = counsellor.slots.count()

        response = self.authed_client.post(
            reverse("api:slots", args=[counsellor.id]),
            content_type="application/json",
            data={"from_time": "01:00", "duration": "30", "fee": 300},
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(last_count, counsellor.slots.count())

    def test_create_slots_by_invalid_counsellor_id(self):

        last_count = self.counsellor.slots.count()
        response = self.authed_client.post(
            reverse("api:slots", args=[uuid.uuid4()]),
            content_type="application/json",
            data={"from_time": "01:00", "duration": "30", "fee": 300},
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(last_count, self.counsellor.slots.count())

    def test_get_slots_filter_days(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except SU, M, Tu
            },
        ]
        self.create_slots(counsellor, slots)

        days_fetch = ["SU"]
        days_bits = [0b1]

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "day": days_fetch,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["totalItems"], 2)

        for slot in json["items"]:
            found = 0
            for day_bit in days_bits:
                found = (slot["days"] & day_bit) == day_bit
                if found:
                    break
            if not found:
                self.fail(f"slot({slot}) was not active in neither of specified days")

    def test_get_slots_filter_days_2(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        days_fetch = ["SA"]
        days_bits = [0b1000000]

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        # import ipdb;ipdb.set_trace()
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "day": days_fetch,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)

        for slot in json["items"]:
            found = 0
            for day_bit in days_bits:
                found = (slot["days"] & day_bit) == day_bit
                if found:
                    break
            if not found:
                self.fail(f"slot({slot}) was not active in neither of specified days")

    def test_get_slots_filter_active(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        # deactivate one slot
        s = counsellor.slots.last()
        s.is_active = False
        s.save()

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]), query_params={"active": True}
        )
        json = response.json()

        # import ipdb;ipdb.set_trace()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["totalItems"], len(slots) - 1)

        for slot in json["items"]:
            self.assertEqual(slot["is_active"], True)

    def test_get_slots_filter_not_active(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        # deactivate one slot
        s = counsellor.slots.last()
        s.is_active = False
        s.save()

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]), query_params={"active": False}
        )
        json = response.json()

        # import ipdb;ipdb.set_trace()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["totalItems"], 1)

        for slot in json["items"]:
            self.assertEqual(slot["is_active"], False)

    def test_get_slots_filter_fee(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={"fee_min": 100, "fee_max": 200},
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["totalItems"], 1)

        for slot in json["items"]:
            self.assertTrue(100 <= slot["fee"] <= 200)

    def test_get_slots_filter_fee_invalid(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "fee_min": 400,
                "fee_max": 10,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)
        self.assertEqual(json["totalItems"], 0)

    def test_get_slots_filter_multiple(self):

        counsellor = self.create_counsellor()

        slots = [
            {
                "from_time": "10:00",
                "duration": 120,
                "fee": 100,
                "days": 1,  # Sunday
            },
            {
                "from_time": "20:00",
                "duration": 33,
                "fee": 93,
                "days": 5,  # Sunday, Tuesday
            },
            {
                "from_time": "23:00",
                "duration": 60,
                "fee": 250,
                "days": 120,  # All except saturday and sunday
            },
        ]
        self.create_slots(counsellor, slots)

        # deactivate one slot
        s = counsellor.slots.last()
        s.is_active = False
        s.save()

        days_params = ["SA", "F", "W"]
        days_bits = [0b1000000, 0b100000, 0b1000]

        # Get auth client with counseller
        client, *_ = self.get_auth_client(counsellor.user)

        # Should fetch 2nd and 3rd slot from slots
        response = client.get(
            reverse("api:slots", args=[counsellor.id]),
            query_params={
                "fee_min": 100,
                "fee_max": 300,
                "active": True,
                "day": days_params,
            },
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json["page"], 1)

        for slot in json["items"]:
            self.assertTrue(100 <= slot["fee"] <= 300)

            found = 0
            for day_bit in days_bits:
                found = (slot["days"] & day_bit) == day_bit
                if found:
                    break
            if not found:
                self.fail(f"slot({slot}) was not active in neither of specified days")


class SlotTest(BaseAuthedTestCase):

    # Get slots
    def test_update_slot_disable(self):
        slot = self.counsellor.slots.all_valids().first()
        slot.is_active = True
        slot.save()

        # Disable one slot
        response = self.authed_counsellor_client.patch(
            reverse("api:slot", args=[self.counsellor.id, slot.id]),
            content_type="application/json",
            data={
                "disable": True,
            },
        )

        slot.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(slot.is_active)

    def test_update_slot_enable(self):

        # Disable an slot programmatically
        slot = self.counsellor.slots.all_valids().last()
        slot.is_active = False
        slot.save()

        # Enable one slot
        response = self.authed_counsellor_client.patch(
            reverse("api:slot", args=[self.counsellor.id, slot.id]),
            content_type="application/json",
            data={
                "disable": False,
            },
        )

        slot.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(slot.is_active)

    def test_update_slot_unauthed(self):

        # Try to update one slot
        response = self.client.patch(
            reverse(
                "api:slot", args=[self.counsellor.id, self.counsellor.slots.last().id]
            ),
            content_type="application/json",
            data={
                "disable": True,
            },
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_slot_unauthorized(self):

        counsellor = self.create_counsellor()
        client, *_ = self.get_auth_client(counsellor.user)

        # Try to update one slot
        response = client.patch(
            reverse(
                "api:slot", args=[self.counsellor.id, self.counsellor.slots.last().id]
            ),
            content_type="application/json",
            data={
                "disable": True,
            },
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_slot_invalid(self):

        # Try to update one slot
        response = self.authed_counsellor_client.patch(
            reverse("api:slot", args=[self.counsellor.id, uuid.uuid4()]),
            content_type="application/json",
            data={
                "disable": True,
            },
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_slot(self):
        slot = self.counsellor.slots.all_valids().first()

        # Delete slot
        response = self.authed_counsellor_client.delete(
            reverse("api:slot", args=[self.counsellor.id, slot.id]),
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(
            self.counsellor.slots.all_valids().filter(id=slot.id).count() <= 0
        )
