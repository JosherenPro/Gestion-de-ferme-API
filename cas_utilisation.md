# Les cas d'utilisation par acteur
## Les acteurs
 - Agriculteur: il gère ses exploitations et ses cultures
 - Technicien: ce lui qui analyse les données et conseille les algriculteurs
 - Administateur: il gére le systeme

## cas utilisation par acteurs

### Argriculteur

- Créer / modifier / supprimer ses exploitations
- Ajouter des cultures
- Enregistrer des mesures manuelles (température, humidité, etc.)
- Consulter les statistiques de ses cultures

> #### il ne peut voir que ses propres exploitations et ses propres données 
 
### Technicien
- Voir les exploitations des agriculteurs assignés
- Ajouter des mesures techniques
- Ajouter des observations terrain
- Générer des rapports analytiques

> #### Ne peut pas supprimer les exploitations

### Admin
- Voir tous les utilisateurs
- Gérer les rôles
- Supprimer comptes
- Accéder aux statistiques globales
- Superviser les logs système
- Accéder aux rapports des techniciens