# magic-manager-skills

Mono-repo de skills Claude pour l'automatisation de tâches de management
(débriefings, suivi RH, reporting, etc.).

## Structure

```text
magic-manager-skills/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── skills/
    └── notion-debrief/
        ├── SKILL.md
        └── assets/
            └── adaptive_card_template.json
```

Chaque skill vit dans son propre sous-dossier sous `skills/`, avec son
`SKILL.md` et ses éventuelles ressources (`assets/`, `references/`,
`scripts/`).

## Installation d'un skill

### Claude Code (application desktop)

1. Zipper le dossier du skill voulu, en gardant le dossier lui-même à la
   racine de l'archive :

   ```bash
   cd skills && zip -r notion-debrief.zip notion-debrief
   ```

2. Dans Claude, aller dans **Compétences → Gérer les compétences**, puis
   ajouter le skill en important le `.zip` généré.

Les archives `*.zip` produites dans `skills/` sont ignorées par Git.

### Autres environnements

Copier le contenu de `skills/<nom-du-skill>/` dans le dossier de skills de
Claude (`/mnt/skills/user/` sur Claude.ai, ou l'équivalent Cowork), ou
importer le fichier `.skill` packagé directement depuis l'interface Claude.

## Skills disponibles

### notion-debrief — v1.2.0

Résume une page Notion et envoie un débriefing (carte adaptive) à un
destinataire via Microsoft Teams. Nécessite les MCP Notion et Kommunicator.
Voir [`skills/notion-debrief/SKILL.md`](skills/notion-debrief/SKILL.md) et
son [`CHANGELOG.md`](skills/notion-debrief/CHANGELOG.md).

## Versionnement

Chaque skill est versionné indépendamment en [semver](https://semver.org/) :

- La version courante est indiquée dans `metadata.version` du frontmatter
  de son `SKILL.md`.
- L'historique détaillé vit dans le `CHANGELOG.md` du skill.
- Chaque release est marquée par un tag Git au format
  `<nom-du-skill>-v<version>` (ex. `notion-debrief-v1.0.0`), pas par un tag
  global de repo — ça permet de revenir en arrière sur un skill précis sans
  toucher aux autres.

```bash
# Exemple : tagger une nouvelle version du skill notion-debrief
git tag notion-debrief-v1.1.0
git push origin notion-debrief-v1.1.0
```

## Ajouter un nouveau skill

1. Créer `skills/<nom-du-skill>/SKILL.md` (frontmatter `name` + `description`,
   puis le corps du workflow).
2. Ajouter les ressources nécessaires dans un sous-dossier `assets/`,
   `references/` ou `scripts/` si besoin.
3. Documenter le skill dans la section "Skills disponibles" de ce README.
4. Committer avec un message clair (`git commit -m "Ajoute skill <nom>"`).
