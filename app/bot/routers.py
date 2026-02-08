from aiogram import Router

from app.bot.handlers.user.start import router as start_router
from app.bot.handlers.user.catalog import router as catalog_router
from app.bot.handlers.user.products import router as product_router
from app.bot.handlers.user.about import router as about_router


router = Router()
router.include_router(start_router)
router.include_router(catalog_router)
router.include_router(product_router)
router.include_router(about_router)


