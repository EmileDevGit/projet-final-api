from abc import ABC, abstractmethod
from data.models.model_utilisateur import UtilisateurModify as UtilisateurModify
from data.models.model_utilisateur import UtilisateurCreate as UtilisateurCreate


class IUtilisateurDAO(ABC):

    @abstractmethod
    def get_all_utilisateurs(self):
        pass

    @abstractmethod
    def get_filtered_utilisateurs(self, q: str):
        pass

    @abstractmethod
    def get_all_mentors(self):
        pass

    @abstractmethod
    def get_filtered_mentors(self, q: str):
        pass

    @abstractmethod
    def get_utilisateur_by_id(self, id: int):
        pass

    @abstractmethod
    def get_utilisateur_by_email(self, email: str):
        pass

    @abstractmethod
    def edit_user(self, id: int, user_data: UtilisateurModify):
        pass

    @abstractmethod
    def delete_user(self, id: int):
        pass

    @abstractmethod
    def update_user_status(self, id: int, actif: bool):
        pass

    @abstractmethod
    def create_user(self, user_data: UtilisateurCreate):
        pass
