from ninja import NinjaAPI
from app.api.shopping_list import router as shopping_list_router
api = NinjaAPI()

api.add_router("/shopping-list", shopping_list_router)
