# Dataset Notes — P_227

- Dataset: AI4I 2020 Predictive Maintenance Dataset (UCI Machine Learning Repository)
- Local file: `data/raw/ai4i2020.csv`
- Records: 10,000
- Target: `Machine failure`
- Class counts: 9,661 non-failure and 339 failure (3.39% failure class)

## Model inputs

- `Type` (categorical)
- `Air temperature [K]`
- `Process temperature [K]`
- `Rotational speed [rpm]`
- `Torque [Nm]`
- `Tool wear [min]`

`UDI` and `Product ID` are identifiers and are not model inputs. Failure-mode indicator columns (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`) are excluded from model inputs to avoid target leakage.

## Important limitation

The AI4I dataset is synthetic. Results on this dataset do not establish performance on real factory equipment. Validate with representative industrial data and confirmed maintenance outcomes before operational use.

Source: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
