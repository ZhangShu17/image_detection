# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from constants import error_constants
from api_tools import api_tools
from PIL import Image
from constants import constants
from monitor.models import PersonFace, CarDetection, Transaction, Obstacle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from serializer.serializers import PersonFaceSerializer, CarDetectionSerializer, TransactionSerializer
import logging

logger = logging.getLogger(__name__)


class FaceDetectionView(APIView):

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            uuid = request.POST.get('uuid')
            match_uuid = request.POST.get('match_uuid', '')
            pic = request.data.get('file')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            img = Image.open(pic)
            loc_path = constants.face_dir_path + str(pic)
            img.save(loc_path)
            # 图片本地网络化，不需要往七牛上传
            # api_tools.upload_pic(str(pic), loc_path)
            link_url = constants.base_url + str(pic)
            cur_person_face = PersonFace(camera_id=1, link_url=link_url, loc_path=loc_path,
                                         gender=gender, age=age, longitude=longitude,
                                         latitude=latitude, uuid=uuid, match_uuid=match_uuid)
            try:
                with transaction.atomic():
                    cur_person_face.save()
            except Exception as ex:
                logger.error(ex)
                return api_tools.generate_error_response(error_constants.ERR_SAVE_MODEL,
                                                         status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {}}
        try:
            mode = int(request.GET.get('mode'))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        # 单一模式
        person_face_list = []
        if mode:
            cur_person_face_list = PersonFace.objects.order_by('-create_at')
            if cur_person_face_list.exists():
                person_face_list.append(cur_person_face_list.first())
                match_uuid = cur_person_face_list.first().match_uuid
                if match_uuid:
                    match_person_face = PersonFace.objects.get(uuid=match_uuid)
                    person_face_list.append(match_person_face)
        else:
            person_face_list = PersonFace.objects.order_by('-create_at')

        paginator = Paginator(person_face_list, cur_per_page)
        page_count = paginator.num_pages

        try:
            person_face_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            person_face_list = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            person_face_list = paginator.page(page)
        serializer = PersonFaceSerializer(person_face_list, many=True)
        response_data['data'] = {}
        response_data['data']['curPage'] = page
        response_data['data']['listCount'] = paginator.count
        response_data['data']['list'] = serializer.data
        response_data['data']['pageCount'] = page_count
        return Response(response_data, status.HTTP_200_OK)


class CarDetectionView(APIView):

    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            pic = request.data.get('file')
            length = float(request.POST.get('length', 0))
            width = float(request.POST.get('width', 0))
            height = float(request.POST.get('height', 0))
            plate_num = request.POST.get('plateNum', '')
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            img = Image.open(pic)
            loc_path = constants.car_dir_path + str(pic)
            img.show()
            img.save(loc_path)
            api_tools.upload_pic(str(pic), loc_path)
            link_url = constants.base_url + str(pic)
            cur_car_detection = CarDetection(camera_id=1, loc_path=loc_path, link_url=link_url,
                                             length=length, width=width, height=height,
                                             plate_num=plate_num, longitude=longitude,
                                             latitude=latitude)
            try:
                with transaction.atomic():
                    cur_car_detection.save()
            except Exception as ex:
                logger.error(ex)
                return api_tools.generate_error_response(error_constants.ERR_SAVE_MODEL,
                                                         status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1],
                         'data': {}}
        try:
            mode = int(request.GET.get('mode'))
            cur_per_page = int(request.GET.get('perPage', 20))
            page = int(request.GET.get('page', 1))
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        # 单一模式
        car_detec_list = []
        if mode:
            cur_car_detec = CarDetection.objects.order_by('-create_at').first()
            car_detec_list.append(cur_car_detec)
        else:
            car_detec_list = CarDetection.objects.order_by('-create_at')

        paginator = Paginator(car_detec_list, cur_per_page)
        page_count = paginator.num_pages

        try:
            car_detec_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            car_detec_list = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            car_detec_list = paginator.page(page)
        serializer = CarDetectionSerializer(car_detec_list, many=True)
        response_data['data'] = {}
        response_data['data']['curPage'] = page
        response_data['data']['listCount'] = paginator.count
        response_data['data']['list'] = serializer.data
        response_data['data']['pageCount'] = page_count
        return Response(response_data, status.HTTP_200_OK)


class ObstacleView(APIView):
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            length = float(request.POST.get('length'))
            width = float(request.POST.get('width'))
            height = float(request.POST.get('heigth'))
            distance = float(request.POST.get('distance'))
            angle = float(request.POST.get('angle'))
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        cur_trans_list = Transaction.objects.order_by('-create_at')
        if cur_trans_list.exists():
            try:
                with transaction.atomic():
                    cur_obstacle = Obstacle(length=length, width=width, height=height, distance=distance, angle=angle, transaction_id=cur_trans_list.first().id)
                    cur_obstacle.save()
            except Exception as ex:
                logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_SAVE_MODEL,
                                                         status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)


class TransactionView(APIView):
    def post(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        try:
            request_data = dict(eval(request.data))
            longitude = str(request_data.get('longitude', ''))
            latitude = str(request_data.get('latitude', ''))
            velocity = float(request_data.get('velocity', 0.0))
            angle = float(request_data.get('angle', 0))
            obstacle_list = list(request_data.get('obstacle'))
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_INVALID_PARAMETER,
                                                     status.HTTP_400_BAD_REQUEST)
        cur_transaction = Transaction(car_id=1, longitude=longitude, latitude=latitude, velocity=velocity, angle=angle)
        try:
            with transaction.atomic():
                cur_transaction.save()
        except Exception as ex:
            logger.error(ex)
            return api_tools.generate_error_response(error_constants.ERR_SAVE_MODEL,
                                                         status.HTTP_400_BAD_REQUEST)
        for obstacle in obstacle_list:
            cur_obstacle = Obstacle(length=obstacle['length'], width=obstacle['width'],  height=obstacle['height'],
                                    distance=obstacle['distance'], angle=obstacle['angle'],
                                    transaction=cur_transaction)
            try:
                with transaction.atomic():
                    cur_obstacle.save()
            except Exception as ex:
                logger.error(ex)
                return api_tools.generate_error_response(error_constants.ERR_SAVE_MODEL,
                                                         status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {'retCode': error_constants.ERR_STATUS_SUCCESS[0],
                         'retMsg': error_constants.ERR_STATUS_SUCCESS[1]}
        cur_transaction = Transaction.objects.order_by('-create_at')
        if cur_transaction.exists():
            cur_transaction = cur_transaction.first()
            response_data['data'] = TransactionSerializer(cur_transaction).data
        return Response(response_data, status.HTTP_200_OK)