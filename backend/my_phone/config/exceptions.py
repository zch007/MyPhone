from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    """
    DRF无法处理的情况下，会显示该异常
    """
    error = "{} {} {}".format(context["view"], context["request"].method, exc)
    print(error)

    # 先让DRF处理异常 根据异常处理的返回值来判断异常是否被处理
    response = drf_exception_handler(exc, context)

    # 如果返回值为None 代表DRF无法处理此异常 需要自定义处理
    if not response:
        return Response({"error_message": "请稍等，马上为您处理"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
