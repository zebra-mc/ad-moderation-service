from repositories.moderation import ModerationRepository
from schemas.advertisement import Advertisement


class ModerationService:
    def __init__(self, repository: ModerationRepository):
        self.repository = repository

    def predict(self, ad: Advertisement) -> bool:
        if ad.is_verified_seller:
            return False

        min_images = self.repository.get_min_images_for_unverified_seller()
        return ad.images_qty < min_images