# Project 7 — Customer Refund Request Classifier

![Level](https://img.shields.io/badge/Level-Beginner-green)
![Industry](https://img.shields.io/badge/Industry-E--commerce-teal)
![Stack](https://img.shields.io/badge/Stack-Google%20Gemini%20%7C%20Gmail%20API%20%7C%20Streamlit-blue)
![AI](https://img.shields.io/badge/AI-Hybrid%20ML%20%2B%20LLM-purple)

---

# Business Problem

E-commerce support teams receive thousands of refund, return, and complaint emails every week.

Manual email triage requires agents to read every email, identify the request type, determine urgency, and decide the next action.

At scale:

- 2,000 support emails/day
- Average triage time: 60 seconds/email
- Agent cost: $0.05/minute

Reducing manual classification time can save significant operational cost while improving customer response time.

---

# Project Objective

Build an AI-powered customer support email classification system that:

✅ Reads customer emails from Gmail using Gmail API  
✅ Extracts email metadata and content  
✅ Classifies emails by request type and urgency  
✅ Uses Machine Learning for fast classification  
✅ Uses Google Gemini LLM for intelligent fallback classification  
✅ Generates structured JSON responses  
✅ Exports classified emails into CSV  
✅ Applies Gmail labels automatically  
✅ Provides a Streamlit dashboard for support teams  

---

# AI Classification Approach

This project uses a **Hybrid AI Classification Architecture**.

Instead of depending on a single model, the system combines traditional Machine Learning with Generative AI.

## Classification Flow

             Gmail Inbox
                  |
                  |
          Gmail API OAuth2
                  |
                  |
          Email Extraction
                  |
                  |
      -------------------------
      |                       |
      |                       |

ML Classifier Gemini LLM
(Fast Prediction) (Smart Reasoning)
| |
| |
TF-IDF + Logistic Google Gemini Model
Regression JSON Classification
|
|
Confidence Check
|
|
High Confidence?
|
Yes -------> Return ML Result
|
No
|
v
Gemini Classification


---

# Why Hybrid AI?

Traditional ML models are fast and inexpensive but have limitations.

## Machine Learning Models Used

### TF-IDF + Logistic Regression

Advantages:

- Fast inference
- Lightweight
- Works well with structured training data
- No API cost

Limitations:

- Does not understand context
- Cannot reason about customer intent
- Struggles with new email formats
- Sensitive to vocabulary changes


Example:


"I am disappointed. The item arrived broken and I need my money back."


A TF-IDF model only sees keywords:


broken
money
back
item


It does not truly understand:


Customer wants refund because product arrived damaged


---

## Word2Vec Experiment

Word2Vec embeddings were also tested.

Advantages:

- Understands semantic similarity better than TF-IDF
- Converts words into numerical vectors

Limitations:

- Requires good training data
- Sentence meaning is limited
- Does not understand full email context
- Gmail emails contain highly variable language

For real-world Gmail classification, Word2Vec alone did not provide enough accuracy.

---

## Google Gemini LLM

Gemini is used as an intelligent fallback classifier.

Advantages:

- Understands customer intent
- Handles new email patterns
- Understands context
- Provides explanations
- Generates structured JSON output

Example:

Input:


Subject:
My order never arrived

Body:
I placed an order three weeks ago. Tracking has not updated.
If this is not fixed I will contact my bank.


Gemini understands:

```json
{
 "request_type":"Refund",
 "urgency":"critical",
 "chargeback_risk":true,
 "suggested_action":"escalate_to_manager"
}
System Architecture
Key Features
1. Gmail Integration

The application connects to Gmail using:

Gmail API
OAuth2 authentication
Secure token management

Capabilities:

Fetch unread emails
Extract sender information
Extract subject
Extract email body
Apply labels automatically
2. AI Email Classification

Each email is classified into:

Request Type
Refund
Return
Exchange
Complaint
Other
Urgency
Critical
High
Medium
Low
Suggested Action
Issue Refund
Process Return
Send Replacement
Escalate Manager
Standard Reply
Flag Review
Risk Detection
Chargeback Risk
Legal Threat
Customer Escalation
3. Structured AI Output

The system forces AI responses into JSON format.

Example:

{
 "request_type":"Refund",
 "urgency":"high",
 "one_line_summary":"Customer requests refund for delayed order",
 "suggested_action":"issue_refund",
 "chargeback_risk":false
}

Benefits:

Easy database storage
Easy CSV export
Easy dashboard visualization
Reliable automation
Folder Structure
Customer-Refund-Request-classification/

├── src/
│
│   ├── classifier.py
│   │       Main application flow
│   │
│   ├── hybrid_classifier.py
│   │       ML + Gemini decision logic
│   │
│   ├── gemini_classifier.py
│   │       Google Gemini integration
│   │
│   ├── gmail_client.py
│   │       Gmail API OAuth2 handling
│   │
│   ├── dashboard.py
│   │       Streamlit dashboard
│   │
│   ├── ML/
│   │
│   │   ├── train.py
│   │   ├── predictor.py
│   │   ├── classifier.pkl
│   │   ├── tfidf.pkl
│   │   ├── word2vec.pkl
│   │   └── word2vec_classifier.pkl
│
├── tests/
│   └── test_classifier.py
│
├── samples/
│   └── sample_emails.json
│
├── output/
│   └── classified_emails.csv
│
├── credentials.json
├── token.json
├── .env
├── .env.example
├── requirements.txt
└── README.md
# Technology Stack

## Programming Language

- Python 3.x

## AI / Machine Learning

- Google Gemini API
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- Word2Vec Embeddings

## Email Integration

- Gmail API
- Google OAuth2 Authentication

## Data Processing

- Pandas
- JSON
- CSV

## Dashboard

- Streamlit

## Testing

- Pytest


---

# Project Setup

## 1. Clone Repository

```bash
git clone <your-repository-url>

cd Customer-Refund-Request-classification
2. Create Virtual Environment

Mac/Linux:

python3 -m venv venv

source venv/bin/activate

Windows:

python -m venv venv

venv\Scripts\activate

A virtual environment keeps project dependencies isolated.

Install Dependencies

Install required packages:

pip install -r requirements.txt

Example requirements:

google-generativeai>=0.8.0
google-auth>=2.29.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.125.0

scikit-learn>=1.4.0
gensim>=4.3.0

pandas>=2.0.0

streamlit>=1.35.0

python-dotenv>=1.0.0

pytest>=8.0.0
Environment Configuration

Create .env file:

GEMINI_API_KEY=your_google_gemini_api_key

Example:

GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxx

The API key is generated from:

Google AI Studio:

https://aistudio.google.com/

Never commit .env into GitHub.

Add this to .gitignore:

.env
credentials.json
token.json
*.pkl
__pycache__/
venv/
output/
Gmail API Setup

This project uses Gmail API to read and modify emails.

Step 1: Create Google Cloud Project

Go to:

https://console.cloud.google.com

Create a new project:

Example:

CustomerRefundClassifier
Step 2: Enable Gmail API

Navigate:

APIs & Services
        |
        |
     Library
        |
        |
    Gmail API
        |
        |
     Enable
Step 3: Configure OAuth Consent Screen

Navigate:

APIs & Services
        |
OAuth Consent Screen

Select:

External

Add:

Application name:

Customer Refund Classifier

Add your Gmail account as a test user.

Step 4: Create OAuth Credentials

Navigate:

APIs & Services

        |

Credentials

        |

Create Credentials

        |

OAuth Client ID

Select:

Desktop Application

Download:

credentials.json

Place it in:

Customer-Refund-Request-classification/
Running the Application
Step 1: Train Machine Learning Models

Train TF-IDF classifier:

python src/ML/train.py

This generates:

src/ML/

classifier.pkl

tfidf.pkl
Step 2: Train Word2Vec Model

Run:

python src/ML/train_word2vec.py

This generates:

src/ML/

word2vec.pkl

word2vec_classifier.pkl
Step 3: Run Gmail Classifier
python src/classifier.py

First execution:

Browser opens
Google authentication required
User grants Gmail permission

After successful login:

token.json

is created.

Future executions reuse this token.

Classification Flow

Example:

Incoming Gmail:

From:
customer@gmail.com

Subject:
Refund needed immediately

Body:
My order arrived damaged.
I want my money back.
Step 1: ML Prediction

TF-IDF model generates:

{
"request_type":"Refund",
"confidence":0.72
}
Step 2: Confidence Check

Example:

CONFIDENCE_THRESHOLD = 0.90

If:

confidence >= 0.90

Return ML result.

If:

confidence < 0.90

Send email to Gemini.

Step 3: Gemini Classification

Gemini receives:

Subject + Email Body

Returns:

{
"request_type":"Refund",
"urgency":"high",
"one_line_summary":"Damaged product refund request",
"suggested_action":"issue_refund",
"chargeback_risk":false
}
Hybrid Classifier Logic

Example:

def classify_email(email):

    ml_result = predict_request_type(email)


    if ml_result["confidence"] >= 0.90:

        return ml_result


    else:

        return classify_email_with_gemini(email)
Gmail Label Automation

The application creates Gmail labels:

Example:

Refund-Critical

Refund-High

Refund-Medium

Refund-Low

Example:

Customer email:

Threatening chargeback

Gets label:

Refund-Critical
CSV Output

Every run generates:

output/classified_20260710.csv

Example:

Email	Type	Urgency	Action
customer1@gmail.com	Refund	High	Issue Refund
customer2@gmail.com	Complaint	Critical	Escalate
customer3@gmail.com	Return	Medium	Process Return
Streamlit Dashboard

Start dashboard:

streamlit run src/dashboard.py

Dashboard provides:

Total emails processed
Urgency statistics
Refund count
Complaint count
Chargeback risks
Filter options
CSV download

Example:

---------------------------------

Critical       High       Medium

  5             12          35


---------------------------------

Email Table


Sender
Subject
Category
Urgency
Action

---------------------------------
Testing

Run:

pytest tests/test_classifier.py -v

Tests cover:

Classification output
JSON validation
ML prediction
Error handling

# Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named config` | Python path issue | Run from project root or add `src` to Python path |
| `FileNotFoundError: credentials.json` | Gmail OAuth file missing | Download OAuth credentials from Google Cloud Console |
| `403 access_denied` during Gmail login | Gmail account not added as test user | Add your Gmail account under OAuth Consent Screen test users |
| `GEMINI_API_KEY missing` | Environment variable not loaded | Check `.env` file and call `load_dotenv()` |
| `401 Unauthorized Gemini API` | Invalid API key | Generate a new key from Google AI Studio |
| `token.json authentication error` | Expired OAuth token | Delete `token.json` and authenticate again |
| Dashboard shows no data | Classifier has not generated CSV | Run `python src/classifier.py` first |
| ML confidence always low | Training data does not represent real emails | Use Gemini fallback or improve dataset |
| Word2Vec accuracy is low | Limited training examples | Increase domain-specific training data |


---

# Machine Learning Model Performance Notes

During development, multiple approaches were evaluated.

## TF-IDF + Logistic Regression

Used as the primary lightweight classifier.

Advantages:

✅ Fast  
✅ Low resource usage  
✅ Easy deployment  
✅ Good baseline accuracy  


Challenges:

❌ Limited understanding of intent  
❌ Depends heavily on keywords  
❌ Struggles with new customer language  


---

## Word2Vec Classifier

Tested as an improvement over TF-IDF.

Advantages:

✅ Captures word relationships  
✅ Better semantic representation  


Challenges:

❌ Requires more training data  
❌ Does not understand complete email context  
❌ Customer emails contain many unseen phrases  


For Gmail-based customer support emails, Word2Vec alone was not sufficient.


---

## Gemini LLM Classification

Used for complex cases.

Advantages:

✅ Understands context  
✅ Handles unseen email patterns  
✅ Detects customer emotion  
✅ Detects escalation risk  
✅ Produces structured responses  


The final architecture combines:


Fast ML Prediction
+
LLM Reasoning
=
Production Hybrid AI System


---

# Security Considerations

## Protected Files

The following files should never be committed:


.env

credentials.json

token.json

*.pkl


These may contain:

- API keys
- OAuth credentials
- Authentication tokens
- Machine learning models


---

# Production Improvements

Future production enhancements:

## 1. Database Storage

Replace CSV storage with:

- PostgreSQL
- MongoDB
- Firebase


Benefits:

- Search capability
- Historical analytics
- Multi-user support


---

## 2. Email Reply Generation

Use Gemini to automatically draft responses.

Example:

Customer:


My package never arrived.


AI Draft:


Hello John,

We apologize for the delay.
We have started an investigation and will update you within 24 hours.

Thank you.


---

## 3. Human-in-the-loop Review

For high-risk emails:


Customer threatens legal action
|
|
Gemini Detection
|
|
Human Approval
|
|
Send Response


---

## 4. Vector Database Integration

Store email embeddings using:

- FAISS
- ChromaDB
- Pinecone


Benefits:

- Similar email search
- Knowledge retrieval
- Faster customer support


---

## 5. RAG Architecture

Future architecture:


Customer Email

   |

Embedding Creation

   |

Vector Database

   |

Retrieve Company Policies

   |

Gemini LLM

   |

Accurate Response


---

## 6. Agentic AI Support Agent

Future version:

AI Agent can:

- Read email
- Classify request
- Check order database
- Validate refund policy
- Create refund ticket
- Reply to customer
- Update CRM


---

# Project Learnings

Through this project, the following AI engineering concepts were implemented:

## Generative AI

- Prompt engineering
- Structured JSON output
- Gemini API integration
- LLM-based classification


## Machine Learning

- Text preprocessing
- TF-IDF vectorization
- Logistic Regression
- Word embeddings
- Model evaluation


## NLP

- Text classification
- Semantic similarity
- Feature extraction
- Intent detection


## Cloud APIs

- Gmail API
- OAuth2 authentication
- Secure API integration


## Software Engineering

- Modular Python architecture
- Environment configuration
- Error handling
- Automated testing
- Dashboard development


---

# Resume Project Description

## Customer Refund Request Classifier — AI Email Automation Platform

Built an AI-powered customer support automation system using Python, Gmail API, Google Gemini, and Machine Learning.

Implemented a hybrid classification architecture combining TF-IDF/Logistic Regression models with Gemini LLM fallback for intelligent email understanding.

Developed an automated pipeline that:

- Fetches customer emails using Gmail API OAuth2
- Classifies requests into refund, return, exchange, complaint categories
- Detects urgency and chargeback risk
- Generates structured JSON responses
- Applies Gmail labels automatically
- Exports analytics data
- Provides a Streamlit dashboard


Technologies:


Python
Google Gemini API
Gmail API
Scikit-learn
TF-IDF
Word2Vec
Pandas
Streamlit
OAuth2


---

# Time Estimate

| Mode | Time |
|---|---|
| Beginner Implementation | 12–16 hours |
| AI Developer Implementation | 6–10 hours |
| Production Version | Multiple weeks |


---

# Conclusion

This project demonstrates a practical enterprise AI workflow:


Real Customer Emails

    |

Data Extraction

    |

Machine Learning Classification

    |

Generative AI Reasoning

    |

Automation

    |

Business Dashboard


It combines traditional Machine Learning and modern Generative AI techniques to solve a real customer support automation problem.
