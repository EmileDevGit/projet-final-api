Feature: Changer le statut d'activite d'un 

	Scenario: Un administrateur change le statut d'un utilisateur existant
		Given un utilisateur authentifie ayant le role ADMIN
		And un utilisateur existant ayant l'id 1 et un statut_actif False
		When il fais un put sur l'utilisateur ayant l'id 1 changeant son statut_actif pour True
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 1 et un status_actif True

	Scenario: Un administrateur change le statut d'un utilisateur inexistant
		Given un utilisateur authentifie ayant le role ADMIN
		And un utilisateur inexistant ayant l'id 999
		When il fais un patch sur l'utilisateur ayant l'id 999 changeant son status_actif True
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le detail "Utilisateur non trouvé"

	Scenario: Un utilisateur change le statut de son propre compte
		Given un utilisateur authentifie ayant le type_compte USER, l'id 5 et le status_actif True
		When il fais un patch sur l'utilisateur ayant l'id 5 changeant le status_actif pour False
		Then le statut de reponse devrait etre 200

	Scenario: Un utilisateur change le statut d'un autre utilisateur
		Given un utilisateur authentifie ayant le type_compte USER, l'id 5
		And un utilisateur existant ayant l'id 1 et un status_actif True
		When il fais un patch sur l'utilisateur ayant l'id 1 changeant le status_actif pour False 
		Then le statut de reponse devrait etre 403
		Then le corps de reponse contient le detail "Vous ne possédez pas les droits de modification pour cet utilisateur"
	

