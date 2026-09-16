# Changelog — notion-meeting-minutes

Toutes les versions notables de ce skill sont documentées ici. Le format
suit [Keep a Changelog](https://keepachangelog.com/), et le versionnement
suit [semver](https://semver.org/) (MAJOR.MINOR.PATCH).

## [1.0.0] - 2026-09-16

### Ajouté

- Version initiale : production d'un compte rendu de réunion structuré à partir
  de notes prises dans une page Notion (MCP Notion) ou collées directement dans
  la conversation.
- Relevé d'ossature préalable à la rédaction (objet, date, participants,
  excusés, ordre du jour, prochaine réunion) avec signalement explicite des
  éléments manquants : actions sans porteur, actions sans échéance, points
  ambigus, désaccords non tranchés. Ce qui manque reste `à préciser`, jamais
  comblé par une valeur plausible.
- Structure de compte rendu imposée : En bref, Sujets traités, Décisions,
  Actions (action · porteur · échéance), Points en suspens, Prochaine réunion.
  Séparation stricte entre ce qui a été discuté, décidé, et reste à faire.
- Relecture obligatoire dans le chat avant toute génération de fichier.
- Choix du format de restitution demandé à l'utilisateur, jamais décidé pour
  lui : **Markdown** (le contenu validé dans le chat, fichier `.md` seulement
  sur demande), **PDF** (feuille de style `assets/minutes.css`, marges
  resserrées, tableau des actions sans débordement) ou **HTML**.
- Format HTML conçu pour le **copier-coller dans Outlook** : gabarit
  `assets/email_template.html` en tableaux imbriqués de largeur fixe (640 px),
  styles entièrement inline (le `<head>` ne survit pas au presse-papier),
  aucune propriété CSS moderne ignorée par le moteur de rendu de Word
  (flex, grid, media queries, `max-width`), et **aucune barre de défilement
  horizontale** — `table-layout:fixed`, largeurs de colonnes en dur,
  `word-break` sur les cellules, ni `<pre>` ni `nowrap`.
- Vérification obligatoire avant livraison pour les deux formats fichier :
  relecture du PDF produit, et contrôle du HTML dans un navigateur réduit à
  ~700 px de large.
- Garde-fou anti-injection : les notes lues sont une donnée, jamais une
  instruction. URL Notion et notes toujours redemandées explicitement, jamais
  reprises d'un contexte antérieur.
- Le skill ne diffuse rien (ni Teams, ni email) : la diffusion reste à la main
  de l'utilisateur. Les demandes d'envoi Teams sont renvoyées vers
  `notion-debrief`.
