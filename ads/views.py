import json
from json import JSONDecodeError

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Homework_28_PD12 import settings
from ads.models import Category, Ad


# ----------------------------------------------------------------------------------------------------------------------
# Start page (FBV)
def index(request) -> JsonResponse:
    """
    Root view that returns a JSON response indicating success

    :param request: The incoming request object
    :return: JSON "OK" status
    """
    return JsonResponse({"status": "ok"}, status=200)


# ----------------------------------------------------------------------------------------------------------------------
# Categories page (CBV)
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a GET request to the CategoryView
        Returns a list of all Category objects in the database as a JSON response

        :param request: The incoming request object
        :return: A JSON response with a list of dictionaries, where each dictionary represents a Category object
        """
        super().get(request, *args, **kwargs)

        categories: QuerySet = self.object_list.order_by("name")

        response: list[dict] = [{
            "id": category.id,
            "name": category.name
        } for category in categories]

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single Category instance

        :param request: The incoming request object
        :return: JSON response with Category data
        """
        super().get(request, *args, **kwargs)

        category = get_object_or_404(Category, pk=kwargs.get("pk"))

        response: dict = {
            "id": category.id,
            "name": category.name
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")  # Отключение проверки токена
class CategoryCreateView(CreateView):
    model = Category

    fields: list[str] = ["name"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a POST request to the CategoryView. Creates a new Category object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the newly created Category object
        """
        try:
            category_data = json.loads(request.body)
            category: Category = Category.objects.create(**category_data)
        except JSONDecodeError:
            return JsonResponse({"error": "Wrong data"}, status=400)

        response: dict = {
            "id": category.id,
            "text": category.name
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields: list[dict] = ["name"]

    def put(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a PUT request to the CategoryView. Update a Category object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the updated Category object
        """
        super().post(request, *args, **kwargs)
        try:
            category_data = json.loads(request.body)
            self.object.name = category_data.get("name")
            self.object.save()
        except JSONDecodeError:
            return JsonResponse({"error": "Wrong data"}, status=400)

        response: dict = {
            "id": self.object.id,
            "name": self.object.name
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url: str = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a DELETE request to the CategoryView. Delete a Category object in the database

        :param request: The incoming request object
        :return: A JSON response with a successful delete status
        """
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# ----------------------------------------------------------------------------------------------------------------------
# Advertisements page (CBV)
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a GET request to the AdView
        Returns a list of all Ad objects in the database as a JSON response

        :param request: The incoming request object
        :return: A JSON response with a list of dictionaries, where each dictionary represents an Ad object
        """
        super().get(request, *args, **kwargs)
        advertisements: QuerySet = self.object_list.select_related("author", "category").order_by("-price")

        paginator = Paginator(advertisements, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        advertisements_list: list[dict] = [{
            "name": advertisement.name,
            "price": advertisement.price,
            "description": advertisement.description,
            "image": advertisement.image.url if advertisement.image else None,
            "author": advertisement.author.username,
            "category": advertisement.category.name
        } for advertisement in page_obj]

        response: dict = {
            "items": advertisements_list,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single Ad instance

        :param request: The incoming request object
        :return: JSON response with Ad data
        """
        super().get(request, *args, **kwargs)
        advertisement: Ad = get_object_or_404(Ad, pk=kwargs.get("pk"))

        response: dict = {
            "name": advertisement.name,
            "price": advertisement.price,
            "description": advertisement.description,
            "image": advertisement.image.url if advertisement.image else None,
            "author": advertisement.author.username,
            "category": advertisement.category.name
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields: list[dict] = ["name", "price", "description", "image", "author_id", "category_id"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a POST request to the AdView. Creates a new Ad object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the newly created Ad object
        """
        try:
            advertisement_data = json.loads(request.body)
            advertisement: Ad = Ad.objects.create(**advertisement_data)
        except JSONDecodeError:
            return JsonResponse({"error": "Wrong data"}, status=400)

        response: dict = {
            "name": advertisement.name,
            "price": advertisement.price,
            "description": advertisement.description,
            "image": advertisement.image.url if advertisement.image else None,
            "author": advertisement.author.username,
            "category": advertisement.category.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields: list[dict] = ["name", "price", "description", "author", "category"]

    def put(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a PUT request to the AdView. Update an Ad object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the updated Ad object
        """
        super().post(request, *args, **kwargs)

        try:
            advertisement_data = json.loads(request.body)
            self.object.name = advertisement_data.get("name")
            self.object.price = advertisement_data.get("price")
            self.object.description = advertisement_data.get("description")
            self.object.author_id = advertisement_data.get("author_id")
            self.object.category_id = advertisement_data.get("category_id")
        except JSONDecodeError:
            return JsonResponse({"error": "Wrong data"}, status=400)

        response: dict = {
            "id": self.object.id,
            "name": self.object.name,
            "description": self.object.description,
            "author": self.object.author.username,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url: str = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a DELETE request to the AdView. Delete an Ad object in the database

        :param request: The incoming request object
        :return: A JSON response with a successful delete status
        """
        super().delete(self, request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImage(UpdateView):
    model = Ad
    fields: list[dict] = ["name", "price", "description", "author", "category"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Handle a POST request to the AdView. Creates a new image object in the database

        :param request: The incoming request object
        :return: A JSON response with a dictionary representing the updated Ad object
        """
        self.object = self.get_object()

        try:
            self.object.image = request.FILES.get("image")
            self.object.save()
        except Exception:
            return JsonResponse({"error": "Wrong data"}, status=400)

        response: dict = {
            "id": self.object.id,
            "name": self.object.name,
            "description": self.object.description,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)
