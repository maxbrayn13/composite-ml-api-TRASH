# 🔬 Composite Materials Property Prediction API

Advanced machine learning-inspired API for predicting mechanical properties of fiber-reinforced composite materials.

## ✨ Features

- **25 Material Combinations**: 5 fiber types × 5 matrix types
- **7 Mechanical Properties**: Tensile, compressive, flexural, ILSS, impact
- **7 Layup Configurations**: From unidirectional to quasi-isotropic
- **7 Manufacturing Processes**: Autoclave, VARTM, RTM, and more
- **Beautiful Web Interface**: Interactive material configurator
- **REST API**: Full JSON API for programmatic access
- **Fast Response**: <10ms prediction time
- **Production Ready**: Deployed on Railway.com

## 🚀 Live Demo

**Website**: https://composite-ml-api-production.up.railway.app
**API**: https://composite-ml-api-production.up.railway.app/api

## 📊 Predicted Properties

1. **Tensile Strength** (MPa)
2. **Tensile Modulus** (GPa)
3. **Compressive Strength** (MPa)
4. **Flexural Strength** (MPa)
5. **Flexural Modulus** (GPa)
6. **ILSS** - Interlaminar Shear Strength (MPa)
7. **Impact Energy** (J)

## 🛠️ Technology Stack

- **Backend**: Flask 3.0
- **Server**: Gunicorn
- **Method**: Empirical formulas + Rule of mixtures
- **Deployment**: Railway.com
- **Frontend**: Vanilla JavaScript + Modern CSS

## 📖 API Documentation

### Endpoints

#### `GET /api`
Returns API information and documentation

#### `POST /api/predict`
Single material property prediction

**Request:**
```json
{
  "fiber_type": "Carbon",
  "matrix_type": "Epoxy",
  "fiber_volume_fraction": 0.6,
  "layup": "UD 0°",
  "manufacturing": "Autoclave"
}
```

**Response:**
```json
{
  "success": true,
  "predictions": {
    "tensile_strength_MPa": 1500.0,
    "tensile_modulus_GPa": 130.0,
    "compressive_strength_MPa": 1200.0,
    "flexural_strength_MPa": 1400.0,
    "flexural_modulus_GPa": 125.0,
    "ILSS_MPa": 75.0,
    "impact_energy_J": 18.0
  }
}
```

#### `POST /api/predict/batch`
Batch predictions for multiple materials

#### `GET /api/materials`
Get complete material database

#### `GET /api/options`
Get all available material options

#### `GET /api/health`
Health check endpoint

## 🔬 Methodology

The prediction system uses:

1. **Literature-based Database**: 25 material combinations with properties from peer-reviewed sources
2. **Rule of Mixtures**: Classical composite mechanics for fiber volume fraction effects
3. **Correction Factors**: Empirical adjustments for layup and manufacturing processes

**Formula:**
```
Property = Base_Value × VF_Factor × Layup_Factor × Manufacturing_Factor
```

Where:
- `VF_Factor` = fiber_volume_fraction / 0.6 (normalized)
- `Layup_Factor` = 0.4 to 1.0 (based on configuration)
- `Manufacturing_Factor` = 0.85 to 1.0 (based on process quality)

## 📦 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/maxbrayn13/composite-ml-api.git
cd composite-ml-api

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Visit: http://localhost:8080

### Deploy to Railway

1. Push code to GitHub
2. Connect repository to Railway.com
3. Railway auto-detects and deploys
4. Live in 3-5 minutes!

## 🧪 Usage Examples

### Python

```python
import requests

url = "https://composite-ml-api-production.up.railway.app/api/predict"
data = {
    "fiber_type": "Carbon",
    "matrix_type": "Epoxy",
    "fiber_volume_fraction": 0.6,
    "layup": "UD 0°",
    "manufacturing": "Autoclave"
}

response = requests.post(url, json=data)
print(response.json()['predictions'])
```

### JavaScript

```javascript
fetch('https://composite-ml-api-production.up.railway.app/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        fiber_type: 'Carbon',
        matrix_type: 'Epoxy',
        fiber_volume_fraction: 0.6,
        layup: 'UD 0°',
        manufacturing: 'Autoclave'
    })
})
.then(r => r.json())
.then(data => console.log(data.predictions));
```

### cURL

```bash
curl -X POST https://composite-ml-api-production.up.railway.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fiber_type": "Carbon",
    "matrix_type": "Epoxy",
    "fiber_volume_fraction": 0.6,
    "layup": "UD 0°",
    "manufacturing": "Autoclave"
  }'
```

## 📚 Material Options

### Fiber Types
- Carbon
- Glass (E-Glass)
- Aramid (Kevlar)
- Basalt
- Natural Fiber

### Matrix Types
- Epoxy
- Polyester
- Vinyl Ester
- PEEK
- Polyamide 6 (PA6)

### Layup Configurations
- UD 0° (Unidirectional)
- UD 90°
- Woven
- [0/90]2s
- [0/45/90/-45]s
- [±45]2s
- Quasi-isotropic

### Manufacturing Processes
- Autoclave (highest quality)
- VARTM
- RTM
- Pultrusion
- Filament Winding
- Compression Molding
- Hand Layup

## 🎓 Academic Use

This API was developed for PhD research in composite materials engineering.

### Citation

```bibtex
@software{composite_ml_api_2025,
  title={Composite Materials Property Prediction API},
  author={Your Name},
  year={2025},
  url={https://github.com/maxbrayn13/composite-ml-api},
  note={Web service for predicting mechanical properties of fiber-reinforced composites}
}
```

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or collaborations, please open an issue on GitHub.

## 🔗 Links

- **Live API**: https://composite-ml-api-production.up.railway.app
- **GitHub**: https://github.com/maxbrayn13/composite-ml-api
- **Documentation**: https://composite-ml-api-production.up.railway.app/api

---

Made with ❤️ for composite materials research
