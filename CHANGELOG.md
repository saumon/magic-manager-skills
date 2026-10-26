# Changelog

Ce fichier référence les changements structurels du mono-repo (ajout/retrait
de skills). L'historique détaillé de chaque skill vit dans son propre
`skills/<nom>/CHANGELOG.md`.

## 2026-10-26 (maj)

- README et landing page : procédure d'import d'un skill mise à jour pour la
  nouvelle interface de Claude (**Paramètres → Personnalisation → Skills**, puis
  **Ajouter → Importer un skill**), en remplacement de « Compétences → Gérer les
  compétences ».
- `mm-reports-signature` passe en v1.1.1 : le PDF signé d'une pièce jointe reprend
  désormais le **nom d'origine** du document (`Astreinte M BOUROGAA 10-26 - signé.pdf`)
  et non le nom donné par l'upload (`dd51ede5-Astreinte_M_BOUROGAA_10-26 - signé.pdf`).
  Nouvelle option `--original-name`, vérifiée contre le fichier renommé pour éviter
  toute inversion dans un lot. Voir
  [skills/mm-reports-signature/CHANGELOG.md](skills/mm-reports-signature/CHANGELOG.md).
- `mm-reports-signature` passe en v1.1.0 : le nom et la signature ne sont plus
  redemandés à chaque nouvelle conversation sur Claude Desktop et Claude.ai, où le
  script tourne dans un environnement isolé recréé à chaque conversation. Le premier
  lancement produit désormais un **zip personnel** du skill embarquant la
  configuration (`config/`), à réimporter une fois ; la configuration utilisateur
  `~/.config/…` reste lue en priorité. Nouvelle sous-commande `config bundle`, et
  `skills/*/config/` ajouté au `.gitignore` pour ne jamais committer une signature.
  Voir
  [skills/mm-reports-signature/CHANGELOG.md](skills/mm-reports-signature/CHANGELOG.md).

## 2026-10-26

- Ajout du skill `mm-reports-signature` v1.0.0 : signature des notes de frais et
  comptes rendus d'astreintes PDF envoyés par les prestataires — Prénom NOM, date
  du jour et image de signature apposés dans la zone de visa client / responsable,
  en rendu aplati dans la page. Nom et PNG de signature demandés au premier
  lancement puis enregistrés hors du dépôt, dans
  `~/.config/magic-manager-skills/mm-reports-signature/`. Détection automatique de
  trois modèles (note de frais STIME « Visa Client », compte-rendu d'astreintes,
  annexe au rapport d'activité STIME) par le script `scripts/sign_reports.py`
  (PyMuPDF) ; un modèle inconnu donne lieu à un emplacement proposé sur aperçu et
  validé par l'utilisateur. Contrôles avant signature : signature prestataire
  absente (alerte), nom pré-rempli différent (confirmation requise), document déjà
  signé (pas de re-signature). Date pré-remplie conservée, PDF source jamais
  modifié, copie suffixée ` - signé.pdf`. Voir
  [skills/mm-reports-signature/CHANGELOG.md](skills/mm-reports-signature/CHANGELOG.md).
- Landing page et README : passage à cinq skills.

## 2026-09-16

- Ajout du skill `notion-meeting-minutes` v1.0.0 : production d'un compte rendu de
  réunion structuré (en bref, sujets traités, décisions, actions avec porteur et
  échéance, points en suspens, prochaine réunion) à partir de notes prises dans une
  page Notion ou collées dans la conversation. Le skill relève d'abord l'ossature de
  la réunion et signale ce qui manque — action sans porteur, échéance absente, point
  ambigu — plutôt que de le combler : ce qui manque reste `à préciser`. Après
  relecture dans le chat, le format de restitution est demandé à l'utilisateur :
  Markdown, PDF (feuille de style `assets/minutes.css`) ou HTML destiné au
  **copier-coller dans un email Outlook** — gabarit `assets/email_template.html` en
  tableaux imbriqués de largeur fixe (640 px), styles entièrement inline, aucune
  propriété CSS ignorée par le moteur de rendu de Word, et **aucune barre de
  défilement horizontale** à l'ouverture du mail. Le skill ne diffuse rien lui-même :
  les envois Teams restent du ressort de `notion-debrief`. Voir
  [skills/notion-meeting-minutes/CHANGELOG.md](skills/notion-meeting-minutes/CHANGELOG.md).

## 2026-08-20 (maj)

- `resume-shortlist` passe en v1.5.0 : le **profil public LinkedIn** du candidat est
  désormais repris dans la restitution (chat et PDF) quand le dossier n'est pas
  anonymisé — champ au relevé factuel, ligne dans les fiches et dans la section des
  candidats écartés, sans colonne dédiée dans le tableau de synthèse. La recherche
  LinkedIn publique est automatique pour les CV non anonymisés sans URL fournie, avec
  confirmation stricte : le lien n'est affiché qu'en cas de correspondance unique ; sinon
  `ambigu` (homonymes) ou `non trouvé`. Cet élément n'entre jamais dans le score, la
  catégorie, la confiance ni l'indice de cohérence. L'étape 1 ne demande plus le format
  de l'offre : elle propose directement de déposer le fichier (PDF, Word ou Markdown) ou
  d'en coller le texte. La restitution porte désormais le **nom du skill et sa version**
  (chat et PDF), et le PDF ajoute en pied de rapport l'URL du projet
  <https://saumon.github.io/magic-manager-skills/>. Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).
- `resume-to-markdown` passe en v1.0.2 : raccourcissement de la description
  du frontmatter pour améliorer le rendu dans Claude Desktop, puis passage en
  bloc YAML multi-ligne `>-` pour fiabiliser le parsing de `description`.
  Voir
  [skills/resume-to-markdown/CHANGELOG.md](skills/resume-to-markdown/CHANGELOG.md).

## 2026-08-20

- `notion-debrief` passe en v1.3.1 : correction du frontmatter (`author: "saumon"`
  au lieu de `author: "magic-manager-skills"`). Voir
  [skills/notion-debrief/CHANGELOG.md](skills/notion-debrief/CHANGELOG.md).
- `resume-to-markdown` passe en v1.0.1 : correction du frontmatter
  (`author: "saumon"` au lieu de `author: "magic-manager-skills"`). Voir
  [skills/resume-to-markdown/CHANGELOG.md](skills/resume-to-markdown/CHANGELOG.md).

- `resume-shortlist` passe en v1.4.0 : notation rendue reproductible. Un même lot rejoué
  avec le même référentiel doit désormais rendre les mêmes catégories, le même ordre de
  classement et des scores à ± 3 points. La lecture des CV est séparée de la notation par
  un **relevé factuel dénombrable** produit à l'étape 4, les quatre paliers du barème sont
  chiffrés pour les quatre critères (ils ne l'étaient que pour 100 %), les CV sont traités
  dans un ordre fixe, et les points laissés à l'appréciation sont désormais réglés :
  arrondi, départage à score égal, barème de la confiance de l'analyse, priorité de
  rattachement et seuils chiffrés des signaux de cohérence. Le référentiel validé
  (must-have, compétences, poids) est restitué en fin d'étape 3 dans un bloc réutilisable
  tel quel d'une analyse à l'autre. Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).

## 2026-08-19

- `resume-shortlist` passe en v1.3.0 : prise en charge des CV au format
  Markdown (`.md`), en plus du PDF et du Word (`.docx`) déjà supportés. Un CV
  Markdown est par nature toujours exploitable, il ne peut pas tomber dans la
  rubrique « à traiter manuellement » pour un motif de lisibilité. Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).
- Ajout du skill `resume-to-markdown` v1.0.0 : conversion d'un CV PDF ou Word
  (`.docx`) en fichier Markdown par dépouillement de forme — photo, images,
  logos, icônes, couleurs, colonnes et jauges disparaîssent, l'intégralité du
  contenu textuel est conservée, dans l'ordre exact du document source et sans
  gabarit imposé. Le fichier produit reprend à l'identique le nom du fichier
  source, seule l'extension devient `.md`, le nom exact étant demandé à
  l'utilisateur plutôt que reconstitué quand il n'est pas connu. Destiné à
  alimenter plus tard `resume-shortlist`, dont le traitement bute sur les CV
  chargés en images. Voir
  [skills/resume-to-markdown/CHANGELOG.md](skills/resume-to-markdown/CHANGELOG.md).
- `resume-shortlist` passe en v1.2.0 : ajout d'un tableau « Appréciation des
  compétences techniques » pour chaque candidat, retenus comme écartés, dans la
  synthèse du chat comme dans le PDF. Chaque compétence listée dans l'offre y
  est positionnée sur quatre niveaux (hors sujet / peu pertinent / moyen /
  bien), dans l'ordre de l'offre, sans modifier le score. Les compétences
  techniques sont désormais extraites et validées dès l'étape 2, et
  `skills/resume-shortlist/assets/report.css` porte le rendu en sélecteur à
  quatre segments. Corrige au passage le tableau de synthèse, qui s'affichait
  dans le chat comme un bloc de balises HTML brutes : la restitution du fil de
  discussion est désormais explicitement en Markdown seul, le HTML restant
  réservé au fichier converti en PDF. Corrige également les marges du PDF, qui
  restaient bien plus larges que prévu et tassaient le rapport sur les deux
  tiers de la largeur. Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).

## 2026-08-18

- `resume-shortlist` passe en v1.1.0 : colonne « Fichier » dans le tableau de
  synthèse, section obligatoire « Candidats écartés (must-have non satisfait) »
  avec les motifs de refus, marges du PDF resserrées et correction du tableau
  qui débordait (barre de défilement horizontale, texte illisible). Mise en
  forme du rapport revue : séparateurs entre fiches, titres non numérotés,
  police légèrement agrandie. Ajout de la feuille de style
  `skills/resume-shortlist/assets/report.css`, appliquée à la conversion PDF.
  Voir
  [skills/resume-shortlist/CHANGELOG.md](skills/resume-shortlist/CHANGELOG.md).

## 2026-08-11

- Ajout de la landing page statique [`docs/index.html`](docs/index.html),
  publiée via GitHub Pages depuis le dossier `/docs` : présentation du projet,
  de la stack visée (Teams via Kommunicator, Notion, Claude), des skills
  disponibles et de la procédure d'installation. Page autonome (HTML + CSS + JS
  inline, aucune dépendance externe), en français, responsive.

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
