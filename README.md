# Flight Software Architecture

An on-board computer flight software architecture: a hard real-time, single-core
FreeRTOS baseline with a cFE-style core framework, a layered driver-independent
design, and a boot and over-the-air update path treated as part of the
architecture rather than bolted on afterwards.

**[Read it online](https://dgonzalez97.github.io/flight-software-architecture/)**
· **[Download the PDF](Flight_Software_Architecture.pdf)**

The chapters under [docs/](docs/) are the source. The two documents above are
built from them, so an edit goes in the Markdown and the build regenerates both.

## Contents

| | Chapter |
| --- | --- |
| 1 | [Design Philosophy and Assumptions](docs/01-design-philosophy-and-assumptions/) |
| 2 | [Architectural Approach](docs/02-architectural-approach/) |
| 3 | [Software Components](docs/03-software-components/) |
| 4 | [Scheduling and Real-Time Behaviour](docs/04-scheduling-and-real-time-behaviour.md) |
| 5 | [Communication Architecture](docs/05-communication-architecture/) |
| 6 | [Fault Containment and Recovery](docs/06-fault-containment-and-recovery.md) |

Each chapter directory holds one file per subsection, and its `README.md` is the
chapter introduction.

## Building the documents

```bash
./build/build.sh
```

It concatenates the chapters in the order [build/order.txt](build/order.txt)
lists, renders every mermaid diagram to SVG, writes `index.html` with its
resources embedded, and prints `Flight_Software_Architecture.pdf` from that same
HTML, so the two outputs cannot drift apart.

Requirements: `pandoc`, `node` with `npx`, and a Chromium or Chrome binary. If
none is on the path the script falls back to the copy
[mermaid-cli](https://github.com/mermaid-js/mermaid-cli) downloads, or you can
point `CHROME` at your own.

Rendered diagrams are cached in `build/.cache`, so a rebuild that changes no
diagram needs no network.

## Adding or changing a chapter

1. Edit the Markdown under `docs/`, or add a file.
2. If you added one, list it in `build/order.txt` at the position it belongs.
3. Run `./build/build.sh` and commit the regenerated `index.html` and PDF.

Diagrams are written as ` ```mermaid ` fences. GitHub renders them in the
Markdown, and the build renders the same source to SVG for the HTML and the PDF.
