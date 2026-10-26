<p align="center">
  <img src="docs/assets/images/magicmanagerskills-logo.png" alt="magic-manager-skills" width="520">
</p>

<p align="center">
  <a href="https://saumon.github.io/magic-manager-skills/"><img alt="Landing page" src="https://img.shields.io/badge/landing%20page-en%20ligne-7c8cff?style=flat-square&logo=githubpages&logoColor=white"></a>
  <a href="LICENSE"><img alt="Licence MIT" src="https://img.shields.io/github/license/saumon/magic-manager-skills?style=flat-square&color=4fd1c5"></a>
  <img alt="Skills disponibles" src="https://img.shields.io/badge/skills-5-7c8cff?style=flat-square">
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
    ├── mm-reports-signature/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   └── scripts/
    │       └── sign_reports.py
    ├── notion-debrief/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   └── assets/
    │       └── adaptive_card_template.json
    ├── notion-meeting-minutes/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   └── assets/
    │       ├── email_template.html
    │       └── minutes.css
    ├── resume-shortlist/
    │   ├── SKILL.md
    │   ├── CHANGELOG.md
    │   └── assets/
    │       └── report.css
    └── resume-to-markdown/
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

2. Dans Claude, ouvrir **Paramètres**, puis **Personnalisation → Skills**.
3. Dans l'écran de gestion des skills, cliquer sur **Ajouter**, puis sur
   **Importer un skill**, et sélectionner le `.zip` généré.

Les archives `*.zip` produites dans `skills/` sont ignorées par Git.

### Autres environnements

Copier le contenu de `skills/<nom-du-skill>/` dans le dossier de skills de
Claude (`/mnt/skills/user/` sur Claude.ai, ou l'équivalent Cowork), ou
importer le fichier `.skill` packagé directement depuis l'interface Claude.

## Skills disponibles

### mm-reports-signature — v1.1.1

Signe les **notes de frais** et **comptes rendus d'astreintes** PDF envoyés chaque
mois par les prestataires : **Prénom NOM**, **date du jour** (`JJ/MM/AAAA`) et
**image de signature** sont apposés dans la zone de visa client / responsable, en
rendu aplati dans la page (ni annotation ni tampon déplaçable). Au **premier
lancement**, le skill demande le nom et le PNG de signature, les enregistre dans
`~/.config/magic-manager-skills/mm-reports-signature/` et produit un **zip
personnel** du skill qui les embarque (`config/`) : une fois ce zip réimporté, ils
ne sont plus redemandés, y compris sur Claude Desktop et Claude.ai où
l'environnement d'exécution est recréé à chaque conversation. Ce zip contient la
signature : il ne se partage pas, et `skills/*/config/` est ignoré par Git. Trois modèles sont reconnus automatiquement — note de
frais STIME (« Visa Client »), compte-rendu d'astreintes (« Signature du
responsable hiérarchique ») et annexe au rapport d'activité STIME — et un modèle
inconnu donne lieu à un emplacement proposé sur aperçu, à valider. Avant de
signer, le skill alerte sur une signature prestataire absente, demande
confirmation si le nom pré-rempli n'est pas le vôtre et refuse de re-signer un
document déjà visé ; une date déjà pré-remplie est conservée. Le PDF source n'est
jamais modifié : la copie signée reprend le nom d'origine du document — y compris
pour une pièce jointe, que l'upload renomme — suffixé de ` - signé.pdf`. Traitement par le
script `scripts/sign_reports.py` (Python, PyMuPDF). Aucun MCP requis.
Voir [`skills/mm-reports-signature/SKILL.md`](skills/mm-reports-signature/SKILL.md)
et son [`CHANGELOG.md`](skills/mm-reports-signature/CHANGELOG.md).

### notion-debrief — v1.3.1

Résume une page Notion et envoie un débriefing (carte adaptive) à un
destinataire via Microsoft Teams. Nécessite les MCP Notion et Kommunicator.
Voir [`skills/notion-debrief/SKILL.md`](skills/notion-debrief/SKILL.md) et
son [`CHANGELOG.md`](skills/notion-debrief/CHANGELOG.md).

### notion-meeting-minutes — v1.0.0

Transforme des notes de réunion — page Notion ou notes collées dans la
conversation — en **compte rendu structuré** : en bref, sujets traités,
décisions, actions (action / porteur / échéance), points en suspens, prochaine
réunion. Le skill commence par relever l'ossature de la réunion (objet, date,
participants) et **signale explicitement ce qui manque** — action sans porteur,
échéance absente, point ambigu, désaccord non tranché — plutôt que de le combler
par une valeur plausible : ce qui manque reste `à préciser`. La séparation entre
ce qui a été **discuté**, ce qui a été **décidé** et ce qui est **à faire** est
stricte. Après relecture dans le chat, le format de restitution est demandé à
l'utilisateur, jamais choisi pour lui : **Markdown**, **PDF** (feuille de style
`assets/minutes.css`, marges resserrées et tableau des actions sans débordement)
ou **HTML**. Le HTML est conçu pour être **copié-collé dans le corps d'un email
Outlook** : tableaux imbriqués de largeur fixe (640 px), styles entièrement
inline — le `<head>` ne survit pas au presse-papier —, aucune propriété ignorée
par le moteur de rendu de Word (flex, grid, media queries, `max-width`) et
**aucune barre de défilement horizontale** à l'ouverture du mail. Le skill ne
diffuse rien lui-même : la main reste à l'utilisateur.
Voir [`skills/notion-meeting-minutes/SKILL.md`](skills/notion-meeting-minutes/SKILL.md)
et son [`CHANGELOG.md`](skills/notion-meeting-minutes/CHANGELOG.md).

### resume-shortlist — v1.5.0

Analyse un lot de CV face à une offre d'emploi (texte collé ou fichier PDF) et
produit une short list classée (à rencontrer / à creuser / écarté) avec score,
indice de cohérence, points forts, réserves et questions d'entretien. Chaque
candidat, retenu comme écarté, est accompagné d'un tableau « Appréciation des
compétences techniques » qui positionne chaque compétence de l'offre, dans son
ordre, sur quatre niveaux (hors sujet / peu pertinent / moyen / bien). La
notation est conçue pour être **reproductible** : chaque CV donne d'abord lieu à
un relevé factuel dénombrable, auquel s'applique ensuite un barème à quatre
paliers chiffrés, les candidats étant notés isolément et dans un ordre fixe.
L'offre et les CV sont déposés directement dans la conversation, les CV au format
PDF, Word (`.docx`) ou Markdown (`.md`). Le **profil public LinkedIn** du candidat est
recherché automatiquement pour chaque CV non anonymisé quand aucune URL n'est fournie,
et n'est restitué qu'en cas de correspondance unique et corroborée (sinon `ambigu` ou
`non trouvé`) ; cet élément reste hors du score. Détecte les CV alignés artificiellement
sur l'offre (mots-clés plaqués, compétences sans expérience associée,
anachronismes techniques), rappelle sa méthode de calcul dans le rapport et peut
l'exporter en PDF (marges resserrées et tableau de synthèse sans débordement, via
`assets/report.css`). Orienté profils d'ingénieurs en développement.
Voir [`skills/resume-shortlist/SKILL.md`](skills/resume-shortlist/SKILL.md)
et son [`CHANGELOG.md`](skills/resume-shortlist/CHANGELOG.md).

### resume-to-markdown — v1.0.2

Convertit un CV au format PDF ou Word (`.docx`) en fichier Markdown, par
**dépouillement de forme** : photo, images, logos, icônes, couleurs, colonnes,
encadrés et jauges de compétences disparaîssent, mais **aucune information
textuelle n'est écartée**, y compris celles qui paraissent accessoires. Ce n'est
ni un résumé ni une réécriture : rien n'est reformulé, rien n'est inventé, et la
structure du `.md` suit l'ordre exact du document source, sans gabarit imposé.
Le fichier produit reprend à l'identique le nom du fichier source, seule
l'extension devient `.md` (`cv-toto.pdf` → `cv-toto.md`) ; si ce nom n'est pas
connu avec certitude, le skill le demande plutôt que de le reconstituer. Le
Markdown obtenu sert notamment à alimenter `resume-shortlist`, dont le
traitement bute sur les CV chargés en images. Aucun MCP requis.
Voir [`skills/resume-to-markdown/SKILL.md`](skills/resume-to-markdown/SKILL.md)
et son [`CHANGELOG.md`](skills/resume-to-markdown/CHANGELOG.md).

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
