# TACTIK AI 5.3 Premium - MVP

**Strategic Intelligence Platform with Scientific Validation**

A web-based MVP for creating high-fidelity avatar simulations powered by real LLMs, enabling strategic preparation for high-stakes interactions.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key (or Anthropic API Key)
- Modern web browser

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Tactik-AI-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Start the server
python api.py
```

The application will be available at **http://localhost:8000**

---

## 📋 Features

### Core Capabilities

✅ **High-Fidelity Avatar Creation**
- Build avatars from verified ground truth sources
- Tier-based source weighting (Primary → Inferred)
- DNA profile construction with behavioral patterns

✅ **Real-Time AI Conversations**
- Powered by GPT-4 or Claude
- Strategic, context-aware responses
- Multi-turn conversation tracking

✅ **Scientific Validation (AVDA)**
- Accuracy scoring (0-100%)
- 95% confidence intervals
- Source coverage analysis
- Classification: Very High/High/Medium/Low/Unreliable

✅ **Quality Assurance**
- Empathy Pause (uncertainty detection)
- Backflow Detection (conversation drift)
- Gating with Hysteresis (quality control)
- Real-time metrics (EIS, HCA, DNA)

✅ **TACTIK Advisor Reports**
- Strategic insights generation
- 72-hour action plans
- Transparency cards with audit trail
- PDF export functionality

---

## 🏗️ Architecture

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML + Tailwind CSS + Vanilla JS
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Storage**: JSON files (data/)
- **Reports**: ReportLab (PDF generation)

### Project Structure

```
Tactik-AI-/
├── api.py                      # FastAPI backend
├── tactik_algorithm.py         # Core TACTIK 5.3 engine
├── llm_integration.py          # LLM integration layer
├── pdf_generator.py            # PDF report generation
├── example_usage.py            # Example: Ecuador → EDEKA
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── static/
│   ├── index.html             # Main web UI
│   └── app.js                 # Frontend logic
├── data/                      # Persistent storage (auto-created)
│   ├── avatars.json
│   └── sessions.json
├── reports/                   # Generated PDF reports
└── README_MVP.md              # This file
```

---

## 🎯 Usage Guide

### 1. Create an Avatar

1. Navigate to **Create Avatar** tab
2. Fill in basic information:
   - Avatar ID (e.g., `ceo_company`)
   - Name (e.g., `John Smith`)
   - Role (e.g., `Chief Executive Officer`)
   - Environment/Context
3. Add Ground Truth Sources:
   - Minimum 3 sources recommended
   - Select tier (Primary/Secondary/Tertiary/Inferred)
   - Add description and URL
   - Mark if cross-verified
4. Enter DNA components (simplified for MVP):
   - Key influences
   - Behavioral patterns
   - Communication style
   - Priorities
5. Click **Create Avatar**
6. Review AVDA score and classification

### 2. Start a Simulation Session

1. Navigate to **Sessions** tab
2. Click **New Session**
3. Enter your strategic goal
4. Select an avatar
5. Begin conversation

### 3. Conduct Strategic Preparation

- Ask questions as you would in the real interaction
- Monitor real-time metrics (EIS, HCA, DNA scores)
- Watch for quality controls:
  - **Empathy Pause**: High uncertainty detected
  - **Backflow**: Conversation drift correction
- Continue multi-turn conversation

### 4. Generate Reports

- Click **Generate Report** for strategic insights
- Click **Export PDF** for professional report with:
  - Avatar validation metrics
  - Key insights
  - Strategic recommendations
  - 72-hour action plan
  - Transparency card

---

## 📊 Understanding Metrics

### AVDA Score (Avatar Validation Deviation & Accuracy)

| Score | Classification | Use Case |
|-------|----------------|----------|
| 90-100% | Very High Fidelity | Critical decisions, real negotiations |
| 75-89% | High Fidelity | Strategic preparation, executive training |
| 60-74% | Medium Fidelity | Scenario exploration, brainstorming |
| 45-59% | Low Fidelity | Hypothetical exercises only |
| <45% | Unreliable | DO NOT USE for strategic preparation |

### Real-Time Conversation Metrics

- **EIS (Emotional Intelligence Score)**: Empathy, awareness, appropriate tone
- **HCA (Human-Centered Approach)**: Practical value, actionable insights
- **DNA Score**: Alignment with avatar profile
- **TACTIK Score**: Composite metric (0-10 scale)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required: At least one LLM provider
OPENAI_API_KEY=sk-your-key-here

# Optional: Alternative LLM
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Server configuration (optional)
PORT=8000
HOST=0.0.0.0
```

### LLM Provider Selection

The system automatically detects and uses available providers:
1. OpenAI GPT-4 (default if available)
2. Anthropic Claude (fallback)

To test without LLM (placeholder responses):
- Don't set any API keys
- System will use simulated responses

---

## 🧪 Testing

### Test LLM Integration

```bash
python llm_integration.py
```

### Test PDF Generation

```bash
python pdf_generator.py
```

### Run Example Scenario

```bash
python example_usage.py
```

---

## 📱 API Endpoints

### Avatars

- `POST /api/avatars` - Create avatar
- `GET /api/avatars` - List all avatars
- `GET /api/avatars/{avatar_id}` - Get avatar details

### Sessions

- `POST /api/sessions` - Create session
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details

### Conversation

- `POST /api/chat` - Send message and get response

### Reports

- `GET /api/sessions/{session_id}/report` - Generate TACTIK Advisor report
- `GET /api/sessions/{session_id}/export/pdf` - Export PDF report

### Health

- `GET /health` - System health check

---

## 🎓 Example Use Cases

### 1. Diplomatic Negotiation Preparation
- Create avatars of key stakeholders (ministers, diplomats, NGO leaders)
- Simulate multi-stakeholder negotiations
- Identify cultural sensitivities and strategic approaches

### 2. Business M&A Preparation
- Model target company executives
- Practice pitch conversations
- Anticipate objections and concerns

### 3. Legal Cross-Examination
- Simulate opposing counsel or witnesses
- Practice questioning strategies
- Refine argumentation approach

### 4. Healthcare Difficult Conversations
- Prepare for patient/family discussions
- Practice empathetic communication
- Anticipate emotional responses

### 5. Academic Socratic Discussion
- Create philosophical thinkers (Socrates, Kant, etc.)
- Engage in dialectical reasoning
- Explore ethical dilemmas

---

## 🔒 Security & Privacy

### Data Storage

- All data stored locally in `data/` directory
- No cloud storage in MVP
- JSON files: `avatars.json`, `sessions.json`

### API Keys

- Never commit `.env` to version control
- Keys sent only to respective LLM providers
- No third-party tracking

### Best Practices

1. Don't store sensitive personal information in avatar DNAs
2. Use generic descriptions when possible
3. Review transparency cards before sharing reports
4. Regularly rotate API keys

---

## 🚧 Limitations (MVP)

### Current Limitations

1. **Single-avatar conversations**: Multi-avatar orchestration not yet in UI
2. **Simplified DNA builder**: Full DNA components available via API only
3. **No user authentication**: Single-user system
4. **Local storage only**: No database persistence
5. **Basic UI**: Functional but not production-polished

### Planned Enhancements

- [ ] Multi-avatar conversation UI
- [ ] Advanced DNA builder with full component support
- [ ] User authentication and multi-user support
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] Voice conversation support
- [ ] Mobile app (React Native)
- [ ] Microsoft Teams integration
- [ ] Real-time collaboration
- [ ] Advanced semantic analysis
- [ ] Conversation replay and analysis

---

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Project Extensions

The MVP is designed for easy extension:

1. **Custom LLM providers**: Extend `llm_integration.py`
2. **Additional metrics**: Modify `tactik_algorithm.py`
3. **UI enhancements**: Edit `static/index.html` and `static/app.js`
4. **Report templates**: Customize `pdf_generator.py`

---

## 📞 Support

For questions or issues:
- Review documentation in `/documentation`
- Check the full whitepaper: `Perplexity white paper Jax.txt`
- Open GitHub issues
- Contact: [Your contact information]

---

## 📜 License

See LICENSE file for details.

---

## 🙏 Acknowledgments

**TACTIK AI 5.3 Premium Edition**
*Author*: Santiago Cañas
*Mission*: Democratizing elite preparation through AI simulation
*Tagline*: "We don't need AI that answers. We need AI that helps us think better."

---

**Version**: MVP 1.0
**Last Updated**: 2024
**Status**: Ready for pilot deployment
