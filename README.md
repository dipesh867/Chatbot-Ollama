AI Chatbot using FastAPI + Ollama

*Overview:

This project is a full-stack AI chatbot system built with a modern architecture that combines a responsive frontend and a powerful backend powered by local LLMs via Ollama. The system is designed to support real-time conversations, persistent chat history, and contextual memory using conversation summarization.

Key Features:
-  User authentication (Login & Register system)
-  Real-time chat interface
-  Conversation history management
-  Context-aware responses using conversation summaries
-  Local AI inference using Ollama
-  Continuous context update after every user interaction
-  Persistent storage of chats and summaries

Tech Stack:

*Frontend
-  Built using a modern frontend framework (designed with Claude assistance)
-  Authentication UI (Login/Register)
-  Chat interface with message input
-  Sidebar for chat history

*Backend
-  FastAPI for high-performance API development
-  SQLAlchemy for ORM-based database handling
-  RESTful architecture

*AI Model
-  Ollama
-  Model used: qwen2.5-coder:3b

*Database Design

- The system is built around three main schemas:
1. User: Stores user credentials and authentication data.

2. Conversation: Handles chat sessions and metadata:
-   Conversation title
-   User association
-   Conversation summary (context memory)

3. Message: Stores individual messages:
-   User messages
-   AI responses
-   Linked to a conversation

*Context & Memory System:
One of the core features of this chatbot is its lightweight memory system which works as follows:

-  The last 5 messages of a conversation are used for context.
-  After each AI response, a summary is generated using the chatbot itself.
-  This summary is stored in the Conversation model using those last 5 messages.
-  The summary acts as long-term memory for future interactions.

This allows the system to maintain contextual awareness without storing full conversation history in active memory.

*Chat Flow Architecture:

-  User sends a message
-  Backend receives request via FastAPI
-  The sumary off last 5 conversation is retrived
-  Context is sent to Ollama (qwen2.5-coder:3b)
-  Model generates response
-  Response is returned to frontend
-  Message is stored in database
-  Conversation summary is updated using a chatbot after every interaction

*Performance Notes:

-  The system runs completely locally
-  No API cost or external dependency
-  Supports unlimited usage
-  Performance is dependent on local hardware (CPU/GPU)

Due to local model execution, response time may vary depending on system specifications.

*Project Highlights:

-  Fully local AI chatbot Scalable 
-  backend architecture using FastAPI
-  Persistent memory system using summarization
-  Clean separation of frontend and backend
-  Optimized for real-world chatbot behavior

*Conclusion

This project demonstrates how a fully local AI chatbot can be built using modern web technologies. By combining FastAPI, structured database design, and Ollama’s local LLM capabilities, the system achieves a balance between performance, privacy, and scalability.