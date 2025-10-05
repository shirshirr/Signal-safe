import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def llm_generate(prompt):
    if not OPENAI_KEY:
        raise RuntimeError('LLM requires OPENAI_API_KEY')
    import openai
    openai.api_key = OPENAI_KEY
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role':'system','content':'You are a financial alerts assistant.'},
                  {'role':'user','content':prompt}],
        max_tokens=400,
        temperature=0.0
    )
    return resp['choices'][0]['message']['content'].strip()

def make_alert_for_ticker(ticker, query_vector, vector_store):
    matches = vector_store.query(query_vector, top_k=6)
    evidence_texts = []
    for m in matches:
        meta = m.get('metadata', {})
        txt = meta.get('text') or 'no-text'
        evidence_texts.append(f"- {meta.get('source')} | {meta.get('datetime')}: {txt[:200]}...")
    prompt = f"Evidence for {ticker}:\n" + "\n".join(evidence_texts) + "\n\nAnswer in JSON with fields: type, confidence, summary, why"
    return llm_generate(prompt)

