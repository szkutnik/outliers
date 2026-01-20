# Outliers

Outliers provides a small, focused API for detecting outliers using the robust
modified z-score technique.

## Installation

```bash
pip install outliers
```

## Usage

```python
from outliers import detect_outliers, modified_z_scores

values = [10, 12, 12, 13, 12, 11, 12, 100]
print(modified_z_scores(values))
print(detect_outliers(values))
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```
