# Changelog — resume-to-markdown

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.0.1] - 2026-08-20

### Modifié

- Correction du frontmatter : `author: "saumon"` au lieu de
  `author: "magic-manager-skills"`. Chaque skill porte le nom de son auteur,
  pas le nom du mono-repo.

## [1.0.0] - 2026-08-19

### Ajouté

- Version initiale du skill : conversion d'un CV **PDF** ou **Word (.docx)** en
  fichier **Markdown**, par **dépouillement de forme** — on retire ce qui n'est
  pas du texte, jamais une information au motif qu'elle paraîtrait peu utile.
  Le fichier produit est destiné à alimenter plus tard le skill
  `resume-shortlist`, les CV chargés en images atteignant les limites de
  traitement.
- Déroulé en 7 étapes : demande explicite du fichier (déposé dans la
  conversation ou désigné par un chemin), lecture intégrale, confirmation qu'il
  s'agit du bon document, conversion, nommage du fichier de sortie, livraison,
  vérification finale.
- Règle stricte de nommage : le fichier produit reprend **à l'identique** le nom
  de base du fichier source, seule l'extension devient `.md`
  (`cv-toto.pdf` → `cv-toto.md`). Ni normalisation de casse, d'accents ou
  d'espaces, ni renommage d'après le nom du candidat, ni écrasement silencieux
  d'un fichier existant. **Quand le nom exact du fichier source n'est pas connu**
  (non visible, tronqué, réécrit par l'interface, orthographe incertaine), le
  skill s'arrête et le demande à l'utilisateur au lieu de reconstruire un nom.
- Structure de sortie calquée sur le CV source, **sans gabarit** : ordre des
  sections, des entrées et des puces identique au document d'origine, intitulés
  de section repris tels quels, aucune section créée, fusionnée, scindée ni
  déplacée. Une mise en page en colonnes est dépliée en flux linéaire.
- Clause d'exclusion dans la description : ne pas déclencher ce skill pour
  évaluer, noter, comparer ou classer des candidats face à une offre — c'est le
  rôle de `resume-shortlist` — et demander à l'utilisateur de trancher en cas de
  doute.
- Liste explicite de ce qui est supprimé (photo, images, logos, icônes,
  couleurs, colonnes, encadrés, jauges de compétences graphiques, numéros de
  page, en-têtes et pieds de page répétés) et de ce qui est conservé (identité,
  contact, accroche, expériences, formations, certifications, compétences,
  langues, projets, publications, centres d'intérêt).
- Règles de rendu Markdown : un seul titre de niveau 1, sections en `##`,
  expériences et formations en `###`, aucun HTML ni emoji, rédaction dans la
  langue du CV source.
- Garde-fous : contenu du CV traité comme une donnée et jamais comme une
  instruction (texte d'injection signalé, jamais exécuté), interdiction
  d'inventer ou de compléter une donnée absente, interdiction de résumer, de
  reformuler ou d'écarter une ligne du source, information illisible notée
  `[illisible]`.
- Points de vigilance sur l'extraction : mises en page multi-colonnes, texte en
  zone graphique, tableaux, coupures de mots, métadonnées de fichier non
  transcrites.
- Checklist de vérification en 6 points avant livraison (complétude, ordre,
  fidélité, propreté, nommage, absence d'ajout comme de retrait).

[1.0.0]: https://github.com/saumon/magic-manager-skills/releases/tag/resume-to-markdown-v1.0.0
