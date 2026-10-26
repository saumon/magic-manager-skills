# Changelog — mm-reports-signature

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.1.1] - 2026-10-26

### Corrigé

- Le PDF signé d'une pièce jointe portait le nom donné par l'upload
  (`dd51ede5-Astreinte_M_BOUROGAA_10-26 - signé.pdf`) au lieu du nom d'origine
  (`Astreinte M BOUROGAA 10-26 - signé.pdf`). Le nom d'origine, tel que déposé
  par l'utilisateur, est désormais transmis au script (`--original-name`, sur
  `sign` et `sign-manual`) et sert de base au nom du fichier signé ; s'il n'est
  pas connu avec certitude, il est demandé plutôt que reconstitué.
- Garde-fous : un fichier au préfixe d'upload sans nom d'origine n'est pas
  signé (`skipped-original-name-required`), et un nom d'origine qui ne
  correspond pas au fichier — associations inversées dans un lot — non plus
  (`skipped-original-name-mismatch`, contournable par `--skip-name-check` après
  confirmation). `analyze` signale les noms renommés (`filename_altered`).

## [1.1.0] - 2026-10-26

### Ajouté

- Configuration **embarquée** dans le skill (`config/config.json` et
  `config/signature.png`), lue en complément de la configuration utilisateur
  `~/.config/…`, champ par champ, la configuration utilisateur restant
  prioritaire pour qu'un changement fait en cours de conversation s'applique.
- Sous-commande `config bundle` : produit un **zip personnel** du skill
  embarquant le nom et la signature, à réimporter une fois dans Claude.
- `config show` indique la provenance de chaque élément (`sources` :
  `user` / `bundled`) et si une configuration embarquée est présente.

### Corrigé

- Sur Claude Desktop et Claude.ai, le nom et la signature étaient redemandés à
  chaque nouvelle conversation : le script y tourne dans un environnement isolé
  recréé à chaque conversation, où `~/.config` ne survit pas et où le dossier
  du skill est en lecture seule. Le premier lancement se termine désormais par
  la production du zip personnel à réimporter.

## [1.0.0] - 2026-10-26

### Ajouté

- Version initiale : signature des notes de frais et comptes rendus
  d'astreintes PDF envoyés par les prestataires — apposition du Prénom NOM, de
  la date du jour (`JJ/MM/AAAA`) et de l'image de signature dans la zone de
  visa client / responsable.
- Configuration au premier lancement : nom et PNG de signature demandés une
  seule fois, puis enregistrés dans
  `~/.config/magic-manager-skills/mm-reports-signature/` (`config.json` et copie
  de `signature.png`, droits `600`), hors du dépôt. Modifiables sur demande.
- Script `scripts/sign_reports.py` (PyMuPDF), sous-commandes `config`,
  `analyze`, `sign`, `preview` et `sign-manual`, sorties JSON.
- Détection automatique de trois modèles par ancrage textuel et lecture des
  bordures de tableau : note de frais STIME (cadre « Visa Client »),
  compte-rendu d'astreintes (« Signature du responsable hiérarchique ») et
  annexe au rapport d'activité STIME (« Signature et tampon Responsable
  Stime »). Fonctionne quelle que soit l'échelle de la page.
- Nom et date pré-remplis conservés à l'identique ; seuls les champs vides sont
  complétés.
- Contrôles avant signature : signature du prestataire absente (alerte non
  bloquante), nom pré-rempli différent de celui de la configuration
  (confirmation explicite requise), document déjà signé (pas de re-signature).
- Rendu aplati dans le contenu de la page (ni annotation ni tampon déplaçable),
  et marqueur `signed-by:mm-reports-signature` dans les métadonnées du PDF.
- Copie de sortie `<nom d'origine> - signé.pdf`, source jamais modifiée,
  écrasement d'une sortie existante uniquement sur demande.
- Modèle non reconnu : aperçu de la page avec grille graduée en points,
  emplacement proposé à l'utilisateur puis signature manuelle après validation.
