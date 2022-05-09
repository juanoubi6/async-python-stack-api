from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.builder import add_events
from app.http import add_routes, FastAPIWrapper, add_error_handlers, add_middlewares

api = FastAPIWrapper(default_response_class=JSONResponse)
add_routes(api)
add_error_handlers(api)
add_middlewares(api)
add_events(api)

# Add ASGI middlewares
api.add_middleware(GZipMiddleware, minimum_size=1000)
