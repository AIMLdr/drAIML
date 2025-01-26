# drAIML
machine learning medical diagnosis consultation

```text
draiml/
├── draiml.py                # Main drAIML application
├── chatter.py               # Model handlers and API integrations
├── hippocratic.py           # Medical ethics and decision system
├── logic.py                 # Logic and reasoning system
├── memory.py                # Memory management system
├── openmind.py              # API and model management
├── socratic.py              # Socratic reasoning system
├── oath.txt                 # Dr. AIML's oath
├── prompt.txt               # Dr. AIML's prompt
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── memory/                  # Memory folder structure
    ├── logs/                # System logs
    │   ├── api.log
    │   ├── medical.log
    │   ├── model.log
    │   └── openmind.log
    ├── medical/             # Medical interaction logs
    ├── stm/                 # Short-term memory
    └── ltm/                 # Long-term memory
```
```bash
git clone https://github.com/AIMLdr/drAIML/
```
```bash
cd drAIML
```
```bash
python3 -m venv draiml
source draiml/bin/activate
```
```bash
pip install -r requirements.txt
```
```text
.env
TOGETHER_API_KEY=your_together_key
GROQ_API_KEY=your_groq_key
```
```bash
streamlit run draiml.py
```

NOTE: the streamlit app demo version https://aimldr.streamlit.app works with a together.ai API key to run a private consultation with drAIML use ollama on your local machine 
```bash
git clone https://github.com/AIMLdr/drAIML/
```
and start <a href=://https://ollama.com/download">ollama</a> then run ollamamodel from your ollama list<br />
v2 is on my desk....  will update when ready
