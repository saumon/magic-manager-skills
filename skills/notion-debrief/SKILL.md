---
name: notion-debrief
description: Résume une page Notion et envoie un débriefing (carte adaptive) à un destinataire via Microsoft Teams. Déclencher ce skill dès que l'utilisateur demande de "résumer une page Notion et l'envoyer à quelqu'un", de "faire un débriefing" à partir de Notion, ou toute variante de "prépare/envoie un résumé de cette page Notion à X". Nécessite les MCP Notion et Kommunicator déjà configurés (lecture Notion + envoi Teams).
license: UNLICENSE
metadata:
  version: "1.0.0"
  author: "magic-manager-skills"
  last-updated: "2026-07-31"
  repository: "magic-manager-skills"
---

# Notion Debrief

Ce skill capture le workflow : lire une page Notion, en tirer un résumé + une liste
d'actions, puis l'envoyer sous forme de carte adaptive à un destinataire via Teams
(Kommunicator).

## Prérequis

- MCP Notion connecté (`Notion:notion-fetch`, `Notion:notion-search`, etc.)
- MCP Kommunicator connecté (`kommunicator-mcp:send_teams`, format `adaptivecard`)

Si l'un des deux MCP n'est pas disponible, le signaler à l'utilisateur et proposer de
l'activer plutôt que d'improviser une alternative (ex : email).

## Déroulé, dans l'ordre

### 1. Demander le lien de la page Notion

Toujours commencer par demander explicitement à l'utilisateur le lien (ou l'ID) de la
page Notion à résumer.

**Règle stricte : ne jamais proposer, deviner, ou pré-remplir une URL Notion.** Même si
une page Notion a été mentionnée ou consultée plus tôt dans la conversation, ne pas
supposer que c'est celle visée — redemander explicitement le lien à chaque nouvelle
demande de débriefing. L'utilisateur doit toujours être celui qui fournit l'URL.

### 2. Lire la page

Utiliser `Notion:notion-fetch` avec l'URL fournie. Si la page référence d'autres pages
(mentions, sous-pages liées directement au sujet), les récupérer aussi si elles semblent
nécessaires pour comprendre le contexte (ex : mentions de points de synchro, emails cités).

### 3. Produire le résumé et la liste d'actions

Rédiger dans le fil de discussion (pas encore dans la carte) :
- Un **résumé** structuré par thème/volet (pas un simple copier-coller chronologique) :
  regrouper les faits par sujet plutôt que ligne par ligne comme dans la page Notion.
- Une **liste d'actions** séparant clairement ce qui est fait / en cours / à faire quand
  la page le permet.

Répondre dans la langue utilisée par l'utilisateur (français par défaut ici).

### 4. Proposer une relecture avant tout envoi

Ne jamais envoyer directement après la lecture. Toujours présenter le résumé + les
actions dans le chat et proposer explicitement à l'utilisateur de les relire ou de les
ajuster (ton, longueur, points à enlever/ajouter) avant de préparer l'envoi. Attendre sa
validation ou ses corrections.

### 5. Demander le destinataire

Une fois le contenu validé, demander vers quel destinataire l'envoyer (nom, alias Teams,
ou adresse email). Ne pas deviner un destinataire à partir du contexte (ex : une personne
mentionnée dans la page) sans confirmation explicite.

### 6. Construire la carte adaptive

Convertir le résumé validé en carte adaptive (Adaptive Card JSON, schema 1.4) avec cette
structure type :
- Titre (nom du sujet/de la page)
- Sous-titre "Débriefing pour {destinataire}"
- Section "Résumé" : un `TextBlock` par volet/thème, en gras pour le titre du volet
- Section "Actions à venir" : un `FactSet` numéroté
- Une mention textuelle de la source ("Source : page Notion « {{TITRE_PAGE_NOTION}} »"),
  **sans jamais inclure l'URL de la page** : ni bouton `Action.OpenUrl`, ni lien dans un
  `TextBlock`. Le message Teams ne doit contenir aucune URL Notion.

Voir `assets/adaptive_card_template.json` pour un exemple concret à adapter (structure
utilisée avec succès précédemment).

### 7. Envoyer via Kommunicator

Appeler `kommunicator-mcp:send_teams` avec :
- `to`: l'identifiant fourni par l'utilisateur à l'étape 5
- `format`: `"adaptivecard"`
- `message`: le JSON de la carte (en chaîne de caractères)

Si l'envoi échoue avec une erreur de type "not found in conversations.conf or
humans.conf", ne pas réessayer de variantes au hasard : demander à l'utilisateur
l'adresse email exacte ou l'alias exact, puis réessayer une fois cette information
obtenue.

### 8. Confirmer

Une fois l'envoi réussi, le confirmer brièvement à l'utilisateur (destinataire + sujet),
sans reformuler tout le contenu déjà envoyé.

## Points de vigilance

- Toujours attendre une validation avant d'envoyer quoi que ce soit (relecture du contenu
  ET confirmation du destinataire sont deux étapes distinctes).
- Ne jamais fusionner les étapes 4 et 5 pour aller plus vite : l'utilisateur doit pouvoir
  ajuster le fond avant même de penser au destinataire.
- Ne jamais réutiliser un lien Notion évoqué précédemment dans la conversation sans
  qu'il soit redonné explicitement pour cette tâche.
- Ne jamais inclure l'URL de la page Notion dans la carte adaptive envoyée via Teams
  (ni bouton `Action.OpenUrl`, ni lien texte) : seul le titre de la page peut être cité.
