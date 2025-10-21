Feature: Changer le statut d'activite d'un 

	Scenario: Un administrateur change le statut d'un utilisateur existant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur existant ayant l'id 1 et un statut inactif
		When je fais un put sur l'utilisateur ayant l'id 1 changeant son statut pour actif
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 1 et un statut actif

	Scenario: Un administrateur change le statut d'un utilisateur inexistant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur inexistant ayant l'id 999
		When je fais un patch sur l'utilisateur ayant l'id 999 changeant son statut pour actif
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le message "not found"

	Scenario: Un utilisateur change le statut de son propre compte
		Given un utilisateur authentifie ayant le role user, l'id 5 et le statut actif
		When je fais un patch sur l'utilisateur ayant l'id 5 changeant le statut pour inactif
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient le message "compte desactive"

	Scenario: Un utilisateur change le statut d'un autre utilisateur
		Given un utilisateur authentifie ayant le role user, l'id 5
		And un utilisateur existant ayant l'id 1 et un statut inactif
		When je fais un patch sur l'utilisateur ayant l'id 1 changeant le statut pour actif 
		Then le statut de reponse devrait etre 403
		Then le corps de reponse contient le message "forbidden"
	

