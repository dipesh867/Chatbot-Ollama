from database import SessionLocal
from models.conversation import Conversation
from models.message import Message
from chatbot import get_chatbot_response


def update_summary_task(conv_id: int):
    db = SessionLocal()

    try:
        conv = db.query(Conversation).filter(
            Conversation.id == conv_id
        ).first()

        if not conv:
            return

        last_messages = db.query(Message).filter(
            Message.conversation_id == conv_id,
        ).order_by(Message.id.desc()).limit(10).all()

        last_messages = list(reversed(last_messages))

        user_inputs = "\n".join(
            f"- {m.content}" for m in last_messages
        )

        prompt = f"""
You are a text compression system.

Your job is ONLY to store user input history in a short memory format in: the user is talking about and include the compressed inputs given to you.


DO NOT answer the user.
DO NOT explain anything.
DO NOT act like an assistant.
DO NOT continue conversation.
Make sure to inlude all the content given.

RULES:
- Only summarize what the USER said across messages
- Ignore meaning, context, or correctness
- Do NOT respond to questions
- Do NOT generate new content
- Output ONLY compressed memory


eg:
if your input is :
input1: what is djagno 
response1: django is a python based framework good for bilding large webapps
input2: what is python
response 2:python is a programming language 
input3: what are top programming languages
response3: the top programming languages are python,js,node where thy offer diversity

then you should mave a summary as  :
the user was previously talking about django and got resposen that django is a pythonbased framweork best for large webapps and 
the user asked about python and got that it is aprogramming language  and then user asked top programming languages and got python,js,node.

so in this way include all the user questions in that pattern

USER MESSAGES:
{user_inputs}


"""
        print(user_inputs)
        new_summary = get_chatbot_response(prompt).strip()

        conv.summary = new_summary
        db.commit()
        print(new_summary)

    except Exception as e:
        print("SUMMARY ERROR:", e)

    finally:
        db.close()