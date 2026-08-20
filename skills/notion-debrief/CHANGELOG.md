# Changelog — notion-debrief

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.3.1] - 2026-08-20

### Modifié

- Correction du frontmatter : `author: "saumon"` au lieu de
  `author: "magic-manager-skills"`. Chaque skill porte le nom de son auteur,
  pas le nom du mono-repo.

## [1.3.0] - 2026-08-03

### Modifié

- Refonte du template de carte adaptive : listes à puces réelles (items `- `
  séparés par `\r`), en-tête en `Container` `style: emphasis`, titres de volet
  colorés, séparateurs entre sections.
- La section « Actions à venir » (`FactSet` numéroté) devient « Actions »
  scindée en « Fait » et « À faire » : le `FactSet` écrasait la numérotation
  et faisait perdre la distinction fait / à faire présente dans le résumé.

### Ajouté

- Règles de rendu Teams dans l'étape 6 : séparateur `\r` pour les puces,
  `wrap: true` obligatoire, markdown limité à `**gras**` / `_italique_`,
  une puce = une information (pas de fusion en paragraphe).
- Point de vigilance : la carte doit rester fidèle au résumé validé à
  l'étape 4, et toute omission volontaire (donnée sensible) doit être
  signalée à l'utilisateur avant l'envoi.

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
