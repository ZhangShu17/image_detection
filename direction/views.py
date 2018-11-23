# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from models import Command, StopStatus, ControlState
import time
import logging

logger = logging.getLogger(__name__)


class CarMoveView(APIView):
    # 发出指令
    def post(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功'
        }
        try:
            angle = int(request.POST.get('angle'))
            # time = str(request.POST.get('time', ''))
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 1001,
                'retMessage': u'参数无效'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)

        if angle > 360 or angle < -360 or not time:
            response_data = {
                'retCode': 1002,
                'retMessage': u'参数越界'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        cur_time = int(10*time.time())
        last_command = Command.objects.all().order_by('-time')

        if len(last_command):
            total_angle = last_command.first().total_angle + angle
        else:
            total_angle = angle
        response_data['totalAngle'] = total_angle
        try:
            Command.objects.create(angle=angle, time=cur_time, total_angle=total_angle)
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 1003,
                'retMessage': u'创建对象失败'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)

    # 获取当前方向盘角度
    def get(self, request):
        """
        查看当前方向盘角度
        :param request:
        :return:
        """
        response_data = {
            'retCode': 0,
            'retMessage': u'成功'
        }
        last_command = Command.objects.all().order_by('-time')
        if not len(last_command):
            total_angle = 0
        else:
            total_angle = last_command.first().total_angle

        response_data['totalAngle'] = total_angle
        return Response(response_data, status.HTTP_200_OK)


class ChangeStopStatus(APIView):
    def post(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功'
        }
        try:
            stop_status = int(request.POST.get('status'))
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 8001,
                'retMessage': u'参数无效'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        Stop_Obj = StopStatus.objects.first()
        current_status = Stop_Obj.stop_status
        if stop_status == 0:
            if not current_status:
                response_data = {
                    'retCode': 8002,
                    'retMessage': u'已是启动状态，启动命令无效'
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST)
            else:
                if not len(Command.objects.all()):
                    Command.objects.create(angle=0, time=int(10*time.time()), total_angle=0)
                StopStatus.objects.update(stop_status=False)
        elif stop_status == 1:
            if current_status:
                response_data = {
                    'retCode': 8003,
                    'retMessage': u'已是停止状态，停止命令无效'
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST)
            else:
                StopStatus.objects.update(stop_status=True)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功'
        }
        try:
            Stop_Obj = StopStatus.objects.first()
            stop_status = int(Stop_Obj.stop_status)
            response_data['stopStatus'] = stop_status
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 8004,
                'retMessage': u'获取车辆状态出错'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status.HTTP_200_OK)


class CommandExecuView(APIView):

    def get(self, request):
        """
        获取最新指令
        :param request:
        :return:
        """
        response_data = {
            'retCode': 0,
            'retMessage': u'成功',
            'time': 0,
            'angle': 0
        }
        all_command = Command.objects.all().order_by('-time')
        if len(all_command):
            cur_command = all_command.first()
        else:
            response_data = {
                'retCode': 10008,
                'retMessage': u'没有有效的指令',
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        response_data['time'] = cur_command.time
        response_data['angle'] = cur_command.angle
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功',
        }
        try:
            time = int(request.POST.get('time'))
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 2001,
                'retMessage': u'参数无效'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        cur_command = Command.objects.filter(time=time)
        if not len(cur_command):
            response_data = {
                'retCode': 2002,
                'retMessage': u'时间不正确'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        else:
            cur_command.update(execute=True)
            return Response(response_data, status.HTTP_200_OK)

    def delete(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功',
        }
        Command.objects.delete()
        ControlState.objects.update(control_status=True)
        StopStatus.objects.update(stop_status=True)
        return Response(response_data, status.HTTP_200_OK)


# 切换控制模式，0：自动驾驶模式，1：手动控制模式
class ControlStateView(APIView):
    def post(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功',
        }
        try:
            control_state = int(request.POST.get('controlState'))
        except Exception as ex:
            logging.error(ex)
            response_data = {
                'retCode': 12001,
                'retMessage': u'参数无效'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        cur_cont_stat =int(ControlState.objects.first().control_status)
        if control_state == cur_cont_stat:
            response_data = {
                'retCode': 12002,
                'retMessage': u'状态一致，无需切换'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        ControlState.objects.update(control_status=control_state>0)
        if control_state == 0:
            StopStatus.objects.update(stop_status=False)
        if control_state == 1:
            StopStatus.objects.update(stop_status=True)
        return Response(response_data, status.HTTP_200_OK)

    def get(self, request):
        response_data = {
            'retCode': 0,
            'retMessage': u'成功',
        }
        try:
            cur_cont_stat = int(ControlState.objects.first().control_status)
        except Exception as ex:
            print('function name: ', __name__)
            print(Exception, ': ', ex)
            response_data = {
                'retCode': 12003,
                'retMessage': u'get请求出错'
            }
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        response_data['cur_control_state'] = cur_cont_stat
        return Response(response_data, status.HTTP_200_OK)