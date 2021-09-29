""" File with routes for receiving statistic"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from project.serializers import StatisticSerializerPost as Ssp, StatisticSerializer as Ss
from project.models import *
from source.constants import API_SECURE_KEY


@api_view(['GET'])
def get_statistic(request):
    """ Method for obtaining statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return Response(data="INVALID_SECURE_KEY", status=status.HTTP_400_BAD_REQUEST)

    date_from, date_to = request.data.get('from'), request.data.get('to')
    if date_from and date_to:
        validate_date_from, validate_date_to = Ssp(data={'date': date_from}), Ssp(data={'date': date_to})
        validate_date_from.is_valid(raise_exception=True)
        validate_date_to.is_valid(raise_exception=True)
    else:
        return Response(data="NO_fields_(date_from, date_to)", status=status.HTTP_400_BAD_REQUEST)

    qs = Statistic.objects.filter(date__gte=date_from, date__lte=date_to)
    serializer = Ss(qs, many=True)
    if serializer.data:

        sort_by_field = request.data.get('sort_by_field') if request.data.get('sort_by_field') else 'date'
        try:
            serializer_data = sorted(
                serializer.data, key=lambda k: k[sort_by_field], reverse=True)
            return Response(data=serializer_data, status=status.HTTP_200_OK)
        except KeyError:
            return Response(data="ORDER_BY_FIELD_ERROR", status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_statistic(request):
    """ Method for create statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return Response(data="INVALID_SECURE_KEY", status=status.HTTP_400_BAD_REQUEST)

    serializer = Ssp(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data="SUCCESSFULLY_ADDED_STATISTIC", status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_statistic(request):
    """ Method for delete statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return Response(data="INVALID_SECURE_KEY", status=status.HTTP_400_BAD_REQUEST)

    element_for_delete = Statistic.objects.all()
    if element_for_delete:
        element_for_delete.delete()
        return Response(data="STATISTIC_SUCCESSFULLY_DELETED", status=status.HTTP_410_GONE)
    return Response(data="NO_STATISTIC", status=status.HTTP_404_NOT_FOUND)
