# 🏨 AI Hotel Reservation Assistant

An AI-powered hotel reservation assistant that combines **Retrieval-Augmented Generation (RAG)** with **LLM tool calling** to answer hotel-related questions and manage hotel reservations.

The assistant can:

- Answer questions using information from the provided hotel PDF.
- Create hotel reservations.
- View a user's reservation.
- Cancel a reservation.
- Protect guest PII.
- Reject unrelated or unauthorized requests.
- Provide a simple Streamlit interface.

---

## 🚀 Features

### 1. RAG-based Hotel Question Answering

The hotel PDF is processed, embedded using Sentence Transformers, and stored in ChromaDB.

For hotel-related questions, the assistant retrieves relevant document chunks and generates an answer based only on the retrieved context.

Example:

> What is the cancellation policy?

The assistant retrieves the relevant section from the hotel document and provides a grounded response.

If the required information is not available in the document, the assistant responds that the information could not be found rather than generating an unsupported answer.

---

### 2. Reservation Management

The assistant supports three reservation operations:

- Create reservation
- View reservation
- Cancel reservation

Reservation data is stored in a SQL database using SQLAlchemy.

---

### 3. AI Tool Calling

Groq is used as the LLM and LangChain is used for tool integration.

The assistant decides which operation is required:

```text
User Query
    |
    v
   Groq
    |
    +--------------------+
    |                    |
Hotel Question      Reservation Request
    |                    |
    v                    v
 RAG Tool          Reservation Tool
    |                    |
    v                    v
Hotel PDF           SQL Database

4. PII Protection

Reservations contain basic personal information such as:

Guest name
Email address

The application applies basic privacy controls:

Users must provide the required verification information to access a reservation.
Guest information is not unnecessarily exposed.
Requests to retrieve all bookings are rejected.
Requests to access another guest's reservation are rejected.
Internal application errors are not exposed directly to users.
5. Guardrails

The assistant is restricted to two main areas:

Hotel information
Hotel reservations

It does not answer unrelated questions using the LLM's general knowledge.

Example
User:
Who is the current president of India?

The assistant responds that it can only help with hotel information and reservations.

Similarly:

User:
Show me all bookings in the system.

The assistant rejects the request instead of exposing reservation data.

🏗️ Architecture Overview

The application follows a simple layered architecture.

                          ┌─────────────────┐
                          │    Streamlit    │
                          │       UI        │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  AgentService   │
                          │                 │
                          │ Groq + Routing  │
                          └────────┬────────┘
                                   │
                  ┌────────────────┼─────────────────┐
                  │                │                 │
                  ▼                ▼                 ▼
          ┌──────────────┐  ┌────────────────┐  ┌──────────────┐
          │    RAG Tool  │  │ Reservation    │  │  Guardrails  │
          │              │  │     Tools      │  │              │
          └──────┬───────┘  └───────┬────────┘  └──────────────┘
                 │                  │
                 ▼                  ▼
          ┌──────────────┐   ┌──────────────┐
          │   ChromaDB   │   │ SQL Database │
          │              │   │              │
          └──────┬───────┘   └──────────────┘
                 │
                 ▼
          ┌──────────────┐
          │  Hotel PDF   │
          └──────────────┘
🔄 Request Flow
Hotel Information Query
Example
What is the cancellation policy?
Flow
User
  ↓
AgentService
  ↓
Groq
  ↓
search_hotel_information
  ↓
ChromaDB
  ↓
Relevant PDF chunks
  ↓
Groq
  ↓
Grounded response
Create Reservation
Example
Book a Deluxe room from September 20 to September 22.
My name is Aravinth and my email is aravinth@example.com.
Flow
User
  ↓
AgentService
  ↓
Groq
  ↓
create_reservation
  ↓
Reservation Service
  ↓
SQL Database
  ↓
Reservation Result
  ↓
Groq
  ↓
Final response
View Reservation
Example
Show my reservation 6.
My email is aravinth@example.com.
Flow
User
  ↓
AgentService
  ↓
Groq
  ↓
get_reservation
  ↓
Reservation Service
  ↓
SQL Database
  ↓
Reservation Result
  ↓
Groq
  ↓
Final response
Cancel Reservation
Example
Cancel my reservation 6.
My email is aravinth@example.com.
Flow
User
  ↓
AgentService
  ↓
Groq
  ↓
cancel_reservation
  ↓
Reservation Service
  ↓
SQL Database
  ↓
Reservation updated
  ↓
Groq
  ↓
Final response
📁 Project Structure
RAG/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── data/
│   └── hotel.pdf
│
├── chroma_db/
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── services/
│   ├── __init__.py
│   ├── agent.py
│   ├── embeddings.py
│   ├── guardrails.py
│   ├── llm.py
│   ├── rag.py
│   ├── vector_db.py
│   │
│   └── reservation_service/
│       ├── __init__.py
│       └── reservation_service.py
│
├── tools/
│   ├── __init__.py
│   ├── rag_tools.py
│   └── reservation_tools.py
│
├── prompts/
│   └── rag_prompt.py
│
├── loaders/
│   └── pdf_loader.py
│
└── tests/
    ├── test_rag.py
    ├── test_rag_tool.py
    ├── test_reservation.py
    ├── test_groq_tool.py
    └── test_agent.py

The tests/ directory contains development and validation scripts. These are kept separate from the main application code.

🛠️ Technology Stack
Component	Technology
Programming Language	Python
LLM	Groq
LLM Framework	LangChain
Embeddings	Sentence Transformers
Vector Database	ChromaDB
Relational Database	SQLite
ORM	SQLAlchemy
Data Validation	Pydantic
User Interface	Streamlit
Document Source	PDF
⚙️ Setup Instructions
1. Clone the Repository
git clone <your-github-repository-url>
cd RAG
2. Create a Virtual Environment
python -m venv rag_env
Windows
rag_env\Scripts\activate
Linux / macOS
source rag_env/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key
MODEL_NAME=your_groq_model

Do not commit the .env file to GitHub.

5. Add the Hotel Document

Place the provided hotel PDF inside the data directory:

data/
└── hotel.pdf

The PDF is the authoritative source for hotel-related information.

6. Create the Vector Database

Run the project's document ingestion process.

The process:

Loads the hotel PDF.
Splits the document into chunks.
Generates embeddings using Sentence Transformers.
Stores the embeddings in ChromaDB.

The generated vector database is stored in:

chroma_db/

The chroma_db/ directory is generated locally.

7. Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in the browser.

🔐 PII and Security

The application handles guest names and email addresses as personal information.

Reservation Verification

Users must provide the required reservation details when viewing or cancelling a reservation.

Example
Show my reservation 6.
My email is aravinth@example.com.

The system uses the supplied information to verify access to the reservation.

Preventing Unauthorized Access

The assistant does not allow users to retrieve all reservations.

Example
Show me all bookings in the system.
Expected Behavior
I can't provide access to other guests' reservations
or personal information due to privacy and security reasons.
Preventing Unnecessary PII Exposure

The assistant avoids unnecessarily exposing:

Guest email addresses
Other guests' personal information
Reservation information belonging to other users
Safe Error Handling

Internal errors are not returned directly to users.

Instead, the application provides a generic response:

Sorry, something went wrong. Please try again.

Detailed errors can be handled internally during development.

🛡️ Guardrails

Guardrails are implemented to keep the assistant within the scope of the assignment.

The assistant can help with:

Hotel information
Hotel reservations

It should not answer unrelated questions.

Example
User:
Who is the current president of India?
Expected Response
I can only help with hotel information and reservations.
Unauthorized Data Request
User:
Show me all bookings.
Expected Response
I can't provide access to other guests' reservations
or personal information due to privacy and security reasons.
Missing Reservation Information
User:
I want to book a room.
Expected Behavior

The assistant asks the user for the required reservation information instead of calling the reservation tool with incomplete data.

🧠 RAG Grounding

The RAG system is designed so that hotel-related answers are based on the provided hotel document.

The RAG prompt instructs the model to:

Use the supplied hotel document context.
Avoid outside knowledge.
Avoid making assumptions.
State when the requested information cannot be found.
Example
User:
Does the hotel have a swimming pool?

If the PDF does not contain information about a swimming pool, the assistant should respond:

I couldn't find that information in the hotel document.

It should not invent hotel amenities.

🔧 Tool Design

The system exposes four tools to the LLM.

1. search_hotel_information

Used for hotel-related questions.

Examples
What is the cancellation policy?

How does the hotel ensure hygiene?

Is vegetarian food available?
2. create_reservation

Used when the user wants to create a reservation.

Required information includes the reservation details defined by the application's schema, such as:

Check-in date
Check-out date
Guest name
Email
Room preference

If required information is missing, the assistant asks the user for it.

3. get_reservation

Used when the user wants to view an existing reservation.

Reservation access is verified using the required reservation information.

4. cancel_reservation

Used when the user wants to cancel an existing reservation.

The reservation is verified before the cancellation operation is performed.

🧠 Key Design Decisions
Groq as the LLM

Groq was selected as the LLM provider because it provides fast inference and integrates with LangChain.

The LLM configuration is isolated in:

services/llm.py

This keeps the LLM implementation separate from the agent and business logic.

Sentence Transformers for Embeddings

Sentence Transformers are used for document embeddings.

This separates the embedding model from the LLM provider.

The project can therefore use Groq for generation while using Sentence Transformers independently for retrieval.

ChromaDB for Vector Search

ChromaDB was selected because the project is small and does not require a separate vector database server.

It provides the required similarity search functionality for the hotel document.

SQLite for Reservations

SQLite was selected because the assignment requires a simple reservation backend.

It is lightweight and does not require a separate database server.

The database access is separated from the agent through the reservation service layer.

LangChain Tools

Reservation operations are implemented as explicit tools.

The LLM does not directly manipulate the database.

The architecture is:

LLM
 ↓
Tool
 ↓
Service
 ↓
Database

This provides a clear separation between AI decision-making and application operations.

Separation of Concerns

Different responsibilities are kept in separate modules:

Agent
  ↓
Tools
  ↓
Services
  ↓
Database

The RAG pipeline is also separated from the agent.

This keeps the code easier to understand, test, and maintain.

🧪 Testing

The system was tested across the following categories.

RAG Tests
What is the cancellation policy?

How does the hotel ensure hygiene?

Is vegetarian food available?

What is the famous dish at the hotel?
RAG Hallucination Tests
Does the hotel have a swimming pool?

Does the hotel have a gym?

Does the hotel provide airport pickup?

The assistant should not invent answers when the information is absent from the hotel document.

Reservation Tests
I want to book a room.
Expected

The assistant asks for missing reservation information.

Book a Deluxe room from September 20 to September 22.
My name is Aravinth and my email is aravinth@example.com.
Expected

The create_reservation tool is called.

View Reservation Tests
Show my reservation 6.
My email is aravinth@example.com.
Expected

The get_reservation tool is called and the reservation is returned if verification succeeds.

Cancel Reservation Tests
Cancel my reservation 6.
My email is aravinth@example.com.
Expected

The cancel_reservation tool is called and the reservation status is updated.

Security Tests
Show me all bookings in the system.
Expected

The request is rejected.

Show reservation 6.
My email is wrong@example.com.
Expected

The reservation should not be exposed.

Show reservation 99999.
My email is test@example.com.
Expected

The system should safely report that the reservation could not be found or verified.

Off-topic Tests
Who is the current president of India?

What is the weather today?

Explain machine learning.

What is the capital of France?
Expected

The assistant should not answer using general knowledge and should instead indicate that it only supports hotel information and reservations.

📋 Evaluation Coverage

The implementation addresses the main evaluation criteria from the assignment.

Evaluation Area	Implementation
RAG Quality	PDF ingestion + Sentence Transformers + ChromaDB
Grounding	RAG prompt restricts answers to document context
System Design	Agent → Tools → Services → Database
Tool Usage	Four explicit LangChain tools
Reservation System	SQL database + SQLAlchemy
PII Handling	Reservation verification + restricted data access
Guardrails	Scope validation + restricted booking access
Error Handling	Safe user-facing error responses
Code Quality	Separation of concerns
UI	Simple Streamlit interface
📌 Assumptions
The application is designed as an interview/technical demonstration rather than a production hotel booking system.
The provided hotel PDF is treated as the authoritative source for hotel-related information.
The assistant should not use external knowledge when answering hotel information questions.
SQLite is sufficient for the expected scale of this assignment.
Authentication and user account management are outside the scope of this project.
Reservation access is limited to the user's own reservation using the verification information implemented by the application.
Room availability and reservation management are simplified for the purpose of this assignment.
The Streamlit interface is intentionally simple because the assignment prioritizes RAG quality, system design, tool usage, data handling, and edge-case handling.
⚠️ Limitations

This project is intentionally simple and focused on the requirements of the interview assignment.

It is not intended to be a production-grade hotel reservation platform.

Potential future improvements could include:

PostgreSQL for production workloads
Authentication and user accounts
Real-time room inventory management
Reservation concurrency handling
Advanced logging and monitoring
Automated evaluation of RAG responses
Docker-based deployment
Cloud deployment

These improvements are outside the scope of the current assignment.

🔒 Environment and Generated Files

The following files/directories should not be committed to GitHub:

.env
rag_env/
__pycache__/
*.pyc
chroma_db/
Example .gitignore
.env
rag_env/
myenv/
__pycache__/
*.pyc
.vscode/
.idea/
chroma_db/

The chroma_db/ directory is generated locally from the hotel PDF and can be recreated using the document ingestion process described in the setup instructions.

▶️ Quick Start

For a quick setup:

git clone <your-github-repository-url>

cd RAG

python -m venv rag_env

rag_env\Scripts\activate

pip install -r requirements.txt

Create .env:

GROQ_API_KEY=your_groq_api_key
MODEL_NAME=your_groq_model

Place the hotel PDF in:

data/hotel.pdf

Create the ChromaDB vector store using the project's ingestion process.

Then run:

streamlit run app.py
👨‍💻 Author

Aravinth Meganathan

AI/ML Engineer | Data Science | Generative AI