Feature: Afficher les details d'un utilisateur

	Scenario: L'administrateur accède aux détails d'un utilisateur
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur existant ayant l'id 1
		When je fais un fetch sur l'utilisateur ayant l'id 1
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 1

	Scenario: L'administrateur accède aux détails d'un utilisateur inexistant
		Given un utilisateur authentifie ayant le role admin
		And un utilisateur inexistant ayant l'id 999
		When je fais un fetch sur l'utilisateur ayant l'id 999
		Then le statut de reponse devrait etre 404
		Then le corps de reponse contient le message "aucun résultat"

	Scenario: Un utilisateur accede a ses propres details
		Given un utilisateur authentifie ayant le role user, l'id 5 et le prenom Emile
		When je fais un fetch sur l'utilisateur ayant l'id 5
		Then le statut de reponse devrait etre 200
		And le corps de reponse contient un utilisateur ayant l'id 5
		And le l'utilisateur retourne possede le role user et le prenom Emile
	
	Scenario: Un utilisateur accede au détail d'un autre utilisateur 
		Given un utilisateur authentifie ayant le role user, l'id 5 et le prenom Emile
		And un utilisateur existant ayant l'id 1
		When je fais un fetch sur l'utilisateur ayant l'id 1
		Then le statut de reponse devrait etre 403
		And le corps de reponse contient le message "forbidden"
