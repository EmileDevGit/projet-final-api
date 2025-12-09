from abc import ABC, abstractmethod


class IAuthDAO(ABC):
    @abstractmethod
    def update_refresh_token_state(self, id: int, is_revoked: bool):
        pass

    @abstractmethod
    def check_refresh_token(self, res_data: dict):
        pass

    @abstractmethod
    def save_refresh_token(self, res_data: dict):
        pass
