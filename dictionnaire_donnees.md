## Utilisateur
- id: int
- nom: string
- prenom: string
- email: string
- password: string
- role: Enum("agriculteur", "technicien", "Admin")

## Ferme
- id
- nom: string
- localisation: string
- perimetre: float
- aire: float
- utilisateur_id: int

## Culture
- id: int
- type: string
- perimetre: float
- aire: float
- date_culture: datetime
- ferme_id: int 