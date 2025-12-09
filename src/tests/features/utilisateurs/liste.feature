Feature: Liste des utilisateurs

	Scenario: L'administrateur accède à la liste complète 
		Given un administrateur existant
		When il fais un fetch sur touts les utilisateurs
		Then il recoit un code 200
		Then il recoit un tableau json nommé utilisateurs




