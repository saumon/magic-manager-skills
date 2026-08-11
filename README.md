<p align="center">
  <img src="docs/assets/images/magicmanagerskills-logo.png" alt="magic-manager-skills" width="520">
</p>

<p align="center">
  <a href="https://saumon.github.io/magic-manager-skills/"><img alt="Landing page" src="https://img.shields.io/badge/landing%20page-en%20ligne-7c8cff?style=flat-square&logo=githubpages&logoColor=white"></a>
  <a href="LICENSE"><img alt="Licence MIT" src="https://img.shields.io/github/license/saumon/magic-manager-skills?style=flat-square&color=4fd1c5"></a>
  <img alt="Skills disponibles" src="https://img.shields.io/badge/skills-2-7c8cff?style=flat-square">
  <img alt="Claude Skills" src="https://img.shields.io/badge/Claude-Skills-d97757?style=flat-square&logo=anthropic&logoColor=white">
  <img alt="MCP requis" src="https://img.shields.io/badge/MCP-Notion%20%7C%20Kommunicator-4fd1c5?style=flat-square">
  <img alt="Langue : français" src="https://img.shields.io/badge/langue-fran%C3%A7ais-7c8cff?style=flat-square">
</p>

# magic-manager-skills

Mono-repo de skills Claude pour l'automatisation de tâches de management
(débriefings, suivi RH, reporting, etc.).

Landing page : <https://saumon.github.io/magic-manager-skills/>
(source : [`docs/index.html`](docs/index.html), publiée par GitHub Pages depuis
le dossier `/docs` de la branche `dev`).

## Structure

```text
magic-manager-skills/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── index.html
│   ├── .nojekyll
│   └── assets/
│       └── images/
│           └── magicmanagerskills-logo.png
└── skills/
    ├── notion-debrief/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   └── assets/
    │       └── adaptive_card_template.json
    └── resume-shortlist/
        ├── SKILL.md
        └── CHANGELOG.md
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

### notion-debrief — v1.3.0

Résume une page Notion et envoie un débriefing (carte adaptive) à un
destinataire via Microsoft Teams. Nécessite les MCP Notion et Kommunicator.
Voir [`skills/notion-debrief/SKILL.md`](skills/notion-debrief/SKILL.md) et
son [`CHANGELOG.md`](skills/notion-debrief/CHANGELOG.md).

### resume-shortlist — v1.0.0

Analyse un lot de CV face à une offre d'emploi (texte collé ou fichier PDF) et
produit une short list classée (à rencontrer / à creuser / écarté) avec score,
indice de cohérence, points forts, réserves et questions d'entretien. L'offre
et les CV sont déposés directement dans la conversation. Détecte les CV
alignés artificiellement sur l'offre (mots-clés plaqués, compétences sans
expérience associée, anachronismes techniques), rappelle sa méthode de calcul
dans le rapport et peut l'exporter en PDF. Orienté profils d'ingénieurs en
développement.
Voir [`skills/resume-shortlist/SKILL.md`](skills/resume-shortlist/SKILL.md)
et son [`CHANGELOG.md`](skills/resume-shortlist/CHANGELOG.md).

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
