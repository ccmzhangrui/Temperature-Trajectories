import os

HISTORY_FOLDER = "history"
DOCS_FOLDER = "docs"
GALLERY_FILE = os.path.join(DOCS_FOLDER, "gallery.html")


def build_gallery():
    os.makedirs(DOCS_FOLDER, exist_ok=True)
    entries = {}
    for file in sorted(os.listdir(HISTORY_FOLDER)):
        if file.endswith(".png") or file.endswith(".csv"):
            date = file.split("_")[0]
            entries.setdefault(date, []).append(file)

    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>Phenotype History Gallery</title>",
        "<style>body{font-family:Arial;background:#f4f4f4;padding:20px}.controls{textalign:center;margin-bottom:20px}button{padding:8px 12px;margin:0 5px; cursor: pointer; border: none; background:  # 0055aa;color:white}.entry{display:inlineblock;margin:10px;padding:5px;background:#fff;border:1px solid #ccc}.hidden{display:none} img {max - width: 300px} </style> ",
        "</head>",
        "<body>",
        "<h1>Phenotype Analysis History</h1>",
        "<div class='controls'>",
        "<button onclick=\"filterType('all')\">Show All</button>",
        "<button onclick=\"filterType('gmm')\">GMM Only</button>",
        "<button onclick=\"filterType('pam')\">PAM Only</button>",
        "</div>",
        "<script>function filterType(t) {document.querySelectorAll('.entry').forEach(e= > { if (t ==='all') {e.classList.remove('hidden');}  else {e.classList.add('hidden'); if (e.dataset.type ===t)e.classList.remove('hidden');}});} </script>"
    ]

    for date, files in sorted(entries.items(), reverse=True):
        html.append(f"<h2>{date}</h2>")

        for f in sorted(files):
            path = f"../{HISTORY_FOLDER}/{f}"
            ftype = "gmm" if "gmm" in f.lower() else "pam"
            if f.endswith(".png"):
                html.append(f"<div class='entry' data-type='{ftype}'><img src='{path}' alt = '{f}' > < p > {f} </p> < div>")
            elif f.endswith(".csv"):
                html.append(f"<div class='entry' data-type='{ftype}'><a href='{path}' target = '_blank' > Download {f} </a> </div>")


    html.extend(["</body>", "</html>"])
    with open(GALLERY_FILE, "w") as f:
        f.write("\n".join(html))


if __name__ == "__main__":
    build_gallery()
