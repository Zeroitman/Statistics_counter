""" File with routes for statistic"""
from rest_framework import status
from rest_framework.decorators import api_view
from project.serializers import StatisticSerializerPost as Ssp, StatisticSerializer as Ss
from project.models import *
from source.constants import API_SECURE_KEY
from source.utils import CustomResponse


@api_view(['GET'])
def get_statistic(request):
    """ Method for obtaining statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return CustomResponse(result="INVALID_SECURE_KEY")
    date_from, date_to = request.query_params.get('from'), request.query_params.get('to')
    if date_from and date_to:
        validate_date_from, validate_date_to = Ssp(data={'date': date_from}), Ssp(data={'date': date_to})
        validate_date_from.is_valid(raise_exception=True)
        validate_date_to.is_valid(raise_exception=True)
    else:
        return CustomResponse(result="NO_OR_WRONG_FIELDS_from_AND_to")

    qs = Statistic.objects.filter(date__gte=date_from, date__lte=date_to)
    serializer = Ss(qs, many=True)
    if serializer.data:

        sort_by_field = request.query_params.get('sort_by_field') if request.query_params.get(
            'sort_by_field') else 'date'
        try:
            serializer_data = sorted(
                serializer.data, key=lambda k: k[sort_by_field], reverse=True)
            return CustomResponse(result=serializer_data, result_code=status.HTTP_200_OK)
        except KeyError:
            return CustomResponse(result="SORT_FIELD_ERROR")
    return CustomResponse(result="NO_DATA", result_code=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def save_statistic(request):
    """ Method for create statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return CustomResponse(result="INVALID_SECURE_KEY")

    serializer = Ssp(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return CustomResponse(result="SUCCESSFULLY_ADDED_STATISTIC", result_code=status.HTTP_201_CREATED)
    return CustomResponse(result=serializer.errors)


@api_view(['DELETE'])
def delete_statistic(request):
    """ Method for delete statistic """
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return CustomResponse(result="INVALID_SECURE_KEY")

    element_for_delete = Statistic.objects.all()
    if element_for_delete:
        element_for_delete.delete()
        return CustomResponse(result="STATISTIC_SUCCESSFULLY_DELETED", result_code=status.HTTP_410_GONE)
    return CustomResponse(result="NO_STATISTIC", result_code=status.HTTP_404_NOT_FOUND)
