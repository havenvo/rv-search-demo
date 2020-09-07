from Core.models import Profile
from Home.serializers import ProfileSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.renderers import TemplateHTMLRenderer


def home(request):
    return render(request, 'Home/home.html', {})


def signup(request):
    return render(request, 'Home/sign-up.html')


def signin(request):
    return render(request, 'Home/sign-in.html')


def sitter_registration(request):
    return render(request, 'Home/sitter-registration.html')


def search(request):
    return render(request, 'Home/search.html', {'user_config': {'show_model': 'false'}})


def search_alternative(request):
    accept = request.GET.get('accept', 'html')
    profiles = Profile.objects.all()

    service_type = request.GET.get('service_type', None)
    if service_type:
        profiles = profiles.filter(service_rates__service_type__short_code=service_type)

    price_from = request.GET.get('min_price', None)
    price_to = request.GET.get('max_price', None)
    if price_from and price_to:
        profiles = profiles.filter(service_rates__service_type__short_code=service_type,
                                   service_rates__price__gte=price_from, service_rates__price__lte=price_to)

    pet_type = request.GET.get('pet_type', None)
    if pet_type:
        pet_type_list = pet_type.split(',')
        profiles = profiles.filter(pet_types__short_code__in=pet_type_list).distinct()

    pet_num = request.GET.get('pet_num', None)
    if pet_num:
        profiles = profiles.filter(pet_num__gte=pet_num)

    context = {"service_type": service_type}
    data = ProfileSerializer(profiles, context=context, many=True).data
    return render(request, 'Home/_search-result.html', {'profile_list': data})


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Home/profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})
