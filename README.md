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
Introduction to drAIML - Medical AI Consultant

drAIML is an advanced medical AI consultation system leveraging (A)rtificial (I)ntelligence (M)achine (L)earning technology to provide accurate, ethical, and compassionate medical information to patients as participants. Designed to be an autonomous medical expert, drAIML integrates multiple AI models, ethical medical practices, and sophisticated reasoning systems to deliver personalized medical consultations while maintaining strict ethical guidelines and ensuring patient safety.
Purpose

The primary purpose of drAIML is to bridge the gap between medical expertise and accessibility. By harnessing the power of AI, drAIML aims to provide users with immediate access to medical insights, symptom analysis, and treatment recommendations, especially in situations where professional medical advice may not be readily available. It is engineered to act as a trustworthy medical assistant that adheres to the highest standards of medical ethics and confidentiality.
Key Features

    Multiple AI Model Integration: Supports various AI providers, including OpenAI's GPT-4, Groq models, Together.ai, and local models through Ollama. This flexibility ensures robustness and availability.

    Ethical Medical Practice: Implements the Hippocratic principles through the hippocratic.py module, ensuring that all recommendations adhere to medical ethics, including "do no harm," patient confidentiality, and informed consent.

    Socratic Reasoning: Utilizes a Socratic reasoning system (socratic.py) to engage in logical, in-depth dialogues with users, enhancing the accuracy and reliability of its responses.

    Comprehensive Memory Management: Incorporates a memory system (memory.py) for storing conversation history, medical decisions, and analytics, enabling continuous learning and personalization.

    Dynamic Model Selection: Allows users to select the AI model provider and configure settings according to their preferences and needs.

    Emergency Detection and Response: Equipped with the ability to recognize emergency situations and provide appropriate guidance, including advising users to seek immediate professional medical help.

Areas for enhancement

    Privacy and Security: Prioritizes user privacy by implementing secure data handling practices and safeguarding sensitive medical information.

Mission Statement

To provide accessible, reliable, and ethical medical consultations powered by advanced AI technologies, while upholding the highest standards of medical ethics and patient care.
Vision

drAIML envisions a future where high-quality medical advice is accessible to everyone, anytime and anywhere. By combining state-of-the-art artificial intelligence with rigorous ethical practices, drAIML strives to empower individuals with the knowledge they need to make informed health decisions, ultimately contributing to better health outcomes worldwide.
Core Values

    Precision: Ensuring all medical information and advice provided is accurate and evidence-based.

    Compassion: Interacting with users empathetically, acknowledging the human aspect of healthcare.

    Evolution: Continuously learning and adapting to new medical research and user feedback to improve service quality.

    Accountability: Taking responsibility for the information provided and ensuring that it aligns with medical best practices.

How It Works

drAIML operates through a user-friendly interface where users can describe their symptoms or ask health-related questions. The system processes the input using the selected AI model, applies ethical reasoning and safety checks, and generates a response. This response is then validated against medical guidelines and ethical standards before being presented to the user.

The system is designed to:

    Analyze user input for medical relevance and urgency.
    Generate responses that are clear, concise, and actionable.
    Provide disclaimers and encourage professional medical consultation when necessary.
    Maintain a conversation history for context and continuity.

Ethical Considerations

drAIML is built with a strong emphasis on ethical medical practice. It incorporates the following ethical principles:

    Do No Harm: Prioritizes user safety by avoiding harmful recommendations and recognizing its limitations.

    Patient Confidentiality: Ensures all user data is handled securely and privately.

    Informed Consent: Provides information in a way that allows users to make informed decisions about their health.

    Emergency Protocols: Recognizes signs of medical emergencies and advises users to seek immediate professional help.

Getting Started

To use drAIML, participants select their preferred AI provider, configure any necessary settings, and begin interacting with the system through the consultation interface. The system guides users through the process, ensuring that they have all the information needed to make the most of the service.
Contributions and Further Development

drAIML is an open-source project that welcomes contributions from the developer and medical communities. By collaborating, we aim to enhance the system's capabilities, expand its knowledge base, and improve its effectiveness in providing ethical and accurate medical consultations.
Disclaimer
While drAIML strives to provide accurate and helpful medical information, it is not a substitute for professional medical advice, diagnosis, or treatment. Users are encouraged to consult qualified healthcare providers for any medical concerns or conditions. drAIML is designed to augment medical advice useful for both patients and health care professionals for accurate assessments as diganosis.


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
