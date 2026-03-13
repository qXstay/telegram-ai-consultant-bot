from app.handlers.faq import router as faq_router
from app.handlers.lead_form import router as lead_form_router
from app.handlers.start import router as start_router

__all__ = ["start_router", "faq_router", "lead_form_router"]
