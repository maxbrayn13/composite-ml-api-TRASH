"""
Composite Materials Property Prediction API
Version: 2.0 - Production Ready for Railway.com
Method: Empirical formulas based on composite mechanics
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

PORT = int(os.environ.get('PORT', 8080))

print("="*80, file=sys.stderr)
print(f"🚀 Composite ML API v2.0 - Starting on PORT {PORT}", file=sys.stderr)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)
print("="*80, file=sys.stderr)

# Comprehensive material properties database (from literature)
MATERIALS_DB = {
    'Carbon': {
        'Epoxy': {'ts': 1500, 'tm': 130, 'cs': 1200, 'fs': 1400, 'fm': 125, 'ilss': 75, 'ie': 18},
        'Polyester': {'ts': 1200, 'tm': 110, 'cs': 950, 'fs': 1150, 'fm': 105, 'ilss': 62, 'ie': 15},
        'Vinyl_ester': {'ts': 1350, 'tm': 120, 'cs': 1050, 'fs': 1250, 'fm': 115, 'ilss': 68, 'ie': 16},
        'PEEK': {'ts': 1800, 'tm': 145, 'cs': 1400, 'fs': 1650, 'fm': 138, 'ilss': 88, 'ie': 25},
        'PA6': {'ts': 1400, 'tm': 125, 'cs': 1100, 'fs': 1300, 'fm': 120, 'ilss': 70, 'ie': 20}
    },
    'Glass': {
        'Epoxy': {'ts': 420, 'tm': 26, 'cs': 280, 'fs': 550, 'fm': 24, 'ilss': 40, 'ie': 27},
        'Polyester': {'ts': 350, 'tm': 22, 'cs': 230, 'fs': 450, 'fm': 20, 'ilss': 32, 'ie': 22},
        'Vinyl_ester': {'ts': 385, 'tm': 24, 'cs': 255, 'fs': 500, 'fm': 22, 'ilss': 36, 'ie': 24},
        'PEEK': {'ts': 480, 'tm': 30, 'cs': 320, 'fs': 620, 'fm': 28, 'ilss': 46, 'ie': 32},
        'PA6': {'ts': 400, 'tm': 25, 'cs': 270, 'fs': 520, 'fm': 23, 'ilss': 38, 'ie': 26}
    },
    'Aramid': {
        'Epoxy': {'ts': 560, 'tm': 32, 'cs': 180, 'fs': 480, 'fm': 28, 'ilss': 35, 'ie': 42},
        'Polyester': {'ts': 480, 'tm': 28, 'cs': 150, 'fs': 410, 'fm': 24, 'ilss': 28, 'ie': 35},
        'Vinyl_ester': {'ts': 520, 'tm': 30, 'cs': 165, 'fs': 445, 'fm': 26, 'ilss': 31, 'ie': 38},
        'PEEK': {'ts': 620, 'tm': 36, 'cs': 200, 'fs': 530, 'fm': 32, 'ilss': 40, 'ie': 48},
        'PA6': {'ts': 540, 'tm': 31, 'cs': 175, 'fs': 460, 'fm': 27, 'ilss': 33, 'ie': 40}
    },
    'Basalt': {
        'Epoxy': {'ts': 380, 'tm': 24, 'cs': 250, 'fs': 490, 'fm': 22, 'ilss': 38, 'ie': 24},
        'Polyester': {'ts': 320, 'tm': 20, 'cs': 210, 'fs': 410, 'fm': 18, 'ilss': 30, 'ie': 20},
        'Vinyl_ester': {'ts': 350, 'tm': 22, 'cs': 230, 'fs': 450, 'fm': 20, 'ilss': 34, 'ie': 22},
        'PEEK': {'ts': 430, 'tm': 27, 'cs': 280, 'fs': 550, 'fm': 25, 'ilss': 43, 'ie': 28},
        'PA6': {'ts': 365, 'tm': 23, 'cs': 240, 'fs': 470, 'fm': 21, 'ilss': 36, 'ie': 23}
    },
    'Natural': {
        'Epoxy': {'ts': 55, 'tm': 2.5, 'cs': 45, 'fs': 85, 'fm': 3.5, 'ilss': 12, 'ie': 10},
        'Polyester': {'ts': 45, 'tm': 2.0, 'cs': 38, 'fs': 70, 'fm': 2.8, 'ilss': 9, 'ie': 8},
        'Vinyl_ester': {'ts': 50, 'tm': 2.2, 'cs': 41, 'fs': 77, 'fm': 3.1, 'ilss': 10, 'ie': 9},
        'PEEK': {'ts': 65, 'tm': 3.0, 'cs': 52, 'fs': 95, 'fm': 4.0, 'ilss': 14, 'ie': 12},
        'PA6': {'ts': 52, 'tm': 2.4, 'cs': 43, 'fs': 80, 'fm': 3.3, 'ilss': 11, 'ie': 9}
    }
}

# Layup configuration factors
LAYUP_FACTORS = {
    'UD 0°': 1.0,
    'UD 90°': 0.4,
    'Woven': 0.8,
    '[0/90]2s': 0.85,
    '[0/45/90/-45]s': 0.75,
    '[±45]2s': 0.65,
    'Quasi-isotropic': 0.7
}

# Manufacturing process factors
MANUFACTURING_FACTORS = {
    'Autoclave': 1.0,
    'VARTM': 0.95,
    'Hand_layup': 0.85,
    'Pultrusion': 0.98,
    'RTM': 0.97,
    'Compression_molding': 0.93,
    'Filament_winding': 0.96
}


def predict_properties(fiber_type, matrix_type, fiber_vf, layup, manufacturing):
    """
    Predict composite properties using empirical formulas and rule of mixtures
    
    Parameters:
    - fiber_type: Type of reinforcement fiber
    - matrix_type: Type of matrix material
    - fiber_vf: Fiber volume fraction (0.3-0.7)
    - layup: Layup configuration
    - manufacturing: Manufacturing process
    
    Returns:
    - Dictionary with 7 material properties
    """
    # Get base properties
    fiber = fiber_type if fiber_type in MATERIALS_DB else 'Carbon'
    matrix = matrix_type if matrix_type in MATERIALS_DB.get(fiber, {}) else 'Epoxy'
    base = MATERIALS_DB[fiber].get(matrix, MATERIALS_DB['Carbon']['Epoxy'])
    
    # Volume fraction effect (normalized to Vf=0.6)
    vf_factor = fiber_vf / 0.6
    
    # Layup configuration effect
    layup_factor = LAYUP_FACTORS.get(layup, 0.85)
    
    # Manufacturing quality effect
    manuf_factor = MANUFACTURING_FACTORS.get(manufacturing, 0.95)
    
    # Combined multiplication factor
    total_factor = vf_factor * layup_factor * manuf_factor
    
    # Calculate all properties
    return {
        'tensile_strength_MPa': round(base['ts'] * total_factor, 1),
        'tensile_modulus_GPa': round(base['tm'] * total_factor, 1),
        'compressive_strength_MPa': round(base['cs'] * total_factor, 1),
        'flexural_strength_MPa': round(base['fs'] * total_factor, 1),
        'flexural_modulus_GPa': round(base['fm'] * total_factor, 1),
        'ILSS_MPa': round(base['ilss'] * total_factor, 1),
        'impact_energy_J': round(base['ie'] * total_factor, 1)
    }


@app.route('/')
def home():
    """Serve main web interface"""
    try:
        return send_from_directory('static', 'index.html')
    except Exception as e:
        return jsonify({
            'status': 'online',
            'message': 'Composite Materials API',
            'api_docs': '/api',
            'error': 'Web interface not found'
        })


@app.route('/health')
@app.route('/api/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'method': 'empirical_formulas',
        'materials_count': len(MATERIALS_DB),
        'port': PORT,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api')
def api_info():
    """API documentation and information"""
    return jsonify({
        'name': 'Composite Materials Property Prediction API',
        'version': '2.0',
        'status': 'active',
        'method': 'Empirical formulas with rule of mixtures',
        'description': 'Predicts mechanical properties of fiber-reinforced composites',
        'dataset': {
            'fiber_types': 5,
            'matrix_types': 5,
            'total_combinations': 25,
            'layup_configs': 7,
            'manufacturing_processes': 7
        },
        'endpoints': {
            'GET /': 'Web interface',
            'GET /health': 'Health check',
            'GET /api': 'API information',
            'POST /api/predict': 'Single material prediction',
            'POST /api/predict/batch': 'Batch predictions',
            'GET /api/materials': 'Material database',
            'GET /api/options': 'Available options'
        },
        'usage': {
            'example_request': {
                'fiber_type': 'Carbon',
                'matrix_type': 'Epoxy',
                'fiber_volume_fraction': 0.6,
                'layup': 'UD 0°',
                'manufacturing': 'Autoclave'
            }
        }
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Single material property prediction"""
    try:
        data = request.get_json()
        
        # Extract parameters with defaults
        fiber_type = data.get('fiber_type', 'Carbon')
        matrix_type = data.get('matrix_type', 'Epoxy')
        fiber_vf = float(data.get('fiber_volume_fraction', 0.6))
        layup = data.get('layup', 'UD 0°')
        manufacturing = data.get('manufacturing', 'Autoclave')
        
        # Validate fiber volume fraction
        if not (0.3 <= fiber_vf <= 0.7):
            return jsonify({
                'success': False,
                'error': 'Fiber volume fraction must be between 0.3 and 0.7'
            }), 400
        
        # Calculate properties
        predictions = predict_properties(fiber_type, matrix_type, fiber_vf, layup, manufacturing)
        
        return jsonify({
            'success': True,
            'method': 'empirical_formulas',
            'input': {
                'fiber_type': fiber_type,
                'matrix_type': matrix_type,
                'fiber_volume_fraction': fiber_vf,
                'layup': layup,
                'manufacturing': manufacturing
            },
            'predictions': predictions,
            'units': {
                'strength': 'MPa',
                'modulus': 'GPa',
                'ILSS': 'MPa',
                'impact_energy': 'J'
            }
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """Batch predictions for multiple materials"""
    try:
        data = request.get_json()
        samples = data.get('samples', [])
        
        if not samples:
            return jsonify({
                'success': False,
                'error': 'No samples provided'
            }), 400
        
        results = []
        for idx, sample in enumerate(samples):
            try:
                fiber_type = sample.get('fiber_type', 'Carbon')
                matrix_type = sample.get('matrix_type', 'Epoxy')
                fiber_vf = float(sample.get('fiber_volume_fraction', 0.6))
                layup = sample.get('layup', 'UD 0°')
                manufacturing = sample.get('manufacturing', 'Autoclave')
                
                predictions = predict_properties(fiber_type, matrix_type, fiber_vf, layup, manufacturing)
                
                results.append({
                    'index': idx,
                    'input': sample,
                    'predictions': predictions,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'index': idx,
                    'input': sample,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'method': 'empirical_formulas',
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/materials')
def get_materials():
    """Get complete material properties database"""
    return jsonify({
        'success': True,
        'database': MATERIALS_DB,
        'note': 'Base values at fiber volume fraction = 0.6',
        'units': {
            'ts': 'MPa (Tensile Strength)',
            'tm': 'GPa (Tensile Modulus)',
            'cs': 'MPa (Compressive Strength)',
            'fs': 'MPa (Flexural Strength)',
            'fm': 'GPa (Flexural Modulus)',
            'ilss': 'MPa (Interlaminar Shear Strength)',
            'ie': 'J (Impact Energy)'
        }
    })


@app.route('/api/options')
def get_options():
    """Get all available material options"""
    return jsonify({
        'success': True,
        'options': {
            'fiber_types': list(MATERIALS_DB.keys()),
            'matrix_types': ['Epoxy', 'Polyester', 'Vinyl_ester', 'PEEK', 'PA6'],
            'layups': list(LAYUP_FACTORS.keys()),
            'manufacturing': list(MANUFACTURING_FACTORS.keys()),
            'fiber_volume_fraction': {
                'min': 0.3,
                'max': 0.7,
                'recommended': 0.6
            }
        },
        'factors': {
            'layup': LAYUP_FACTORS,
            'manufacturing': MANUFACTURING_FACTORS
        }
    })


print("="*80, file=sys.stderr)
print("✅ API Ready!", file=sys.stderr)
print("Method: Empirical formulas + Rule of mixtures", file=sys.stderr)
print(f"Materials: {len(MATERIALS_DB)} fiber types × 5 matrix types = 25 combinations", file=sys.stderr)
print("="*80, file=sys.stderr)


if __name__ == '__main__':
    print(f"🌐 Starting Flask server on 0.0.0.0:{PORT}", file=sys.stderr)
    app.run(host='0.0.0.0', port=PORT, debug=False)
