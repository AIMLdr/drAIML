# drAIML - Medical AI Consultant
## Technical Documentation

### Project Overview
drAIML is a medical AI consultation system that integrates multiple large language models (LLMs) with ethical medical practice, Socratic reasoning, and comprehensive safety protocols. The system provides a streamlined interface for medical consultations while maintaining strict ethical guidelines and comprehensive logging.

### System Architecture

#### Core Components

**OpenMind (`openmind.py`)**
   - API key management
   - Memory structure initialization
   - Comprehensive logging system
   - File handling (oath.txt, prompt.txt)
   - Error tracking and management
   - Log rotation and archival

  **Chatter System (`chatter.py`)**
   - Model interface implementations:
     - OpenAI GPT-4
     - Groq
     - Together.ai
     - Ollama (local models)
   - Asynchronous response generation
   - Error handling and timeout management
   - System prompt integration
   - Model validation and verification

  **Memory Management (`memory.py`)**
   - Conversation history tracking
   - Short-term memory (STM)
   - Long-term memory (LTM)
   - Dialog entry structuring
   - Medical decision storage
   - Analytics tracking

  **Socratic Reasoning (`socratic.py`)**
   - Medical reasoning implementation
   - Premise validation
   - Conclusion generation
   - Logic verification
   - Medical context validation

### Directory Structure
draiml/
├── app.py # Main Streamlit application
├── chatter.py # Model handlers
├── hippocratic.py # Medical ethics system
├── logic.py # Logic and reasoning system
├── memory.py # Memory management
├── openmind.py # API and model management
├── socratic.py # Socratic reasoning system
├── oath.txt # Dr. AIML's oath
├── prompt.txt # Dr. AIML's prompt
└── memory/ # Memory folder structure
├── logs/ # System logs
├── medical/ # Medical decisions
├── stm/ # Short-term memory
├── ltm/ # Long-term memory
└── analytics/ # Usage analytics

### Key Features

#### Model Integration
- **Multiple Model Support**
  - OpenAI GPT-4 integration
  - Groq model support
  - Together.ai implementation
  - Local Ollama model support
  - Dynamic model selection
  - Automatic model validation

- **Model Management**
  - Asynchronous response generation
  - Configurable timeouts
  - Error recovery
  - Model performance tracking
  - Response validation

#### Memory System
- **Hierarchical Storage**
  - Short-term conversation memory
  - Long-term knowledge storage
  - Medical decision archival
  - Error logging and tracking
  - Analytics storage

- **Data Management**
  - Automatic cleanup
  - Log rotation
  - Data archival
  - Memory optimization
  - Backup systems

#### Medical Ethics
- **Ethical Framework**
  - Hippocratic principles
  - Medical decision validation
  - Privacy protection
  - Data security
  - Professional boundaries

- **Safety Protocols**
  - Emergency detection
  - Risk assessment
  - Referral recommendations
  - Confidence scoring
  - Validation checks

### Implementation Details

#### Response Generation Flow

User Input → Model Selection → Prompt Construction → 
Response Generation → Validation → Ethics Check → 
Memory Storage → User Display
# Memory Management Flow


Dialog Entry → STM Storage → Analytics Update → 
Periodic Cleanup → LTM Archival
```Model Selection Process

Provider Selection → API Validation → Model Availability Check →
Model Initialization → System Prompt Integration →
Response Generation
Configuration
# Environment Variables
```text
TOGETHER_API_KEY=your_together_key
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```
# Model Configuration
Timeout settings
Response parameters
Model-specific configurations
System prompt customization
# Memory Settings
Cleanup intervals
Archive policies
Log rotation
Backup frequency
Error Handling
# Model Errors
Timeout recovery
API error handling
Model fallback
Response validation
# Memory Errors
Storage verification
Data integrity checks
Recovery procedures
Backup systems
# System Errors
Comprehensive logging
Error tracking
Recovery mechanisms
User notification
Security Considerations
# Data Protection
API key security
Conversation privacy
Medical data protection
Log file security
# Access Control
API rate limiting
Request validation
Response sanitization
Error masking
Performance Optimization
# Response Generation
Asynchronous processing
Timeout management
Cache implementation
Response optimization
# Memory Management
Efficient storage
Quick retrieval
Automatic cleanup
Resource optimization
Future Enhancements
Model Integration

Additional model support
Enhanced model selection
Performance tracking
Response optimization
Memory System

Advanced analytics
Enhanced search
Pattern recognition
Knowledge base integration
Medical Features

Symptom tracking
Treatment monitoring
Condition analysis
Medical knowledge base
Development Guidelines
Code Structure

Modular design
Clear documentation
Type hints
Error handling
Testing

Unit tests
Integration tests
Performance testing
Security testing
Documentation

Code comments
API documentation
System documentation
User guides
Deployment
Requirements

Python 3.8+
Required packages
API keys
System resources
