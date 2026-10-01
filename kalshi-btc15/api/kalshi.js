export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store, max-age=0');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'GET only' });

  const mode = String(req.query.mode || 'active');
  const ticker = req.query.ticker ? String(req.query.ticker) : '';
  const base = 'https://external-api.kalshi.com/trade-api/v2';

  try {
    let url;
    if (mode === 'market' && ticker) {
      if (!/^KXBTC15M/i.test(ticker)) return res.status(400).json({ error: 'Unsupported ticker' });
      url = base + '/markets/' + encodeURIComponent(ticker);
    } else {
      url = base + '/markets?series_ticker=KXBTC15M&status=open&limit=50';
    }

    const r = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'KalshiBTC15PaperBot/1.0'
      },
      cache: 'no-store'
    });

    const text = await r.text();
    if (!r.ok) {
      return res.status(r.status).json({
        error: 'Kalshi upstream error',
        status: r.status,
        body: text.slice(0, 500)
      });
    }

    res.status(200);
    res.setHeader('Content-Type', 'application/json');
    res.send(text);
  } catch (e) {
    res.status(502).json({ error: 'Kalshi relay failed', detail: String(e?.message || e) });
  }
}
