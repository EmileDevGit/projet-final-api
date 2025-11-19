from abc import ABC, abstractmethod
from typing import List, Optional
from data.models.model_ressource import RessourceCreate, RessourceModify


class IRessourceDAO(ABC):

    @abstractmethod
    def get_all_ressources(self):
        pass

    @abstractmethod
    def get_filtered_ressources(self, q: str):
        pass

    @abstractmethod
    def get_ressource_by_id(self, id: int):
        pass

    @abstractmethod
    def get_ressources_by_categorie(self, categorie_id: int):
        pass

    @abstractmethod
    def get_ressources_by_auteur(self, auteur_id: int):
        pass

    @abstractmethod
    def edit_ressource(self, id: int, res_data: RessourceModify):
        pass

    @abstractmethod
    def delete_ressource(self, id: int):
        pass

    @abstractmethod
    def update_ressource_visibility(self, id: int, visible: bool):
        pass

    @abstractmethod
    def create_ressource(self, res_data: RessourceCreate):
        pass