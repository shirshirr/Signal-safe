from ingest import load_news, load_prices
from embeddings import embed_texts
from vector_store import VectorStore
import pandas as pd

def run_replay(ticker='AAPL'):
    news = load_news()
    prices = load_prices()
    vs = VectorStore()
    
    news_t = news[news['ticker'] == ticker].sort_values('datetime')
    texts = (news_t['text'] + ' | source:' + news_t['source']).tolist()
    ids = [f"{ticker}_n_{i}" for i in range(len(texts))]
    vecs = embed_texts(texts)
    metas = [{'text': t, 'source': s, 'datetime': str(dt), 'ticker': ticker}
             for t, s, dt in zip(news_t['text'], news_t['source'], news_t['datetime'])]
    
    vs.upsert(ids, vecs, metas)
    
    unique_days = sorted(prices[prices['ticker'] == ticker]['date'].dt.date.unique())
    
    all_results = []  # List to collect all matches
    
    for day in unique_days:
        window_news = news_t[news_t['datetime'].dt.date <= day].tail(6)
        if window_news.empty:
            continue
        q_text = '\n'.join(window_news['text'].tolist())
        q_vec = embed_texts([q_text])[0]
        matches = vs.query(q_vec, top_k=5)
        
        for m in matches:
            meta = m['metadata']
            all_results.append({
                'Day': str(day),
                'Ticker': ticker,
                'ID': m['id'],
                'Score': m['score'],
                'Headline': meta.get('text') or '',
                'Source': meta.get('source') or ''
            })
    
    # Save results to CSV
    df = pd.DataFrame(all_results)
    df.to_csv(f'{ticker}_top_matches.csv', index=False)
    print(f"Results saved to {ticker}_top_matches.csv")

if __name__ == '__main__':
    run_replay('AAPL')
