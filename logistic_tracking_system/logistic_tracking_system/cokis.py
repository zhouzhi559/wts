from django.utils.deprecation import MiddlewareMixin


class SoloveCrossDomainMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """
        处理跨域的中间件，将所有的响应都能实现跨域
        """
        response['Access-Control-Allow-Origin'] = "http://10.0.20.107:8080" #改成*就是允许跨所有域，但是set-cookie就会失效
        response['Access-Control-Allow-Headers'] = "Content-Type"
        response['Access-Control-Allow-Credentials'] = "true"
        return response
