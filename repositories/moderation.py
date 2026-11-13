class ModerationRepository:
    def __init__(self):
        self.rules = {"min_images_for_unverified_seller": 1}

    def get_min_images_for_unverified_seller(self) -> int:
        return self.rules["min_images_for_unverified_seller"]