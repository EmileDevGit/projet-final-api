
Feature: Supprimer un utilisateur

	Scenario: Un administrateur supprime un utilisateur existant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur existant ayant l'id 1
		When je fais un delete sur l'utilisateur ayant l'id 1
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un message "utilisateur 1 supprimé"

	Scenario: Un administrateur supprime un utilisateur inexistant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur inexistant ayant l'id 999
		When je fais un delete sur l'utilisateur ayant l'id 999
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le message "not found"

	Scenario: Un utilisateur supprime son propre compte
		Given un utilisateur authentifie ayant le role user et l'id 5
		When je fais un delete sur l'utilisateur ayant l'id 5
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient le message "utilisateur 5 supprime"

	Scenario: Un utilisateur supprime un autre utilisateur
		Given un utilisateur authentifie ayant le role user, l'id 5
		And un utilisateur existant ayant l'id 1
		When je fais un delete sur l'utilisateur ayant l'id 1
		Then le statut de reponse devrait etre 403
		Then le corps de reponse contient le message "forbidden"
	

