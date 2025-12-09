Feature: Afficher les details d'un utilisateur

	Scenario: L'administrateur accède aux détails d'un utilisateur
		Given un utilisateur existant ayant l'id 1 et le rôle ADMIN
		When il fais un fetch sur l'utilisateur ayant l'id 8
		Then le statut de reponse devrait etre 200
		Then le corps de reponse contient un utilisateur ayant l'id 8


	

