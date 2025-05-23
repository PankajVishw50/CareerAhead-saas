import logging

logger = logging.getLogger(__name__)


class WebSocketLoggerMiddleware:
    def __init__(self, inner) -> None:
        self.inner = inner

    async def __call__(self, scope, receive, send):

        if scope["type"] == "websocketk":
            path = scope.get("path", "")
            logger.info(f"Web Socket request to: {path}")

        return await self.inner(scope, receive, send)
