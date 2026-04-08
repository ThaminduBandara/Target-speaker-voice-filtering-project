#!/usr/bin/env python3
"""
Generate comprehensive project PDF documentation
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Create PDF
pdf_filename = os.path.join(os.path.dirname(__file__), "Project_Documentation.pdf")
doc = SimpleDocTemplate(pdf_filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for PDF elements
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#2563eb'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=colors.HexColor('#1e40af'),
    spaceAfter=8,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=6,
    leading=14
)

tech_style = ParagraphStyle(
    'TechStyle',
    parent=styles['BodyText'],
    fontSize=9,
    textColor=colors.HexColor('#1f2937'),
    spaceAfter=4,
    leading=12
)

# ==================== COVER PAGE ====================
elements.append(Spacer(1, 1.5*inch))
elements.append(Paragraph("🎙️ TARGET SPEAKER VOICE FILTERING PROJECT", title_style))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("Advanced Voice Separation & Speaker Identification System", 
                         ParagraphStyle('subtitle', parent=styles['Heading3'], 
                                       fontSize=14, textColor=colors.HexColor('#4b5563'),
                                       alignment=TA_CENTER)))
elements.append(Spacer(1, 0.8*inch))
elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", 
                         ParagraphStyle('date', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER)))
elements.append(PageBreak())

# ==================== TABLE OF CONTENTS ====================
elements.append(Paragraph("TABLE OF CONTENTS", heading_style))
elements.append(Spacer(1, 0.2*inch))
toc_items = [
    "1. Project Overview",
    "2. Key Technologies",
    "3. System Architecture",
    "4. How It Works (3-Step Pipeline)",
    "5. Core Components",
    "6. Project Structure",
    "7. Setup & Installation",
    "8. Running the Backend",
    "9. API Endpoints",
    "10. Use Cases & Applications"
]
for item in toc_items:
    elements.append(Paragraph(item, body_style))
    elements.append(Spacer(1, 0.1*inch))
elements.append(PageBreak())

# ==================== 1. PROJECT OVERVIEW ====================
elements.append(Paragraph("1. PROJECT OVERVIEW", heading_style))
elements.append(Spacer(1, 0.15*inch))
overview_text = """
<b>Target Speaker Voice Filtering Project</b> is an advanced audio processing system that combines voice separation and speaker recognition to extract a specific person's voice from multi-speaker environments. The system learns what your voice sounds like, then uses that knowledge to identify and extract your voice from noisy recordings containing multiple speakers.
<br/><br/>
This is particularly useful for:
<ul>
<li>Extracting your voice from group meetings or conferences</li>
<li>Cleaning background noise and other speakers from recordings</li>
<li>Improving transcription accuracy by isolating target speaker</li>
<li>Voice authentication and speaker verification applications</li>
<li>Multi-speaker audio processing and analysis</li>
</ul>
"""
elements.append(Paragraph(overview_text, body_style))
elements.append(Spacer(1, 0.2*inch))

# ==================== 2. KEY TECHNOLOGIES ====================
elements.append(Paragraph("2. KEY TECHNOLOGIES", heading_style))
elements.append(Spacer(1, 0.15*inch))

tech_data = [
    ["Technology", "Purpose", "Details"],
    ["SepFormer", "Voice Separation", "Neural network model that separates multiple speakers from a single audio stream. Pre-trained on WHAM-R dataset."],
    ["ECAPA", "Speaker Embedding", "State-of-the-art speaker recognition model. Creates a 192-dimensional embedding (fingerprint) for each speaker."],
    ["PyTorch", "Deep Learning Framework", "Core ML framework for model inference and tensor operations."],
    ["TorchAudio", "Audio Processing", "High-level audio operations: loading, resampling, filtering, normalization."],
    ["FastAPI", "Backend Server", "Modern REST API framework for Python. Enables React frontend communication."],
    ["SpeechBrain", "Model Hub", "Open-source speech processing library. Provides pretrained models."],
    ["Sounddevice", "Audio I/O", "Records audio from microphone in real-time."],
]

tech_table = Table(tech_data, colWidths=[1.2*inch, 1.3*inch, 2.2*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))
elements.append(tech_table)
elements.append(PageBreak())

# ==================== 3. SYSTEM ARCHITECTURE ====================
elements.append(Paragraph("3. SYSTEM ARCHITECTURE", heading_style))
elements.append(Spacer(1, 0.15*inch))

arch_text = """
The system follows a modular microservices architecture with clear separation of concerns:
<br/><br/>
<b>Frontend Layer:</b> React-based web interface (optional)<br/>
<b>Backend Layer:</b> FastAPI server with CORS support for cross-origin requests<br/>
<b>Service Layer:</b> Core business logic modules
<ul>
<li><b>Record Service:</b> Handles microphone input and audio recording</li>
<li><b>Embedding Service:</b> Extracts speaker fingerprints using ECAPA</li>
<li><b>Separation Service:</b> Separates voices using SepFormer</li>
<li><b>Model Loader:</b> Manages pretrained model loading and caching</li>
</ul>
<b>Storage Layer:</b> Local file system for recordings, embeddings, and model weights
"""
elements.append(Paragraph(arch_text, body_style))
elements.append(Spacer(1, 0.2*inch))

# ==================== 4. HOW IT WORKS ====================
elements.append(Paragraph("4. HOW IT WORKS (3-STEP PIPELINE)", heading_style))
elements.append(Spacer(1, 0.15*inch))

# Step 1
elements.append(Paragraph("STEP 1: ENROLLMENT (Create Voice Profile)", subheading_style))
step1_text = """
<b>Objective:</b> Create a unique voice fingerprint for the target speaker<br/>
<b>Process:</b>
<ul>
<li>User records 5 seconds of clean, clear speech</li>
<li>Audio is captured at 16kHz sample rate</li>
<li>ECAPA model processes the audio to generate a 192-dimensional embedding</li>
<li>Embedding is saved to disk: <b>enroll_embedding.pt</b></li>
</ul>
<b>Output:</b> Voice fingerprint (embedding vector) that uniquely identifies the speaker
"""
elements.append(Paragraph(step1_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# Step 2
elements.append(Paragraph("STEP 2: VOICE SEPARATION", subheading_style))
step2_text = """
<b>Objective:</b> Separate multiple speakers from a single audio stream<br/>
<b>Process:</b>
<ul>
<li>User records 5 seconds of audio with multiple speakers</li>
<li>SepFormer neural network analyzes the mixture and identifies distinct speaker sources</li>
<li>Audio is separated into individual speaker streams (typically 2-4 speakers)</li>
<li>Each separated speaker is saved as a separate WAV file</li>
<li>Audio is resampled from 8kHz to 16kHz for compatibility</li>
</ul>
<b>Output:</b> Multiple speaker WAV files (speaker_0.wav, speaker_1.wav, etc.)
"""
elements.append(Paragraph(step2_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# Step 3
elements.append(Paragraph("STEP 3: SPEAKER MATCHING & SELECTION", subheading_style))
step3_text = """
<b>Objective:</b> Identify and extract the target speaker's voice<br/>
<b>Process:</b>
<ul>
<li>For each separated speaker stream, compute an embedding using ECAPA</li>
<li>Calculate cosine similarity between target embedding and each separated speaker</li>
<li>Select the speaker with highest similarity score (best match)</li>
<li>Return the filtered audio containing only the target speaker's voice</li>
</ul>
<b>Output:</b> Clean audio file containing ONLY the target speaker's voice
"""
elements.append(Paragraph(step3_text, body_style))
elements.append(PageBreak())

# ==================== 5. CORE COMPONENTS ====================
elements.append(Paragraph("5. CORE COMPONENTS", heading_style))
elements.append(Spacer(1, 0.15*inch))

# Component 1: SepFormer
elements.append(Paragraph("A. SepFormer Voice Separator", subheading_style))
comp_text1 = """
<b>Model:</b> SepFormer-WHAM-R (Pretrained on WHAM-R dataset)<br/>
<b>Input:</b> Mono audio waveform (8kHz)<br/>
<b>Output:</b> Separated waveforms for N speakers<br/>
<b>Architecture:</b> Transformer-based architecture optimized for speaker separation<br/>
<b>Capabilities:</b> Can separate 2-4 speakers with high quality<br/>
<b>Processing:</b> Returns 8kHz audio which is upsampled to 16kHz for consistency
"""
elements.append(Paragraph(comp_text1, tech_style))
elements.append(Spacer(1, 0.1*inch))

# Component 2: ECAPA
elements.append(Paragraph("B. ECAPA Speaker Embedding", subheading_style))
comp_text2 = """
<b>Model:</b> ECAPA-TDNN (Emphasizing Channel and Phonetic Awareness)<br/>
<b>Input:</b> Audio waveform at 16kHz<br/>
<b>Output:</b> 192-dimensional embedding vector<br/>
<b>Training Data:</b> Pretrained on VoxCeleb dataset (100k+ speakers)<br/>
<b>Purpose:</b> Creates speaker-specific "fingerprints" that are consistent for the same speaker<br/>
<b>Similarity Metric:</b> Cosine similarity is used to compare embeddings
"""
elements.append(Paragraph(comp_text2, tech_style))
elements.append(Spacer(1, 0.1*inch))

# Component 3: Backend API
elements.append(Paragraph("C. FastAPI Backend Server", subheading_style))
comp_text3 = """
<b>Framework:</b> FastAPI (async, high-performance)<br/>
<b>CORS Configuration:</b> Allows requests from any origin for React frontend integration<br/>
<b>Endpoints:</b> REST API for enrollment, embedding extraction, and voice filtering<br/>
<b>File Serving:</b> Returns processed WAV files as downloadable audio
"""
elements.append(Paragraph(comp_text3, tech_style))
elements.append(PageBreak())

# ==================== 6. PROJECT STRUCTURE ====================
elements.append(Paragraph("6. PROJECT STRUCTURE", heading_style))
elements.append(Spacer(1, 0.15*inch))

structure_text = """
<b>/backend</b> - FastAPI server and core services<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>main.py</b> - API routes and endpoints<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>services/</b> - Business logic modules<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>record_service.py</b> - Microphone recording<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>embedding_service.py</b> - ECAPA embeddings<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>separation_service.py</b> - SepFormer separation<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>model_loader.py</b> - Model initialization<br/>
<br/>
<b>/src</b> - Standalone Python scripts for development<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>target_speaker.py</b> - Complete pipeline (Step 3)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>record_enroll.py</b> - Step 1 standalone<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>extract_embedding.py</b> - Step 2 standalone<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>identify_my_voice.py</b> - Speaker matching logic<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>separate_voice.py</b> - Voice separation pipeline<br/>
<br/>
<b>/pretrained_models</b> - Downloaded model weights<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>sepformer-whamr/</b> - SepFormer model files<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>spkrec-ecapa/</b> - ECAPA model files<br/>
<br/>
<b>/recordings</b> - Audio files and embeddings<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>my_voice_samples/</b> - Enrollment recordings<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>enroll_embedding/</b> - Saved speaker embeddings<br/>
&nbsp;&nbsp;&nbsp;&nbsp;<b>step3_output/</b> - Filtered output audio files
"""
elements.append(Paragraph(structure_text, tech_style))
elements.append(PageBreak())

# ==================== 7. SETUP & INSTALLATION ====================
elements.append(Paragraph("7. SETUP & INSTALLATION", heading_style))
elements.append(Spacer(1, 0.15*inch))

setup_text = """
<b>Prerequisites:</b>
<ul>
<li>Python 3.8+ installed</li>
<li>pip package manager</li>
<li>Virtual environment (recommended)</li>
<li>Microphone for audio input</li>
</ul>
<br/>
<b>Step 1: Clone Repository</b>
<pre>git clone &lt;repository-url&gt;
cd voiceFilterProject</pre>
<br/>
<b>Step 2: Create Virtual Environment</b>
<pre>python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate     # Windows</pre>
<br/>
<b>Step 3: Install Dependencies</b>
<pre>pip install -r requirements.txt
pip install fastapi uvicorn</pre>
<br/>
<b>Step 4: Download Pretrained Models</b>
<pre>python src/pretrained_model_download.py</pre>
"""
elements.append(Paragraph(setup_text, body_style))
elements.append(PageBreak())

# ==================== 8. RUNNING THE BACKEND ====================
elements.append(Paragraph("8. RUNNING THE BACKEND", heading_style))
elements.append(Spacer(1, 0.15*inch))

run_text = """
<b>Start the FastAPI Server:</b>
<pre>uvicorn backend.main:app --reload</pre>
<br/>
<b>Expected Output:</b>
<pre>INFO:     Started server process
INFO:     Waiting for application startup
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000</pre>
<br/>
<b>Access API Documentation:</b> <b>http://localhost:8000/docs</b>
<br/><br/>
<b>Server Configuration:</b>
<ul>
<li>Host: 127.0.0.1 (local)</li>
<li>Port: 8000</li>
<li>CORS: Enabled for all origins</li>
<li>Auto-reload: Enabled for development</li>
</ul>
<br/>
<b>For Production:</b>
<pre>uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4</pre>
"""
elements.append(Paragraph(run_text, body_style))
elements.append(PageBreak())

# ==================== 9. API ENDPOINTS ====================
elements.append(Paragraph("9. API ENDPOINTS", heading_style))
elements.append(Spacer(1, 0.15*inch))

endpoints_data = [
    ["Endpoint", "Method", "Purpose", "Response"],
    ["/", "GET", "Health check", "Server status message"],
    ["/record-enroll", "POST", "Record enrollment audio (Step 1)", "Path to saved audio"],
    ["/extract-embedding", "POST", "Extract speaker embedding (Step 2)", "Path to embedding file"],
    ["/separate", "POST", "Separate and filter audio (Step 3)", "URLs to mixture and cleaned audio"],
    ["/file/{filename}", "GET", "Download processed audio file", "WAV audio file"],
]

endpoints_table = Table(endpoints_data, colWidths=[1.3*inch, 0.8*inch, 1.7*inch, 1.2*inch])
endpoints_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 7.5),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))
elements.append(endpoints_table)
elements.append(Spacer(1, 0.2*inch))

# Example request/response
elements.append(Paragraph("Example API Call:", subheading_style))
example_text = """
<b>Request:</b><pre>curl -X POST http://localhost:8000/record-enroll</pre>
<br/>
<b>Response:</b><pre>{"saved": "/path/to/recordings/my_voice_samples/clean_voice.wav"}</pre>
"""
elements.append(Paragraph(example_text, tech_style))
elements.append(PageBreak())

# ==================== 10. USE CASES & APPLICATIONS ====================
elements.append(Paragraph("10. USE CASES & APPLICATIONS", heading_style))
elements.append(Spacer(1, 0.15*inch))

usecases_text = """
<b>1. Meeting & Conference Recording</b>
<ul>
<li>Extract your voice from multi-participant video calls</li>
<li>Isolate speaker for transcription and note-taking</li>
<li>Remove background noise and other speakers</li>
</ul>
<br/>
<b>2. Podcast & Content Production</b>
<ul>
<li>Separate guest interviews from host voice</li>
<li>Extract lead actor from group scenes</li>
<li>Remove background dialogue and ambient noise</li>
</ul>
<br/>
<b>3. Accessibility Applications</b>
<ul>
<li>Enhance hearing aid audio by filtering target speaker</li>
<li>Improve speech recognition accuracy for individuals</li>
<li>Provide speaker-specific audio filtering</li>
</ul>
<br/>
<b>4. Security & Authentication</b>
<ul>
<li>Voice-based authentication systems</li>
<li>Speaker verification and identification</li>
<li>Fraud detection in voice-based transactions</li>
</ul>
<br/>
<b>5. Research & Development</b>
<ul>
<li>Speech processing algorithm testing</li>
<li>Multi-speaker separation research</li>
<li>Speaker recognition model evaluation</li>
</ul>
<br/>
<b>6. Real-time Communication</b>
<ul>
<li>Zoom/Teams call noise reduction</li>
<li>Telehealth consultation clarity</li>
<li>Customer service call recording enhancement</li>
</ul>
"""
elements.append(Paragraph(usecases_text, body_style))
elements.append(Spacer(1, 0.3*inch))

# ==================== FOOTER ====================
footer_text = """
<b>Project Repository:</b> Target-speaker-voice-filtering-project<br/>
<b>Author:</b> ThaminduBandara<br/>
<b>License:</b> Open Source<br/>
<b>Last Updated:</b> February 2026
"""
elements.append(Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], 
                                                      fontSize=9, textColor=colors.grey,
                                                      alignment=TA_CENTER)))

# Build PDF
doc.build(elements)
print(f"✅ PDF generated successfully: {pdf_filename}")
print(f"📄 File size: {os.path.getsize(pdf_filename) / 1024:.1f} KB")
