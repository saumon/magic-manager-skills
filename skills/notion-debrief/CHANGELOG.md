# Changelog — notion-debrief

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.0.0] - 2026-07-31

### Ajouté

- Première version du skill : lecture d'une page Notion, résumé structuré
  par volet, liste d'actions, relecture obligatoire avant envoi, envoi
  d'une carte adaptive via Kommunicator (Teams).
- Template de carte adaptive de référence (`assets/adaptive_card_template.json`).
- Règle stricte : ne jamais proposer/deviner une URL Notion ou un
  destinataire — toujours les demander explicitement.

### Modifié

- La carte adaptive envoyée via Teams n'inclut plus l'URL de la page Notion (retrait
  du bouton `Action.OpenUrl`) ; seul le titre de la page est cité en source.

### Contexte

- Dérivé d'un cas d'usage réel : débriefing d'un dossier d'internalisation
  envoyé à un collaborateur.

[1.0.0]: https://github.com/<org>/magic-manager-skills/releases/tag/notion-debrief-v1.0.0
