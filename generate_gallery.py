import os

HISTORY_FOLDER = "history"
DOCS_FOLDER = "docs"
GALLERY_FILE = os.path.join(DOCS_FOLDER, "gallery.html")


def build_gallery() -> None:
    os.makedirs(DOCS_FOLDER, exist_ok=True)
    os.makedirs(HISTORY_FOLDER, exist_ok=True)

    entries = {}
    for file in sorted(os.listdir(HISTORY_FOLDER)):
        low = file.lower()
        if low.endswith(".png") or low.endswith(".csv"):
            date = file.split("_")[0]
            entries.setdefault(date, []).append(file)

    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<title>Phenotype History Gallery</title>",
        "<style>",
        "body{font-family:Arial;background:#f4f4f4;padding:20px}",
        ".controls{text-align:center;margin-bottom:20px}",
        "button{padding:8px 12px;margin:0 5px;cursor:pointer;border:none;background:#0055aa;color:white}",
        ".entry{display:inline-block;margin:10px;padding:5px;background:#fff;border:1px solid #ccc;vertical-align:top}",
        ".hidden{display:none}",
        "img{max-width:300px;display:block}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Phenotype Analysis History</h1>",
        '<div class="controls">',
        '<button onclick="filterType(\'all\')">Show All</button>',
        '<button onclick="filterType(\'gmm\')">GMM Only</button>',
        '<button onclick="filterType(\'pam\')">PAM Only</button>',
        "</div>",
        "<script>",
        "function filterType(t){",
        "  document.querySelectorAll('.entry').forEach(function(e){",
        "    if(t==='all'){ e.classList.remove('hidden'); return; }",
        "    e.classList.add('hidden');",
        "    if(e.dataset.type===t){ e.classList.remove('hidden'); }",
        "  });",
        "}",
        "</script>",
    ]

    for date, files in sorted(entries.items(), reverse=True):
        html.append(f"<h2>{date}</h2>")
        for f in sorted(files):
            low = f.lower()
            ftype = "gmm" if "gmm" in low else ("pam" if "pam" in low else "other")
            path = f"../{HISTORY_FOLDER}/{f}"

            if low.endswith(".png"):
                html.append(
                    f'<div class="entry" data-type="{ftype}">'
                    f'<img src="{path}" alt="{f}"/>'
                    f"<p>{f}</p>"
                    f"</div>"
                )
            elif low.endswith(".csv"):
                html.append(
                    f'<div class="entry" data-type="{ftype}">'
                    f'<a href="{path}" target="_blank">Download {f}</a>'
                    f"</div>"
                )

    html.extend(["</body>", "</html>"])

    with open(GALLERY_FILE, "w", encoding="utf-8") as fp:
        fp.write("\n".join(html))


if __name__ == "__main__":
    build_gallery()
