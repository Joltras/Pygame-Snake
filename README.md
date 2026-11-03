# Pygame Snake

Ein Snake-Spiel, geschrieben in Python mit [pygame](https://www.pygame.org/).

## Installation

Benötigt Python 3.9 oder neuer.

```bash
pip install -r requirements.txt
```

## Starten

Aus dem Hauptordner des Repos:

```bash
python -m src.main
```

## Steuerung

| Taste | Aktion |
|---|---|
| Pfeiltasten | Schlange steuern |
| Leertaste | Spiel starten / fortsetzen |
| Esc | Pause |
| Y / N | Nach Game Over: neu starten / beenden |

## Tests

```bash
python -m unittest test.Test_Snake
```
