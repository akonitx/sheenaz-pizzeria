class ContentSecurityPolicyMiddleware:
    """
    Middleware that sets HTTP Content-Security-Policy header to
        - scipt-src:
    """

    def __init__(self, get_response):
        self._get_response = get_response

    @staticmethod
    def set_scirpt_source(response):
        """
        Setting Content-Security-Policy header with
            - script-src 'self'
        values
        """

        response.headers[
            "Content-Security-Policy"
        ] = "script-src 's3.eu-central-1.amazonaws.com*' ;"
        (
            "https://s3.eu-central-1.amazonaws.com/lime-static-files.django/static/admin/js/theme.js"
        )

    def __call__(self, request):
        response = self._get_response(request)

        #   self.set_scirpt_source(response)

        return response


class AccessControlAllowOriginMiddleware:
    """
    Middleware that sets HTTP AccessControlAllowOrigin header to
        https://www.youtube.com
    """

    def __init__(self, get_response):
        self._get_response = get_response

    @staticmethod
    def set_access_control_allow_origin(response):
        """
        Setting AccessControlAllowOrigin header with
            https://www.youtube.com
        values
        """

        response.headers["Access-Control-Allow-Origin"] = "https://www.youtube.com"

    def __call__(self, request):
        response = self._get_response(request)

        self.set_access_control_allow_origin(response)

        return response
