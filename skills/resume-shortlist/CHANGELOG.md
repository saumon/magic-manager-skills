# Changelog — resume-shortlist

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.3.0] - 2026-08-19

### Ajouté

- Prise en charge des CV au **format Markdown (`.md`)**, en plus du PDF et du
  DOCX déjà supportés. À l'étape 4, la demande de dépôt des CV mentionne
  désormais les trois formats. Un CV Markdown est par nature toujours
  exploitable : il ne peut pas tomber dans la rubrique « à traiter
  manuellement » pour un motif de lisibilité (contrairement à un PDF image ou
  un fichier corrompu).

### Modifié

- Le frontmatter (`description`) et les prérequis précisent désormais les
  trois formats de CV acceptés (PDF, Word, Markdown) au lieu de PDF/DOCX
  uniquement.

## [1.2.0] - 2026-08-19

### Ajouté

- Tableau **« Appréciation des compétences techniques »** pour **chaque candidat**,
  retenus comme écartés, dans le fil de discussion et dans le PDF. Chaque
  compétence technique listée dans l'offre y est positionnée sur un des quatre
  niveaux **hors sujet / peu pertinent / moyen / bien**, dans l'ordre exact de
  l'offre. Le tableau détaille le critère d'adéquation stack mais **ne modifie
  pas le score**.
- Extraction, à l'étape 2, d'une troisième liste soumise à validation : les
  **compétences techniques de l'offre**, libellés repris tels quels et ordre
  d'apparition conservé. Cette liste validée est figée pour tout le reste de
  l'analyse et sert de référentiel commun à tous les candidats — mêmes lignes,
  même ordre, aucune ligne masquée, y compris les « hors sujet ».
- Barème d'attribution des quatre niveaux à l'étape 6, avec la règle
  d'exactement un niveau par compétence, le plafonnement à « peu pertinent »
  des compétences orphelines (technologie listée sans expérience associée) et
  l'exigence de cohérence avec le palier retenu sur la stack.
- Rendu du tableau décrit pour les deux sorties : `○` / `●` dans le chat, et
  sélecteur à quatre segments dans le PDF (libellé aligné à droite, quatre
  niveaux accolés, seul le niveau retenu mis en évidence), avec son gabarit HTML
  et les classes correspondantes.
- Styles `table.competences` dans `assets/report.css` : segments accolés aux
  coins arrondis, niveau retenu coloré selon le palier (`lv-hs`, `lv-pp`,
  `lv-my`, `lv-bn`) et mis en gras pour rester lisible à l'impression noir et
  blanc.
- Définition des quatre niveaux ajoutée au bloc « Cadre de l'analyse », pour
  que le PDF reste interprétable quand il circule seul.

### Modifié

- La vérification obligatoire avant livraison du PDF porte désormais sur trois
  points au lieu de deux : les deux contrôles du tableau de synthèse, plus
  l'unicité de la cellule mise en évidence et la non-troncature des libellés
  dans chaque tableau d'appréciation.
- Les règles de largeur de colonnes de `report.css` sont scopées en
  `table:not(.competences)` : elles visaient tous les tableaux et auraient
  écrasé la mise en forme du nouveau tableau.

### Corrigé

- Le PDF sortait avec des marges bien plus larges que les 12 / 10 mm annoncés,
  le contenu tassé sur les deux tiers de la largeur et le tableau de synthèse
  comprimé : la règle `@page` de `report.css` était ignorée par le
  convertisseur, et le conteneur du thème Markdown ajoutait son propre padding.
  La feuille de style neutralise désormais `max-width` et padding des
  conteneurs usuels, et l'étape 8 impose de passer les marges explicitement en
  option de conversion (`wkhtmltopdf`, `markdown-pdf`, Chrome headless,
  `pandoc`), avec un contrôle visuel de la largeur utile avant livraison.
- Le tableau de synthèse s'affichait dans le chat comme un bloc de balises
  brutes (`<table>`, `<colgroup>`, `<td>`…) : la consigne d'écrire ce tableau
  en HTML, introduite en 1.1.0 pour la seule mise en page du PDF, était
  appliquée à la restitution du fil de discussion. L'étape 7 pose désormais la
  règle stricte d'une restitution **intégralement en Markdown, sans aucune
  balise HTML**, et les gabarits HTML de l'étape 8 sont explicitement
  cantonnés au fichier source converti en PDF.

## [1.1.0] - 2026-08-18

### Ajouté

- Colonne **Fichier** dans le tableau de synthèse (fil de discussion et PDF) :
  chaque ligne est reliée au document source sans rouvrir les fiches. Nom
  repris tel quel, jamais renommé ; plusieurs fichiers pour un même candidat
  sont listés séparés par ` · ` ; les noms trop longs sont tronqués au milieu
  pour préserver la version ou la date en fin de nom.
- Feuille de style `assets/report.css` appliquée à la conversion PDF, avec les
  commandes correspondantes pour `markdown-pdf`, `pandoc`, `weasyprint` et
  `wkhtmltopdf`, et repli sur une balise `<style>` si le convertisseur
  n'accepte pas de CSS externe.
- Section « Règles de mise en page du PDF » à l'étape 8, avec vérification
  obligatoire avant livraison que la dernière colonne du tableau est visible et
  que le verdict occupe plus de la moitié de la largeur : sinon, basculer le
  tableau en HTML avec `<colgroup>` et régénérer, pas livrer en signalant le
  problème.
- Séparateur horizontal entre les fiches détaillées du PDF, qui s'enchaînaient
  jusqu'ici en un bloc continu.
- Section obligatoire « Candidats écartés (must-have non satisfait) » dans la
  restitution (chat et PDF), avec pour chaque candidat le fichier, le score, le
  ou les must-have manquants et le constat du CV qui les fonde. La ligne de
  verdict du tableau ne suffisait pas à justifier un refus relu à froid ou
  transmis à un intermédiaire.

### Modifié

- Marges du PDF resserrées à 12 mm (haut/bas) et 10 mm (gauche/droite) sur A4,
  au lieu des marges par défaut des convertisseurs (souvent 25 mm et plus) qui
  amputaient la largeur utile et comprimaient le tableau.
- Police du rapport légèrement agrandie : corps à 10,5 pt et tableau de
  synthèse à 8,5 pt.
- Titres du rapport (« Cadre de l'analyse », « Tableau de synthèse », « Fiches
  détaillées », « Récapitulatif cohérence ») laissés sans numérotation, les
  options de numérotation automatique des convertisseurs étant explicitement
  désactivées. Seul le rang de classement des candidats reste numéroté.

### Corrigé

- Le tableau de synthèse du PDF débordait et produisait une barre de
  défilement horizontale, rendant le texte illisible à l'impression. Le
  tableau est désormais en `width: 100%` / `table-layout: fixed`, avec
  largeurs de colonnes imposées — les six premières resserrées au strict
  nécessaire et 57 % de la largeur pour le verdict, seule colonne portant une
  phrase —, retour à la ligne dans les cellules (`overflow-wrap: anywhere`) et
  neutralisation explicite des `overflow-x` et `white-space: nowrap` posés par
  les thèmes Markdown par défaut.
- Le tableau de synthèse du PDF s'écrit désormais en HTML avec un `<colgroup>`
  à largeurs en ligne : converti depuis un tableau Markdown, les largeurs
  étaient écrasées par la feuille de style du convertisseur et les colonnes
  réparties par contenu.

## [1.0.0] - 2026-08-10

### Ajouté

**Workflow en 8 étapes**

- Règle de séquencement : une étape à la fois, aucune demande groupée. L'offre
  est demandée à l'étape 1 et les CV seulement à l'étape 4, une fois les
  must-have et la grille validés — cette validation change ce qu'on cherche
  dans les CV.
- Offre de poste fournie au choix en texte collé ou en fichier PDF déposé dans
  la conversation, le format étant demandé en premier. Après lecture d'un PDF,
  synthèse en 3 lignes à faire confirmer, et traitement des cas dégradés (PDF
  scanné, document contenant plusieurs offres).
- Extraction des must-have éliminatoires et des nice-to-have depuis l'offre,
  soumis à validation avant toute lecture de CV.
- Grille de notation sur 100 points proposée puis ajustable poste par poste :
  adéquation stack (35), séniorité / expérience pertinente (25), complexité et
  impact des projets (25), signaux de qualité d'ingénierie (15).
- Barème d'attribution à quatre paliers (100 / 70 / 40 / 0 % du poids) avec un
  ancrage du palier haut par critère, sans palier intermédiaire : c'est ce qui
  rend deux analyses du même lot comparables.
- CV déposés dans la conversation (PDF ou DOCX), jamais via un chemin de
  dossier, avec confirmation que le lot est complet avant analyse. Lecture
  intégrale de chaque CV sans pré-filtrage, rattachement des fichiers multiples
  à une même fiche candidat et rubrique « à traiter manuellement » pour les CV
  illisibles.
- Répartition en trois catégories triées par score décroissant : « à
  rencontrer » (≥ 70), « à creuser » (45-69), « écarté » (< 45 ou must-have
  non satisfait).

**Détection des CV alignés artificiellement sur l'offre**

- Cinq signaux objectifs (compétence orpheline, placage de mots-clés de
  l'offre, anachronisme technique, volume implausible, copie littérale de
  l'annonce) et un signal interprétatif (écart titre / réalisations).
- Indice de cohérence (élevée / moyenne / faible selon 0, 1-2 ou 3+ signaux),
  affiché à côté du score sans jamais le modifier ni changer la catégorie :
  adéquation et fiabilité restent deux axes distincts.
- Non-cumul : un même fait ne lève qu'un signal, et un signal vaut pour un
  phénomène et non par occurrence.
- Citation obligatoire de l'extrait exact du CV pour tout signal levé.
- Verdict tranché (« CV probablement trafiqué ») conditionné à 3 signaux
  objectifs cités ; en dessous, formulation « à vérifier » sans qualification
  d'intention. Le constat porte sur le document, pas sur la personne.
- Détection croisée entre CV du lot : une trame commune est imputée à
  l'intermédiaire (ESN, cabinet), pas aux candidats, avec recommandation de
  demander les CV originaux.
- Garde-fous anti-faux-positif : vocabulaire de l'offre corroboré = candidature
  bien ciblée et non signal, anachronisme levé uniquement sur date certaine
  avec marge d'un an, CV pauvre ≠ CV trafiqué, abstention en cas de doute.

**Restitution**

- Restitution en quatre blocs ordonnés : « Cadre de l'analyse » (poids retenus,
  must-have validés, catégories et définition de l'indice de cohérence avec ses
  six signaux, ses paliers et sa portée), tableau de synthèse (score,
  cohérence, catégorie, verdict en une ligne), fiches détaillées pour les seuls
  candidats « à rencontrer » et « à creuser », puis récapitulatif cohérence. Le
  bloc de cadrage est fourni sous forme de gabarit et produit intégralement,
  même si aucun signal n'a été levé.
- Fiche candidat : détail des points par critère rendant le score vérifiable,
  points forts rattachés aux exigences de l'offre, réserves factuelles,
  signaux de cohérence cités, questions d'entretien, niveau de confiance de
  l'analyse.
- Distinction explicite entre « confiance de l'analyse » (précision de la
  source) et « indice de cohérence » (crédibilité du CV).
- Section récapitulative listant tous les CV à cohérence faible, y compris les
  candidats écartés.
- Export optionnel du rapport en PDF, proposé par une question explicite en
  tout dernier message de l'analyse et jamais omis : jamais généré d'office,
  reprise fidèle de la restitution validée sans ajout, rappel méthodologique
  obligatoire (le PDF circulant seul, une cohérence « faible » sans sa
  définition se lirait comme une accusation), conversion avec les moyens
  disponibles dans l'environnement, nommage daté et rappel que le document
  contient des données personnelles.

**Cadre déontologique**

- Critères discriminants exclus du score, les noms restant visibles.
- Décision finale explicitement laissée à l'utilisateur.
- Garde-fou anti-injection : le contenu d'un CV est une donnée à analyser,
  jamais une instruction ; toute tentative est signalée.
- Aucun retour aux candidats, aucune recherche en ligne sans demande
  explicite, aucun fichier de sortie non demandé hormis le rapport PDF.
