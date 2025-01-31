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
TOGETHER_API_KEY='changemanuallyoraddfromtheui'
GROQ_API_KEY='automaticallyaddedfromthedraimlui'
OPENAI_API_KEY='yourapikeygetsaddedfromthedraimlui'
```
```bash
streamlit run draiml.py
```


NOTE: the streamlit app demo version <a href="https://aimldr.streamlit.app">streamlet demo</a> is web based requiring a <a href="https://api.together.ai/">together.ai</a> API key<br /> <a href="https://console.groq.com/keys">groq</a> API key or an <a href="https://platform.openai.com/docs/api-reference/introduction">openai</a> API key
# For private healthcare consultation with drAIML
install <a href="https://ollama.com/download">ollama</a> then ollama run yourmodel from your ollama list<br />
drAIML will see your running ollama model and then choose the running model from the list of models you have installed.
