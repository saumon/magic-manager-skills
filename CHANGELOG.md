# Changelog

Ce fichier référence les changements structurels du mono-repo (ajout/retrait
de skills). L'historique détaillé de chaque skill vit dans son propre
`skills/<nom>/CHANGELOG.md`.

## 2026-08-10

- Ajout du skill `resume-shortlist` v1.0.0 : tri de CV face à une offre d'emploi
  (texte collé ou PDF), documents déposés dans la conversation, avec must-have
  éliminatoires validés par l'utilisateur, grille de notation ajustable,
  détection des CV alignés artificiellement sur l'offre, short list en trois
  catégories et export PDF optionnel du rapport. Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).
- Correction du README : `notion-debrief` y était encore annoncé en v1.2.0
  alors que son `SKILL.md` déclare la v1.3.0.

## 2026-08-03

- `notion-debrief` passe en v1.3.0 : refonte du template de carte adaptive
  (puces réellement rendues dans Teams, actions scindées en « Fait » / « À faire »).
- Ajout du fichier `LICENSE` (MIT), cohérent avec le champ `license`
  déclaré dans les `SKILL.md`.
- `notion-debrief` passe en v1.2.0. Le tag `notion-debrief-v1.1.0` avait été
  publié prématurément (contenu identique à la 1.0.0) : il est laissé en place
  et la numérotation reprend en 1.2.0.

## 2026-07-31

- Création du mono-repo `magic-manager-skills`.
- Ajout du skill `notion-debrief` v1.0.0, dérivé d'un cas d'usage réel
  (débriefing d'un dossier d'internalisation envoyé à un collaborateur).
  Voir [skills/notion-debrief/CHANGELOG.md](skills/notion-debrief/CHANGELOG.md).
