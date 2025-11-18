import django_filters as drf_filters
from rest_framework import viewsets, serializers
from django.shortcuts import render
from django.db import models
from .models import (
    GeneralInformation,
    Director,
    Associate,
    Client,
    Affiliation,
    Level,
    Period,
    Activity,
    Domain,
    Field,
    Action,
    TypeAction,
    Beneficiary,
    Decision,
    Target,
    Observation
)


def home(request):
    data = (("Groupements", GeneralInformation.objects.count()),
            ("Activities", Activity.objects.count()))
    
    return render(request, "hatvp/index.html", locals())


def viewset_factory(m):
    class FilterSet(drf_filters.FilterSet):
        class Meta:
            model = m
            fields = "__all__"

    class Serializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = m
            fields = "__all__"

    class ViewSet(viewsets.ModelViewSet):
        serializer_class = Serializer
        filterset_class = FilterSet
        queryset = m.objects.all()
        
    return ViewSet

viewsets = [
    viewset_factory(m) for m in (
        GeneralInformation,
        Director,
        Associate,
        Client,
        Affiliation,
        Level,
        Period,
        Activity,
        Domain,
        Field,
        Action,
        TypeAction,
        Beneficiary,
        Decision,
        Target,
        Observation
    )
]


# class GeneralInformationFilterSet(
#     class Meta:
#         model = GeneralInformation
#         fields = "__all__"

# class GeneralInformationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GeneralInformation
#         fields = "__all__"

# class GeneralInformationViewSet(viewsets.ModelViewSet):
#     serializer_class = GeneralInformationSerializer
#     filterset_class = GeneralInformationFilterSet
#     queryset = GeneralInformation.objects.all()


# class ActivitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Activity
#         fields = "__all__"

# class ActivityViewSet(viewsets.ModelViewSet):
#     serializer_class = ActivitySerializer
#     queryset = Activity.objects.all()
