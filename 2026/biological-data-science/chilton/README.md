# Build better skills. Build better workflows. Keep the receipts.

John Chilton, Marius van den Beek, Dannon Baker, Danielle Callan, Scott Cain, Anton Nekrutenko. CSHL Biological Data Science, November 4–7, 2026.

The Galaxy Workflow Foundry: a wiki of typed notes compiled into agent skills, with programs (gxwf, Planemo), not the model, checking each step. The receipts on the poster come from one Foundry run that turned the DengueSeq paper into a tested Galaxy workflow.

`poster.typ` is the source (Typst), 44 × 44 in.

## Files

| Path | What it is |
| - | - |
| `poster.typ` | Poster layout and text |
| `receipts.json` | Receipt contents (CAST, PINNED, VALIDATED, TESTED), extracted from the run |
| `route.json` | The route diagram's phases |
| `assets/` | White Galaxy logo, QR codes (`qr.json` lists their targets) |
| `fonts/` | Atkinson Hyperlegible Next and Mono, Kalam, IBM Plex Sans and Mono; all SIL OFL 1.1, licences alongside |
| `poster.pdf`, `poster.svg` | Built from `poster.typ`; the SVG has text as outlined glyphs |
| `render.py`, `build.sh` | Rebuild the PDF and SVG |

## Rebuild

```bash
./build.sh
```

This runs `uvx --from typst==0.15.0 python render.py`, using only the fonts in `fonts/`. Layout guards in `poster.typ` stop the build if a box overflows; pass the Typst input `noguard=1` to see them as red text on the page instead.

## QR codes

- The Foundry: https://galaxyproject.github.io/foundry/
- Preprint [1]: https://doi.org/10.64898/2026.10.26.761864
