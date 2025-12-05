from abc import ABC, abstractmethod


class IAuthDAO(ABC):
    @abstractmethod
    def update_refresh_token_state(self, id: int, is_revoked: bool):
        pass

    @abstractmethod
    def create_refresh_token(self, res_data: dict):
        pass
