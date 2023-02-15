import json

from django.core.paginator import Paginator
from django.db.models import QuerySet, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Homework_28_PD12 import settings
from users.models import User, Location


# ----------------------------------------------------------------------------------------------------------------------
# Users page (CBV)
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a GET request to the UserView
        Returns a list of all User objects in the database as a JSON response

        :param request: The incoming request object
        :return: A JSON response with a list of dictionaries, where each dictionary represents a User object
        """
        super().get(request, *args, **kwargs)
        users: QuerySet = self.object_list.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True))) \
            .prefetch_related("locations").order_by("username")

        paginator = Paginator(users, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users_list: list[dict] = [{
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
            "total_ads": user.total_ads,
        } for user in page_obj]

        return JsonResponse({
            "items": users_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }, safe=False, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single User instance

        :param request: The incoming request object
        :return: JSON response with Category data
        """
        super().get(request, *args, **kwargs)
        user: User = get_object_or_404(User, pk=kwargs["pk"])

        return JsonResponse({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": list(user.locations.all().values_list("name", flat=True))
        }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields: list[str] = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a POST request to the UserView. Creates a new User object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the newly created User object
        """
        super().post(request, *args, **kwargs)

        try:
            user_data = json.loads(request.body)

            user: User = User.objects.create(
                username=user_data.get("username"),
                password=user_data.get("password"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                role=user_data.get("role"),
                age=user_data.get("age"),
            )

            for location in user_data.get("locations"):
                location_obj, _ = Location.objects.get_or_create(name=location, defaults={
                    "lat": 11.111111, "lng": 22.111111})
                user.locations.add(location_obj)
            user.save()

            return JsonResponse({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(user.locations.all().values_list("name", flat=True))
            }, status=200)
        except Exception:
            return JsonResponse({"error": "Invalid request"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields: list[dict] = ["username", "first_name", "last_name", "role", "age", "locations"]

    def put(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a PUT request to the UserView. Update a User object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the updated User object
        """
        super().post(request, *args, **kwargs)

        try:
            user_data = json.loads(request.body)

            self.object.username = user_data.get("username")
            self.object.password = user_data.get("password")
            self.object.first_name = user_data.get("first_name")
            self.object.last_name = user_data.get("last_name")
            self.object.age = user_data.get("age")

            for location in user_data.get("locations"):
                try:
                    location_obj = Location.objects.get(id=location)
                except Location.DoesNotExist:
                    return JsonResponse({"error": "Location does not found"}, status=404)
                self.object.locations.add(location_obj)
            self.object.save()
        except Exception:
            return JsonResponse({"error": "Invalid request"}, status=400)

        return JsonResponse({
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(self.object.locations.all().values_list("name", flat=True))
        }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url: str = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a DELETE request to the UserView. Delete a User object in the database

        :param request: The incoming request object
        :return: A JSON response with a successful delete status
        """
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})
