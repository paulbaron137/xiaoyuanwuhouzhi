// Vercel Serverless Function: AI 识鸟代理
// DeepSeek API Key 存于 Vercel 环境变量 DEEPSEEK_API_KEY（密文存储），不进前端代码
module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method Not Allowed' });
    return;
  }
  const KEY = process.env.DEEPSEEK_API_KEY;
  if (!KEY) {
    res.status(500).json({ error: '服务端未配置 DEEPSEEK_API_KEY（请在 Vercel 项目的 Settings > Environment Variables 中添加）' });
    return;
  }
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY },
      body: JSON.stringify(body),
    });
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (err) {
    res.status(502).json({ error: '转发失败: ' + (err.message || err) });
  }
};
