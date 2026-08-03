# Changelog — notion-debrief

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.2.0] - 2026-08-03

### Ajouté

- Garde-fou anti-injection : le contenu de la page Notion est traité comme
  une donnée à résumer, jamais comme une instruction à exécuter (étape 2 et
  « Points de vigilance »).

### Modifié

- `metadata.repository` pointe désormais vers l'URL complète du dépôt.
- Licence du skill : `UNLICENSE` → `MIT`.

## [1.1.0] - 2026-07-31

Tag publié prématurément : contenu identique à la 1.0.0, aucune modification
du skill. Conservé ici pour tracer une référence déjà poussée ; ne pas
utiliser.

## [1.0.0] - 2026-07-31

### Ajouté

- Première version du skill : lecture d'une page Notion, résumé structuré
  par volet, liste d'actions, relecture obligatoire avant envoi, envoi
  d'une carte adaptive via Kommunicator (Teams).
- Template de carte adaptive de référence (`assets/adaptive_card_template.json`).
- Règle stricte : ne jamais proposer/deviner une URL Notion ou un
  destinataire — toujours les demander explicitement.
- La carte adaptive envoyée via Teams n'inclut aucune URL Notion (ni bouton
  `Action.OpenUrl`, ni lien texte) ; seul le titre de la page est cité en source.

### Contexte

- Dérivé d'un cas d'usage réel : débriefing d'un dossier d'internalisation
  envoyé à un collaborateur.

[1.2.0]: https://github.com/saumon/magic-manager-skills/releases/tag/notion-debrief-v1.2.0
[1.1.0]: https://github.com/saumon/magic-manager-skills/releases/tag/notion-debrief-v1.1.0
[1.0.0]: https://github.com/saumon/magic-manager-skills/releases/tag/notion-debrief-v1.0.0
