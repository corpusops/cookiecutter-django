import re

from django.conf import settings

_HTML_TYPES = ("text/html", "application/xhtml+xml")


class ShowInstanceHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check for flag
        if not settings.INSTANCE_HEADER:
            return response

        # Check for responses where the toolbar can't be inserted.
        content_encoding = response.get("Content-Encoding", "")
        content_type = response.get("Content-Type", "").split(";")[0]
        if (
            getattr(response, "streaming", False)
            or "gzip" in content_encoding
            or content_type not in _HTML_TYPES
        ):
            return response

        # Determine message
        message = f"""<div style="text-align: center;
            position: absolute;
            top: 0;
            width: 100%;
            background: {settings.INSTANCE_COLOR};
            height: 30px;
            padding: 5px;
            font-size: 15px;
            box-sizing: border-box;
        ">{settings.INSTANCE_HEADER}</div>"""

        # Insert the message in the response.
        content = response.content.decode(response.charset)
        bits = re.split("<body(.*?)>", content, flags=re.IGNORECASE | re.DOTALL)
        if len(bits) > 1:
            bits[2] = message + bits[2]
            response.content = (
                bits[0]
                + f'<body style="padding-top: 30px; box-sizing: border-box"{bits[1]}>'
                + bits[2]
            )
            if "Content-Length" in response:
                response["Content-Length"] = len(response.content)
        return response
