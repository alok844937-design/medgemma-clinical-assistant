from flask import Flask, request, jsonify, render_template_string
import os
from typing import Dict, List
import re

app = Flask(__name__)

# Simulated MedGemma model responses
class MedGemmaModel:
    def __init__(self):
        self.patient_mode = True
    
    def process_patient_explanation(self, medical_text: str) -> str:
        """Convert medical jargon to patient-friendly language"""
        explanations = {
            'hypertension': 'high blood pressure',
            'myocardial infarction': 'heart attack',
            'diabetes mellitus': 'diabetes (high blood sugar)',
            'hyperlipidemia': 'high cholesterol',
            'anticoagulant': 'blood thinner medication',
            'beta-blocker': 'heart rate and blood pressure medication',
            'statin': 'cholesterol-lowering medication',
        }
        
        result = medical_text.lower()
        for medical, simple in explanations.items():
            result = result.replace(medical.lower(), f"**{simple}**")
        
        return f"""
### Patient-Friendly Explanation

{result}

**What this means for you:**
- Follow your doctor's instructions carefully
- Take all medications as prescribed
- Contact your doctor if you have any concerns
- Attend all follow-up appointments

**Important:** This is a simplified explanation. Please discuss with your healthcare provider.
"""
    
    def process_doctor_structure(self, clinical_notes: str) -> str:
        """Structure clinical information for doctors"""
        return f"""
### Structured Clinical Summary

**Chief Complaint & History:**
{clinical_notes[:200]}...

**Assessment:**
- Primary diagnosis identified
- Relevant comorbidities noted
- Risk factors documented

**Plan:**
1. Medication management as prescribed
2. Follow-up scheduling recommended
3. Patient education completed
4. Monitoring parameters established

**Clinical Notes:**
{clinical_notes}

---
*Generated using MedGemma Clinical Assistant*
"""

model = MedGemmaModel()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MedGemma Clinical Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1.1em;
            font-weight: 600;
            color: #6c757d;
            transition: all 0.3s;
        }
        .tab:hover { background: #e9ecef; }
        .tab.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }
        .content {
            padding: 40px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
            font-size: 1.1em;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .output {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .output h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .output pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MedGemma Clinical Assistant</h1>
            <p>AI-Powered Medical Documentation</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('patient', event)">
                Patient Mode
            </button>
            <button class="tab" onclick="switchTab('doctor', event)">
                Doctor Mode
            </button>
        </div>
        
        <div class="content">
            <div id="patient-mode">
                <h2 style="margin-bottom: 20px;">Patient-Friendly Explanations</h2>
                
                <form id="patient-form">
                    <div class="form-group">
                        <label for="patient-input">Enter Medical Text:</label>
                        <textarea id="patient-input" placeholder="Paste discharge summary here..."></textarea>
                    </div>
                    <button type="submit" class="btn">Generate Explanation</button>
                </form>
                
                <div id="patient-output" class="output" style="display:none;">
                    <h3>Patient Explanation:</h3>
                    <pre id="patient-result"></pre>
                </div>
            </div>
            
            <div id="doctor-mode" style="display:none;">
                <h2 style="margin-bottom: 20px;">Clinical Documentation Assistant</h2>
                
                <form id="doctor-form">
                    <div class="form-group">
                        <label for="doctor-input">Enter Clinical Notes:</label>
                        <textarea id="doctor-input" placeholder="Enter patient history..."></textarea>
                    </div>
                    <button type="submit" class="btn">Structure Notes</button>
                </form>
                
                <div id="doctor-output" class="output" style="display:none;">
                    <h3>Structured Documentation:</h3>
                    <pre id="doctor-result"></pre>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function switchTab(mode, evt) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            evt.target.classList.add('active');
            
            document.getElementById('patient-mode').style.display = mode === 'patient' ? 'block' : 'none';
            document.getElementById('doctor-mode').style.display = mode === 'doctor' ? 'block' : 'none';
        }
        
        document.getElementById('patient-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('patient-input').value;
            
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, mode: 'patient'})
            });

            const data = await response.json();

            if (!response.ok) {alert(data.error); return;}

            document.getElementById('patient-result').textContent = data.result;
            document.getElementById('patient-output').style.display = 'block';
        });
        
        document.getElementById('doctor-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('doctor-input').value;
            
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, mode: 'doctor'})
            });
            
            const data = await response.json();

            if (!response.ok) {alert(data.error); return;}

            document.getElementById('doctor-result').textContent = data.result;
            document.getElementById('doctor-output').style.display = 'block';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '').strip()
    mode = data.get('mode', 'patient')
    
    if not text:
        return jsonify({
            "error": "Please enter medical text before generating output."
        }), 400
    
    if mode == 'patient':
        result = model.process_patient_explanation(text)
    elif mode == 'doctor':
        result = model.process_doctor_structure(text)
    else:
        return jsonify({"error": "Invalid mode"}), 400 
    return jsonify({'result': result})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)