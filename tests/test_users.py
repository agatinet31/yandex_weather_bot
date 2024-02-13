from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="Dmitry",
            email="dmitry@mail.ru",
            password="qweras123",
            telegram="check_username",
            whatsapp="+78005553535",
        )

    def test_username(self):
        """Username совпадает с ожидаемым."""
        user = UserModelTest.user
        username = user.username
        self.assertEqual(username, "Dmitry")

    def test_whatsapp(self):
        """Whatsapp совпадает с ожидаемым."""
        user = UserModelTest.user
        whatsapp = user.whatsapp
        self.assertEqual(whatsapp, "+78005553535")

    def test_telegram(self):
        """Telegram совпадает с ожидаемым."""
        user = UserModelTest.user
        telegram = user.telegram
        self.assertEqual(telegram, "check_username")

    def test_email(self):
        """Email совпадает с ожидаемым."""
        user = UserModelTest.user
        email = user.email
        self.assertEqual(email, "dmitry@mail.ru")

    def test_role_user(self):
        """Role нового юзера совпадаест с ожидаемым."""
        user = UserModelTest.user
        role = user.role
        self.assertEqual(role, User.USER)


class UserCreate(TestCase):
    def test_create_user_with_forbidden_username(self):
        """
        Проверка валидности username.

        Невозможность создать username == "me".
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="me", email="admin@admin.com", password="qweasd123"
            )

    def test_create_admin(self):
        """Role админа совпадает с ожидаемым."""
        user = User.objects.create_admin_user(
            username="admin", email="admin@admin.com", password="qweasd123"
        )
        role = user.role
        self.assertEqual(role, User.ADMIN)

    def test_create_superadmin(self):
        """Role суперадмина совпадает с ожидаемым."""
        user = User.objects.create_superadmin_user(
            username="admin", email="admin@admin.com", password="qweasd123"
        )
        role = user.role
        self.assertEqual(role, User.SUPERADMIN)


class UserViewTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="testPassword",
            telegram="test_telegram",
            whatsapp="+78005553535",
        )
        cls.new_user = User.objects.create_user(
            username="new_user",
            email="newuser@test.com",
            password="testPassword",
        )

    def test_create_user(self):
        """Проверка доступности эндпоинта создания пользователя."""
        count = User.objects.count()
        response = self.client.post(
            reverse("api:user-create"),
            data={
                "username": "test1",
                "email": "test1@test.com",
                "password": "testPassword",
            },
        )
        self.assertEqual(User.objects.count(), count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_profile_for_auth_user(self):
        """Проверка эндпоинта с информацией о пользователе."""
        self.client.force_authenticate(UserViewTest.user)
        response = self.client.get(reverse("api:user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_unavailable_for_unauth(self):
        """Проверка эндпоинта /me для неавторизованного пользователя."""
        response = self.client.get(reverse("api:user-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_with_exists_username(self):
        """Проверка создания пользователя с существующим username."""
        count = User.objects.count()
        response = self.client.post(
            reverse("api:user-create"),
            data={
                "username": "test",
                "email": "test1@test.com",
                "password": "testPassword",
            },
        )
        self.assertEqual(User.objects.count(), count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_exists_email(self):
        """Проверка создания пользователя с существующим email."""
        count = User.objects.count()
        response = self.client.post(
            reverse("api:user-create"),
            data={
                "username": "test1",
                "email": "test@test.com",
                "password": "testPassword",
            },
        )
        self.assertEqual(User.objects.count(), count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_forbidden_username(self):
        """Проверка создания пользователя с username == me."""
        with self.assertRaises(IntegrityError):
            self.client.post(
                reverse("api:user-create"),
                data={
                    "username": "me",
                    "email": "test1@test.com",
                    "password": "testPassword",
                },
            )

    def test_change_username_for_existing(self):
        """Проверка изменения username.

        Пользователь не может поменять свой username
        на тот, что уже есть в базе.
        """
        self.client.force_authenticate(UserViewTest.new_user)
        data = {"username": "test", "email": "newuser@test.com"}
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertNotEqual(
            User.objects.get(pk=self.new_user.pk).username, data["username"]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_username(self):
        """Прооверка возможности изменить свой username."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).username, data["username"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_telegram(self):
        """Проверка возможности добавить или поменять telegram."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "telegram": "new_telegram",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).telegram, data["telegram"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_telegram_for_existing(self):
        """Проверка изменения telegram.

        Пользователь не может добавить или
        поменять свой telegram на уже существующий.
        """
        self.client.force_authenticate(UserViewTest.new_user)
        data = {"telegram": "test_telegram"}
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertNotEqual(
            User.objects.get(pk=self.new_user.pk).telegram, data["telegram"]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_incorrect_telegram(self):
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "telegram": 123,
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertNotEqual(
            User.objects.get(pk=self.user.pk), data["telegram"]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_whatsapp(self):
        """Проверка возможности добавить или поменять whatsapp."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "whatsapp": "+78005553536",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).whatsapp, data["whatsapp"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_whatsapp_for_existing(self):
        """Проверка изменения whatsapp.

        Пользователь не может поменять свой whatsapp на уже существующий.
        """
        self.client.force_authenticate(UserViewTest.new_user)
        data = {
            "whatsapp": "+78005553535",
            "username": "new_user",
            "email": "newuser@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertNotEqual(
            User.objects.get(pk=self.new_user.pk).whatsapp, data["whatsapp"]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_first_name(self):
        """Проверка изменения first_name."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "first_name": "test_first_name",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.get(pk=self.user.pk).first_name,
            data["first_name"],
        )

    def test_change_last_name(self):
        """Проверка изменения last_name."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "last_name": "test_last_name",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.get(pk=self.user.pk).last_name,
            data["last_name"],
        )

    def test_add_phone(self):
        """Проверка добавления телефона."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "phone": "+78005553535",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertEqual(
            User.objects.get(pk=self.user.pk).phone, data["phone"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_incorrect_phone(self):
        """Проверка добавления некорректного номер телефона."""
        self.client.force_authenticate(UserViewTest.user)
        data = {
            "phone": "123",
            "username": "test_user",
            "email": "test@test.com",
            "avatar": "",
        }
        response = self.client.put(
            reverse("api:user-me"),
            data=data,
        )
        self.assertNotEqual(User.objects.get(pk=self.user.pk), data["phone"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
