#!/usr/bin/env python3
"""mm-reports-signature : appose nom, date et signature sur les notes de frais
et comptes rendus d'astreintes envoyés par les prestataires.

Sous-commandes :
  config show                         état de la configuration (JSON)
  config set --name N --signature P   enregistre le nom et une copie du PNG
  config bundle [--out CHEMIN]        zip du skill embarquant la configuration
  analyze PDF...                      détecte le modèle et la zone de visa (JSON)
  sign PDF...                         signe les PDF reconnus -> "<nom> - signé.pdf"
  preview PDF                         rend une page en PNG avec une grille (en points)
  sign-manual PDF --page N --rect ... signe à un emplacement fourni à la main

Dépendance : PyMuPDF (pip install pymupdf).
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

SKILL = "mm-reports-signature"
MARKER = f"signed-by:{SKILL}"
SIGNED_SUFFIX = " - signé"

EXIT_OK, EXIT_PARTIAL, EXIT_NO_CONFIG, EXIT_NO_DEP = 0, 1, 2, 3

try:
    import pymupdf
except ImportError:  # pragma: no cover
    try:
        import fitz as pymupdf  # anciennes versions de PyMuPDF
    except ImportError:
        print(json.dumps({"error": "missing-dependency",
                          "message": "PyMuPDF est requis : pip install pymupdf"}))
        sys.exit(EXIT_NO_DEP)


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

SKILL_DIR = Path(__file__).resolve().parent.parent
BUNDLED_DIR = SKILL_DIR / "config"
BUNDLE_EXCLUDE = {"__pycache__", ".DS_Store"}


def config_dir() -> Path:
    """Configuration utilisateur, modifiable (~/.config/...)."""
    override = os.environ.get("MM_REPORTS_SIGNATURE_HOME")
    if override:
        return Path(override).expanduser()
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "magic-manager-skills" / SKILL


def config_file() -> Path:
    return config_dir() / "config.json"


def read_config(directory: Path) -> dict:
    path = directory / "config.json"
    if not path.is_file():
        return {}
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    sig = cfg.get("signature")
    if sig and not Path(sig).is_absolute():
        cfg["signature"] = str(directory / sig)
    return cfg


def resolve_config() -> tuple:
    """Fusionne, champ par champ, la config utilisateur et la config embarquée
    dans le skill (config/). La config utilisateur l'emporte : le dossier du
    skill peut être en lecture seule, c'est donc là que portent les changements."""
    user, bundled = read_config(config_dir()), read_config(BUNDLED_DIR)
    cfg, sources = {}, {}
    if user.get("full_name"):
        cfg["full_name"], sources["full_name"] = user["full_name"], "user"
    elif bundled.get("full_name"):
        cfg["full_name"], sources["full_name"] = bundled["full_name"], "bundled"
    for origin, src in (("user", user), ("bundled", bundled)):
        sig = src.get("signature")
        if sig and Path(sig).is_file():
            cfg["signature"], sources["signature"] = sig, origin
            break
    cfg["updated_at"] = user.get("updated_at") or bundled.get("updated_at")
    return cfg, sources


def load_config() -> dict:
    return resolve_config()[0]


def config_status() -> dict:
    cfg, sources = resolve_config()
    return {
        "configured": bool(cfg.get("full_name")) and bool(cfg.get("signature")),
        "full_name": cfg.get("full_name"),
        "signature": cfg.get("signature"),
        "sources": sources,
        "bundled_config": (BUNDLED_DIR / "config.json").is_file(),
        "user_config_dir": str(config_dir()),
        "skill_dir": str(SKILL_DIR),
        "skill_dir_writable": os.access(SKILL_DIR, os.W_OK),
        "updated_at": cfg.get("updated_at"),
    }


def cmd_config(args) -> int:
    if args.action == "show":
        print(json.dumps(config_status(), ensure_ascii=False, indent=2))
        return EXIT_OK
    if args.action == "bundle":
        return cmd_bundle(args)

    cfg = read_config(config_dir())
    warnings = []
    if args.name:
        name = " ".join(args.name.split())
        if not name:
            return fail("Nom vide.")
        cfg["full_name"] = name
    if args.signature:
        src = Path(args.signature).expanduser()
        if not src.is_file():
            return fail(f"Fichier introuvable : {src}")
        with open(src, "rb") as fh:
            if fh.read(8) != b"\x89PNG\r\n\x1a\n":
                return fail("La signature doit être une image PNG.")
        pix = pymupdf.Pixmap(str(src))
        if not pix.alpha:
            warnings.append("Le PNG n'a pas de transparence : son fond masquera "
                            "les traits et cadres situés sous la signature.")
        config_dir().mkdir(parents=True, exist_ok=True)
        dst = config_dir() / "signature.png"
        shutil.copyfile(src, dst)
        os.chmod(dst, 0o600)
        cfg["signature"] = "signature.png"
    if not args.name and not args.signature:
        return fail("Rien à enregistrer : préciser --name et/ou --signature.")

    if cfg.get("signature") and Path(cfg["signature"]).is_absolute():
        cfg["signature"] = Path(cfg["signature"]).name
    cfg["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    config_dir().mkdir(parents=True, exist_ok=True)
    config_file().write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(config_file(), 0o600)
    out = config_status()
    out["warnings"] = warnings
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_bundle(args) -> int:
    """Produit un zip du skill embarquant la configuration courante, à réimporter
    dans Claude pour qu'elle survive d'une conversation à l'autre."""
    import zipfile

    cfg, _ = resolve_config()
    if not (cfg.get("full_name") and cfg.get("signature")):
        print(json.dumps({"error": "not-configured", **config_status()},
                         ensure_ascii=False, indent=2))
        return EXIT_NO_CONFIG
    out = Path(args.out).expanduser() if args.out else Path.cwd()
    if out.suffix.lower() != ".zip":
        out = out / f"{SKILL}.zip"
    if out.exists() and not args.force:
        return fail(f"{out} existe déjà (utiliser --force pour l'écraser)")
    out.parent.mkdir(parents=True, exist_ok=True)

    bundled = {
        "full_name": cfg["full_name"],
        "signature": "signature.png",
        "updated_at": cfg.get("updated_at"),
        "bundled_at": dt.datetime.now().isoformat(timespec="seconds"),
    }
    files = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SKILL_DIR.rglob("*")):
            rel = path.relative_to(SKILL_DIR)
            if (rel.parts[0] == "config" or BUNDLE_EXCLUDE & set(rel.parts)
                    or path.suffix == ".pyc" or not path.is_file()):
                continue
            arc = f"{SKILL}/{rel.as_posix()}"
            zf.write(path, arc)
            files.append(arc)
        zf.writestr(f"{SKILL}/config/config.json",
                    json.dumps(bundled, ensure_ascii=False, indent=2))
        zf.write(cfg["signature"], f"{SKILL}/config/signature.png")
        files += [f"{SKILL}/config/config.json", f"{SKILL}/config/signature.png"]
    print(json.dumps({"bundle": str(out), "full_name": cfg["full_name"], "files": files},
                     ensure_ascii=False, indent=2))
    return EXIT_OK


# --------------------------------------------------------------------------- #
# Lecture de la page
# --------------------------------------------------------------------------- #

def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.lower().replace("’", "'").split())


def same_person(a: str, b: str) -> bool:
    key = lambda s: sorted(re.findall(r"[a-z]+", norm(s)))
    return bool(a and b) and key(a) == key(b)


class Line:
    def __init__(self, bbox, text, size, baseline):
        self.rect = pymupdf.Rect(bbox)
        self.text = text
        self.size = size
        self.baseline = baseline

    @property
    def n(self):
        return norm(self.text)

    def __repr__(self):
        return f"Line({self.text!r} @ {tuple(round(v) for v in self.rect)})"


def page_lines(page):
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = " ".join(s["text"].strip() for s in spans)
            out.append(Line(line["bbox"], text, spans[0]["size"], spans[0]["origin"][1]))
    return out


class Grid:
    """Bordures de tableau : segments horizontaux et verticaux de la page."""

    def __init__(self, page):
        self.h, self.v = [], []  # (début, fin, position)
        for d in page.get_drawings():
            for item in d["items"]:
                if item[0] == "re":
                    r = item[1]
                    if r.height <= 2.5 and r.width > 2.5:
                        self.h.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
                    elif r.width <= 2.5 and r.height > 2.5:
                        self.v.append((r.y0, r.y1, (r.x0 + r.x1) / 2))
                    elif d["type"] in ("s", "fs"):
                        self.h += [(r.x0, r.x1, r.y0), (r.x0, r.x1, r.y1)]
                        self.v += [(r.y0, r.y1, r.x0), (r.y0, r.y1, r.x1)]
                elif item[0] == "l":
                    p, q = item[1], item[2]
                    if abs(p.y - q.y) < 1:
                        self.h.append((min(p.x, q.x), max(p.x, q.x), p.y))
                    elif abs(p.x - q.x) < 1:
                        self.v.append((min(p.y, q.y), max(p.y, q.y), p.x))

    def cell(self, x, y, tol=1.5):
        """Plus petit cadre entourant (x, y) ; None pour un bord introuvable."""
        hs = [s[2] for s in self.h if s[0] - tol <= x <= s[1] + tol]
        vs = [s[2] for s in self.v if s[0] - tol <= y <= s[1] + tol]
        above = [p for p in hs if p < y - 0.5]
        below = [p for p in hs if p > y + 0.5]
        left = [p for p in vs if p < x - 0.5]
        right = [p for p in vs if p > x + 0.5]
        return (max(left) if left else None, max(above) if above else None,
                min(right) if right else None, min(below) if below else None)


def has_content(page, region, lines, ignore=()):
    """Vrai si la zone contient une image, un tracé courbe ou du texte."""
    if region.is_empty or region.width < 2 or region.height < 2:
        return False
    for info in page.get_image_info():
        if pymupdf.Rect(info["bbox"]).intersects(region):
            return True
    for annot in page.annots() or []:
        if annot.rect.intersects(region):
            return True
    for d in page.get_drawings():
        if any(it[0] in ("c", "qu") for it in d["items"]) and d["rect"].intersects(region):
            return True
        if any(it[0] == "l" and abs(it[1].x - it[2].x) > 1 and abs(it[1].y - it[2].y) > 1
               for it in d["items"]) and d["rect"].intersects(region):
            return True
    for ln in lines:
        if ln in ignore:
            continue
        inter = ln.rect & region
        if not inter.is_empty and inter.get_area() > 0.5 * ln.rect.get_area():
            return True
    return False


def same_row(line, others, x_min, x_max):
    mid = (line.rect.y0 + line.rect.y1) / 2
    return [o for o in others if o is not line
            and o.rect.y0 - 1 <= mid <= o.rect.y1 + 1
            and x_min <= o.rect.x0 < x_max]


def nearest_below(anchor, lines, label, max_dy):
    cands = [l for l in lines if l.n in label and abs(l.rect.x0 - anchor.rect.x0) < 3
             and 0 < l.rect.y0 - anchor.rect.y0 <= max_dy]
    return min(cands, key=lambda l: l.rect.y0) if cands else None


def fit(area, ratio, max_w=None, max_h=None):
    """Rectangle au ratio de l'image, centré dans area."""
    w, h = area.width, area.height
    if max_w:
        w = min(w, max_w)
    if max_h:
        h = min(h, max_h)
    if w / h > ratio:
        w = h * ratio
    else:
        h = w / ratio
    x0 = area.x0 + (area.width - w) / 2
    y0 = area.y0 + (area.height - h) / 2
    return pymupdf.Rect(x0, y0, x0 + w, y0 + h)


# --------------------------------------------------------------------------- #
# Détection des modèles
# --------------------------------------------------------------------------- #

def text_slot(x, baseline, size, existing=None, action="fill"):
    return {"x": round(x, 1), "baseline": round(baseline, 1), "size": round(size, 1),
            "existing": existing, "action": action}


def detect_visa_client(page, lines, grid, anchor, user_name):
    """Note de frais STIME (export Excel) : cadre « Visa Client » Nom / Date."""
    s = anchor.size
    nom = nearest_below(anchor, lines, ("nom",), 4 * s)
    date = nearest_below(anchor, lines, ("date",), 5 * s)
    if not nom or not date:
        return None
    x0, y0, x1, y1 = grid.cell(anchor.rect.x0 + 1, (date.rect.y0 + date.rect.y1) / 2)
    left = x0 if x0 is not None else anchor.rect.x0 - 2
    right = x1 if x1 is not None else anchor.rect.x0 + 25 * s
    top = y0 if y0 is not None else anchor.rect.y0 - 2
    bottom = y1 if y1 is not None and y1 > date.rect.y1 + 2 * s else date.rect.y1 + 9 * s
    box = pymupdf.Rect(left, top, right, bottom)

    name_vals = same_row(nom, lines, nom.rect.x1, box.x1)
    date_vals = same_row(date, lines, date.rect.x1, box.x1)
    name_txt = " ".join(l.text for l in name_vals) or None
    date_txt = " ".join(l.text for l in date_vals) or None
    if name_vals:
        value_x = name_vals[0].rect.x0
    elif date_vals:
        value_x = date_vals[0].rect.x0
    else:
        value_x = anchor.rect.x0 + 10.6 * s
    fs = max(s, 7)

    sig_area = pymupdf.Rect(box.x0 + 3, date.rect.y1 + 1, box.x1 - 3, box.y1 - 1.5)
    res = {
        "layout": "note-de-frais-visa-client",
        "box": box,
        "name": text_slot(value_x, nom.baseline, fs, name_txt, "keep" if name_txt else "fill"),
        "date": text_slot(value_x, date.baseline, fs, date_txt, "keep" if date_txt else "fill"),
        "signature_area": sig_area,
        "already_signed": has_content(page, sig_area, lines),
        "header_name": None,
    }

    presta = [l for l in lines if l.n == "visa prestataire"]
    if presta:
        p = min(presta, key=lambda l: abs(l.rect.y0 - anchor.rect.y0))
        p_date = nearest_below(p, lines, ("date",), 5 * p.size)
        if p_date:
            px0, _, px1, py1 = grid.cell(p.rect.x0 + 1, (p_date.rect.y0 + p_date.rect.y1) / 2)
            region = pymupdf.Rect(px0 if px0 is not None else p.rect.x0 - 2, p_date.rect.y1 + 1,
                                  px1 if px1 is not None else box.x0 - 5,
                                  py1 if py1 is not None else bottom)
            res["contractor_signature"] = has_content(page, region, lines)
    return res


def detect_hierarchique(page, lines, grid, anchor, user_name):
    """Compte rendu d'astreintes : cellule « Signature du responsable hiérarchique »."""
    s = anchor.size
    cx = (anchor.rect.x0 + anchor.rect.x1) / 2
    hx0, hy0, hx1, hy1 = grid.cell(cx, (anchor.rect.y0 + anchor.rect.y1) / 2)
    head_bottom = hy1 if hy1 is not None else anchor.rect.y1 + 4
    x0, y0, x1, y1 = grid.cell(cx, head_bottom + 3)
    cell = pymupdf.Rect(x0 if x0 is not None else anchor.rect.x0 - 5, head_bottom,
                        x1 if x1 is not None else anchor.rect.x1 + 5,
                        y1 if y1 is not None else head_bottom + 7 * s)

    inside = [l for l in lines if cell.contains(l.rect)]
    existing_name = next((l for l in inside if same_person(l.text, user_name)), None)
    fs = max(s, 9)
    pad = 4
    name_base = cell.y0 + pad + fs
    date_base = name_base + fs * 1.3
    sig_area = pymupdf.Rect(cell.x0 + pad, date_base + 3, cell.x1 - pad, cell.y1 - 2)

    res = {
        "layout": "astreinte-responsable-hierarchique",
        "box": cell,
        "name": text_slot(cell.x0 + pad, name_base, fs,
                          existing_name.text if existing_name else None,
                          "keep" if existing_name else "fill"),
        "date": text_slot(cell.x0 + pad, date_base, fs, None, "fill"),
        "signature_area": sig_area,
        "already_signed": has_content(page, cell, lines,
                                      ignore=[existing_name] if existing_name else ()),
        "header_name": None,
    }
    other_text = [l.text for l in inside if l is not existing_name]
    if other_text:
        res["cell_text"] = other_text

    collab = [l for l in lines if "signature du collaborateur" in l.n]
    if collab:
        c = collab[0]
        ccx = (c.rect.x0 + c.rect.x1) / 2
        _, _, _, chy1 = grid.cell(ccx, (c.rect.y0 + c.rect.y1) / 2)
        cb = chy1 if chy1 is not None else c.rect.y1 + 4
        cx0, _, cx1, cy1 = grid.cell(ccx, cb + 3)
        region = pymupdf.Rect(cx0 if cx0 is not None else c.rect.x0 - 5, cb + 1,
                              cx1 if cx1 is not None else c.rect.x1 + 5,
                              cy1 if cy1 is not None else cell.y1)
        res["contractor_signature"] = has_content(page, region, lines)
    return res


def detect_annexe(page, lines, grid, anchor, user_name):
    """Annexe au rapport d'activité STIME : « Signature et tampon Responsable Stime »."""
    s = anchor.size
    date = None
    cands = [l for l in lines if l.n.startswith("date") and abs(l.rect.x0 - anchor.rect.x0) < 3
             and 0 < anchor.rect.y0 - l.rect.y0 <= 8 * s]
    if cands:
        date = max(cands, key=lambda l: l.rect.y0)

    row = same_row(anchor, lines, anchor.rect.x1 + 1, page.rect.width)
    x0, y0, x1, y1 = grid.cell(anchor.rect.x0 + 1, anchor.rect.y1 + 3)
    col_right = min([l.rect.x0 for l in row] + [x1 if x1 is not None else page.rect.width]) - 4
    bottom = y1 if y1 is not None else anchor.rect.y1 + 20 * s
    fs = max(s, 9)

    date_txt = None
    date_x = anchor.rect.x0 + 20
    date_base = anchor.baseline - 3 * s
    if date:
        m = re.match(r"\s*date\s*:?\s*(.*)$", date.text, flags=re.I)
        tail = m.group(1).strip() if m else ""
        vals = same_row(date, lines, date.rect.x1, col_right)
        date_txt = tail or (" ".join(l.text for l in vals) or None)
        date_x = date.rect.x1 + 3
        date_base = date.baseline

    header = next((l for l in lines if l.n.startswith("responsable stime")), None)
    header_name = None
    if header:
        m = re.match(r"\s*responsable stime\s*:?\s*(.*)$", header.text, flags=re.I)
        header_name = (m.group(1).strip() if m else "") or None
        if not header_name:
            vals = same_row(header, lines, header.rect.x1, header.rect.x1 + 200)
            header_name = " ".join(l.text for l in vals) or None

    name_base = anchor.baseline + fs * 1.5
    has_name = bool(header_name)
    sig_top = (name_base if not has_name else anchor.rect.y1) + 3
    sig_area = pymupdf.Rect(anchor.rect.x0, sig_top, col_right, bottom - 2)
    res = {
        "layout": "annexe-rapport-activite",
        "box": pymupdf.Rect(x0 if x0 is not None else anchor.rect.x0 - 2,
                            y0 if y0 is not None else (date.rect.y0 - 4 if date else anchor.rect.y0 - 4),
                            col_right, bottom),
        "name": text_slot(anchor.rect.x0, name_base, fs, header_name,
                          "keep" if has_name else "fill"),
        "date": text_slot(date_x, date_base, fs, date_txt, "keep" if date_txt else "fill"),
        "signature_area": sig_area,
        "signature_max": (140, 72),
        "already_signed": has_content(page, sig_area, lines),
        "header_name": header_name,
    }

    presta = [l for l in row if l.n.startswith("signature prestataire")]
    if presta:
        p = presta[0]
        nxt = [l.rect.x0 for l in row if l.rect.x0 > p.rect.x1 + 1 and not l.n.startswith("et/ou")]
        region = pymupdf.Rect(p.rect.x0, p.rect.y1 + 1, min(nxt) - 4 if nxt else page.rect.width,
                              bottom - 1)
        res["contractor_signature"] = has_content(page, region, lines)
    return res


DETECTORS = [
    (lambda n: n == "visa client", detect_visa_client),
    (lambda n: "signature du responsable hierarchique" in n, detect_hierarchique),
    (lambda n: n.startswith("signature et tampon responsable"), detect_annexe),
]


def analyze_doc(doc, user_name):
    marked = MARKER in (doc.metadata or {}).get("keywords", "")
    for pno in range(len(doc)):
        page = doc[pno]
        lines = page_lines(page)
        grid = None
        for match, detector in DETECTORS:
            for anchor in (l for l in lines if match(l.n)):
                grid = grid or Grid(page)
                res = detector(page, lines, grid, anchor, user_name)
                if res:
                    res["page"] = pno + 1
                    res["page_rotation"] = page.rotation
                    res["already_signed"] = res["already_signed"] or marked
                    return res
    return {"layout": None, "already_signed": marked,
            "text_layer": any(doc[p].get_text().strip() for p in range(len(doc)))}


def report(path, res, user_name):
    out = {"file": str(path), "layout": res.get("layout"),
           "filename_altered": looks_uploaded(path)}
    if not res.get("layout"):
        out["text_layer"] = res.get("text_layer")
        out["status"] = "unknown-layout"
        out["already_signed"] = res.get("already_signed", False)
        return out
    out["page"] = res["page"]
    out["already_signed"] = res["already_signed"]
    out["contractor_signature"] = res.get("contractor_signature")
    out["name"] = {"existing": res["name"]["existing"], "action": res["name"]["action"]}
    out["date"] = {"existing": res["date"]["existing"], "action": res["date"]["action"]}
    shown = res["name"]["existing"] or res.get("header_name")
    out["name_matches"] = same_person(shown, user_name) if shown else None
    if res.get("cell_text"):
        out["cell_text"] = res["cell_text"]
    out["page_rotation"] = res["page_rotation"]
    out["signature_area"] = [round(v, 1) for v in res["signature_area"]]
    warnings = []
    if res["page_rotation"]:
        warnings.append("page pivotée : vérifier visuellement le rendu")
    if out["contractor_signature"] is False:
        warnings.append("signature du prestataire non détectée")
    if out["name_matches"] is False:
        warnings.append(f"nom pré-rempli différent : « {shown} »")
    if out["already_signed"]:
        warnings.append("zone de visa déjà occupée (document probablement déjà signé)")
    out["warnings"] = warnings
    return out


# --------------------------------------------------------------------------- #
# Signature
# --------------------------------------------------------------------------- #

# Préfixe ajouté par Claude aux fichiers déposés dans la conversation
# (« dd51ede5-Astreinte_M_BOUROGAA_10-26.pdf »), espaces remplacés par « _ ».
UPLOAD_PREFIX = re.compile(r"^[0-9a-f]{8}-", re.I)


def looks_uploaded(path: Path) -> bool:
    return bool(UPLOAD_PREFIX.match(path.name))


def output_path(src: Path, out_dir, original_name=None):
    target = Path(out_dir).expanduser() if out_dir else src.parent
    if original_name:
        stem = re.split(r"[\\/]", original_name.strip())[-1]
        stem = re.sub(r"\.pdf$", "", stem, flags=re.I).strip()
        if not stem:
            raise ValueError(f"Nom d'origine invalide : {original_name!r}")
    else:
        stem = src.stem
    return target / f"{stem}{SIGNED_SUFFIX}.pdf"


def name_key(name: str, drop_accented=False) -> str:
    """Nom réduit à ses lettres et chiffres, pour comparer un nom d'origine au
    nom renommé par l'upload (préfixe retiré, espaces devenus « _ »)."""
    name = UPLOAD_PREFIX.sub("", re.split(r"[\\/]", name)[-1])
    name = re.sub(r"\.pdf$", "", name, flags=re.I)
    if drop_accented:
        name = "".join(c for c in name if c.isascii())
    return re.sub(r"[^a-z0-9]", "", norm(name))


def matches_upload(path: Path, original: str) -> bool:
    key = name_key(path.name)
    return key in (name_key(original), name_key(original, drop_accented=True))


def original_names(args):
    names = args.original_name or []
    pdfs = args.pdf if isinstance(args.pdf, list) else [args.pdf]
    if names and len(names) != len(pdfs):
        raise SystemExit(fail(f"--original-name : {len(names)} nom(s) pour {len(pdfs)} PDF ; "
                              "en donner un par PDF, dans le même ordre"))
    return names or [None] * len(pdfs)


def image_ratio(sig_path):
    pix = pymupdf.Pixmap(sig_path)
    return pix.width / pix.height


def stamp(doc, page, name_slot, date_slot, sig_rect, cfg, date_str):
    if name_slot and name_slot["action"] == "fill":
        page.insert_text((name_slot["x"], name_slot["baseline"]), cfg["full_name"],
                         fontsize=name_slot["size"], fontname="helv", color=(0, 0, 0))
    if date_slot and date_slot["action"] == "fill":
        page.insert_text((date_slot["x"], date_slot["baseline"]), date_str,
                         fontsize=date_slot["size"], fontname="helv", color=(0, 0, 0))
    page.insert_image(sig_rect, filename=cfg["signature"], keep_proportion=True, overlay=True)
    meta = dict(doc.metadata or {})
    kw = meta.get("keywords") or ""
    meta["keywords"] = f"{kw}; {MARKER}" if kw else MARKER
    doc.set_metadata(meta)


def save(doc, dst: Path, force: bool):
    if dst.exists() and not force:
        raise FileExistsError(f"{dst} existe déjà (utiliser --force pour l'écraser)")
    dst.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(dst), garbage=3, deflate=True)


def require_config():
    st = config_status()
    if not st["configured"]:
        print(json.dumps({"error": "not-configured", **st}, ensure_ascii=False, indent=2))
        sys.exit(EXIT_NO_CONFIG)
    return load_config()


def parse_date(value):
    if not value:
        return dt.date.today().strftime("%d/%m/%Y")
    try:
        return dt.datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        raise SystemExit(fail(f"Date invalide : {value} (format attendu JJ/MM/AAAA)"))


def cmd_analyze(args) -> int:
    cfg = load_config()
    results = []
    for f in args.pdf:
        path = Path(f).expanduser()
        try:
            with pymupdf.open(str(path)) as doc:
                results.append(report(path, analyze_doc(doc, cfg.get("full_name")),
                                      cfg.get("full_name")))
        except Exception as exc:  # noqa: BLE001
            results.append({"file": str(path), "status": "error", "error": str(exc)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_sign(args) -> int:
    cfg = require_config()
    date_str = parse_date(args.date)
    ratio = image_ratio(cfg["signature"])
    results, partial = [], False
    for f, original in zip(args.pdf, original_names(args)):
        path = Path(f).expanduser()
        try:
            with pymupdf.open(str(path)) as doc:
                res = analyze_doc(doc, cfg["full_name"])
                rep = report(path, res, cfg["full_name"])
                if looks_uploaded(path) and not original:
                    rep["status"] = "skipped-original-name-required"
                elif original and not args.skip_name_check and not matches_upload(path, original):
                    rep["status"] = "skipped-original-name-mismatch"
                    rep["original_name"] = original
                elif not res.get("layout"):
                    rep["status"] = "skipped-unknown-layout"
                elif res["already_signed"] and not args.resign:
                    rep["status"] = "skipped-already-signed"
                elif rep["name_matches"] is False and not args.allow_name_mismatch:
                    rep["status"] = "skipped-name-mismatch"
                else:
                    page = doc[res["page"] - 1]
                    mw, mh = res.get("signature_max", (None, None))
                    sig_rect = fit(res["signature_area"], ratio, mw, mh)
                    date_slot = res["date"]
                    stamp(doc, page, res["name"], date_slot, sig_rect, cfg, date_str)
                    dst = output_path(path, args.out_dir, original)
                    save(doc, dst, args.force)
                    rep["status"] = "signed"
                    rep["output"] = str(dst)
                    rep["date_written"] = date_str if date_slot["action"] == "fill" else None
                    rep["name_written"] = res["name"]["action"] == "fill"
                    rep["signature_rect"] = [round(v, 1) for v in sig_rect]
        except Exception as exc:  # noqa: BLE001
            rep = {"file": str(path), "status": "error", "error": str(exc)}
        partial |= rep.get("status") != "signed"
        results.append(rep)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return EXIT_PARTIAL if partial else EXIT_OK


def cmd_preview(args) -> int:
    path = Path(args.pdf).expanduser()
    with pymupdf.open(str(path)) as doc:
        page = doc[args.page - 1]
        if args.grid:
            shape = page.new_shape()
            step = args.grid
            w, h = page.rect.width, page.rect.height
            for x in range(0, int(w) + 1, step):
                shape.draw_line((x, 0), (x, h))
            for y in range(0, int(h) + 1, step):
                shape.draw_line((0, y), (w, y))
            shape.finish(color=(1, 0, 0), width=0.3, stroke_opacity=0.4)
            shape.commit()
            for x in range(0, int(w) + 1, step * 2):
                page.insert_text((x + 1, 7), str(x), fontsize=6, color=(1, 0, 0))
            for y in range(step * 2, int(h) + 1, step * 2):
                page.insert_text((1, y - 1), str(y), fontsize=6, color=(1, 0, 0))
        out = Path(args.out).expanduser() if args.out else path.with_suffix(f".page{args.page}.png")
        page.get_pixmap(dpi=args.dpi).save(str(out))
        print(json.dumps({"preview": str(out), "page": args.page,
                          "page_size": [round(page.rect.width, 1), round(page.rect.height, 1)],
                          "pages": len(doc)}, ensure_ascii=False, indent=2))
    return EXIT_OK


def parse_floats(value, n, label):
    try:
        vals = [float(v) for v in value.split(",")]
    except ValueError:
        vals = []
    if len(vals) != n:
        raise SystemExit(fail(f"{label} attend {n} nombres séparés par des virgules"))
    return vals


def cmd_sign_manual(args) -> int:
    cfg = require_config()
    date_str = parse_date(args.date)
    path = Path(args.pdf).expanduser()
    area = pymupdf.Rect(*parse_floats(args.rect, 4, "--rect"))
    ratio = image_ratio(cfg["signature"])
    original = original_names(args)[0]
    if looks_uploaded(path) and not original:
        print(json.dumps({"file": str(path), "status": "skipped-original-name-required"},
                         ensure_ascii=False, indent=2))
        return EXIT_PARTIAL
    if original and not args.skip_name_check and not matches_upload(path, original):
        print(json.dumps({"file": str(path), "original_name": original,
                          "status": "skipped-original-name-mismatch"}, ensure_ascii=False, indent=2))
        return EXIT_PARTIAL
    with pymupdf.open(str(path)) as doc:
        page = doc[args.page - 1]
        name_slot = date_slot = None
        if args.name_at:
            x, y = parse_floats(args.name_at, 2, "--name-at")
            name_slot = text_slot(x, y, args.font_size)
        if args.date_at:
            x, y = parse_floats(args.date_at, 2, "--date-at")
            date_slot = text_slot(x, y, args.font_size)
        sig_rect = fit(area, ratio)
        stamp(doc, page, name_slot, date_slot, sig_rect, cfg, date_str)
        dst = output_path(path, args.out_dir, original)
        save(doc, dst, args.force)
    print(json.dumps({"file": str(path), "status": "signed", "output": str(dst),
                      "signature_rect": [round(v, 1) for v in sig_rect],
                      "name_written": bool(name_slot), "date_written": date_str if date_slot else None},
                     ensure_ascii=False, indent=2))
    return EXIT_OK


def fail(msg) -> int:
    print(json.dumps({"error": msg}, ensure_ascii=False))
    return EXIT_PARTIAL


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="sign_reports.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("config", help="afficher ou enregistrer la configuration")
    c.add_argument("action", choices=["show", "set", "bundle"])
    c.add_argument("--name", help="Prénom NOM tel qu'il doit apparaître sur les documents")
    c.add_argument("--signature", help="chemin du PNG de signature (copié dans la config)")
    c.add_argument("--out", help="bundle : dossier ou fichier .zip de sortie (défaut : dossier courant)")
    c.add_argument("--force", action="store_true", help="bundle : écraser un zip existant")
    c.set_defaults(func=cmd_config)

    a = sub.add_parser("analyze", help="détecter le modèle et la zone de visa")
    a.add_argument("pdf", nargs="+")
    a.set_defaults(func=cmd_analyze)

    s = sub.add_parser("sign", help="signer les PDF reconnus")
    s.add_argument("pdf", nargs="+")
    s.add_argument("--date", help="JJ/MM/AAAA (défaut : aujourd'hui)")
    s.add_argument("--out-dir", help="dossier de sortie (défaut : celui du PDF source)")
    s.add_argument("--skip-name-check", action="store_true",
                   help="ne pas vérifier que --original-name correspond au fichier")
    s.add_argument("--original-name", action="append", help="nom d'origine du PDF, tel que vu par l'utilisateur (un par PDF, même ordre) ; "
                        "obligatoire pour un fichier renommé par l'upload")
    s.add_argument("--force", action="store_true", help="écraser un fichier signé existant")
    s.add_argument("--resign", action="store_true", help="signer même si la zone est déjà occupée")
    s.add_argument("--allow-name-mismatch", action="store_true",
                   help="signer même si le nom pré-rempli n'est pas celui de la configuration")
    s.set_defaults(func=cmd_sign)

    p = sub.add_parser("preview", help="rendre une page en PNG, avec grille en points")
    p.add_argument("pdf")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--out")
    p.add_argument("--dpi", type=int, default=110)
    p.add_argument("--grid", type=int, default=50, help="pas de la grille en points (0 = sans)")
    p.set_defaults(func=cmd_preview)

    m = sub.add_parser("sign-manual", help="signer à un emplacement donné (en points PDF)")
    m.add_argument("pdf")
    m.add_argument("--page", type=int, default=1)
    m.add_argument("--rect", required=True, help="zone de la signature : x0,y0,x1,y1")
    m.add_argument("--name-at", help="position du nom : x,ligne_de_base")
    m.add_argument("--date-at", help="position de la date : x,ligne_de_base")
    m.add_argument("--font-size", type=float, default=10)
    m.add_argument("--date", help="JJ/MM/AAAA (défaut : aujourd'hui)")
    m.add_argument("--out-dir")
    m.add_argument("--skip-name-check", action="store_true",
                   help="ne pas vérifier que --original-name correspond au fichier")
    m.add_argument("--original-name", action="append", help="nom d'origine du PDF, tel que vu par l'utilisateur (un par PDF, même ordre) ; "
                        "obligatoire pour un fichier renommé par l'upload")
    m.add_argument("--force", action="store_true")
    m.set_defaults(func=cmd_sign_manual)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
