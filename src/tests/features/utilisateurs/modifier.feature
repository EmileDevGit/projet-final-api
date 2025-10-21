Feature: Changer le statut d'activite d'un 

	Scenario: Un administrateur modifie un utilisateur existant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur existant ayant l'id 1, le role user et le statut actif 
		When je fais un put sur l'utilisateur ayant l'id 1 modifiant le role pour mentor et le statut pour inactf
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 1, le role mentor et le statut inactif

	Scenario: Un administrateur modifie un utilisateur inexistant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur inexistant ayant l'id 999
		When je fais un put sur l'utilisateur ayant l'id 999 modifiant le role pour mentor et le statut pour inactif
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le message "not found"

	Scenario: Un utilisateur modifie son propre compte
		Given un utilisateur authentifie ayant le role user, l'id 5, le prenom Emile et le statut actif
		When je fais un put sur l'utilisateur ayant l'id 5 changeant le prenom pour Wesner et le statut inactif
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 5, le prenom Wesner et le statut inactif

	Scenario: Un utilisateur modifie un autre utilisateur
		Given un utilisateur authentifie ayant le role user, l'id 5
		And un utilisateur existant ayant l'id 1
		When je fais un put sur l'utilisateur ayant l'id 1 changeant le prenom pour Wesner et le statut pour inactif
		Then le statut de reponse devrait etre 403
		Then le corps de reponse contient le message "forbidden"
