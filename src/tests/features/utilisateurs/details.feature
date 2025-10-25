Feature: Afficher les details d'un utilisateur

	Scenario: L'administrateur accède aux détails d'un utilisateur
		Given un utilisateur existant ayant l'id 1 et le rôle admin
		When il fais un fetch sur l'utilisateur ayant l'id 8
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 8

	Scenario: L'administrateur accède aux détails d'un utilisateur inexistant
		Given un utilisateur existant ayant l'id 1 et le rôle admin
		And un utilisateur inexistant ayant l'id 999
		When il fais un fetch sur l'utilisateur ayant l'id 999
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le message "not found"

	Scenario: Un utilisateur accede a ses propres details
		Given un utilisateur authentifie ayant le role user, l'id 5 et le prenom Emile
		When il fais un fetch sur l'utilisateur ayant l'id 5
		Then le statut de reponse devrait etre 200
		And le corps de reponse contient un utilisateur ayant l'id 5
		And le l'utilisateur retourne possede le role user et le prenom Emile
	
	Scenario: Un utilisateur accede au détail d'un autre utilisateur 
		Given un utilisateur authentifie ayant le role user, l'id 5 et le prenom Emile
		And un utilisateur existant ayant l'id 1
		When il fais un fetch sur l'utilisateur ayant l'id 1
		Then le statut de reponse devrait etre 403
		And le corps de reponse contient le message "forbidden"
