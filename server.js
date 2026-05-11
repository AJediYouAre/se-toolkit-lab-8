const express = require('express');
const app = express();
const PORT = parseInt(process.env.PORT || '8080', 10);

app.use(express.json({ limit: '10mb' }));

// Map internal model names to OpenRouter model IDs
// All map to owl-alpha (free on OpenRouter) to avoid credit requirements
const MODEL_MAP = {
  'qwen3-coder-plus': 'openrouter/owl-alpha',
  'qwen3-coder-flash': 'openrouter/owl-alpha',
  'coder-model': 'openrouter/owl-alpha',
  'vision-model': 'openrouter/owl-alpha',
};

function resolveModel(model) {
  return MODEL_MAP[model] || model;
}

// Health check
app.get('/', (req, res) => res.json({ status: 'ok' }));

// List models
app.get('/v1/models', (req, res) => {
  res.json({
    object: 'list',
    data: [
      { id: 'qwen3-coder-plus', object: 'model', created: 1754686206, owned_by: 'qwen' },
      { id: 'qwen3-coder-flash', object: 'model', created: 1754686206, owned_by: 'qwen' },
      { id: 'coder-model', object: 'model', created: 1754686206, owned_by: 'qwen' },
      { id: 'vision-model', object: 'model', created: 1754686206, owned_by: 'qwen' },
    ]
  });
});

// Chat completions - proxy to OpenRouter
app.post('/v1/chat/completions', async (req, res) => {
  const apiKey = process.env.OPENAI_API_KEY || '';
  const requestedModel = req.body.model || 'coder-model';
  const model = resolveModel(requestedModel);
  const isStream = req.body.stream === true;

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com/inno-se-toolkit/se-toolkit-lab-7',
        'X-Title': 'SE Toolkit Lab 7 Bot',
      },
      body: JSON.stringify({
        model: model,
        messages: req.body.messages,
        temperature: req.body.temperature ?? 0.7,
        max_tokens: req.body.max_tokens ?? 4096,
        top_p: req.body.top_p,
        tools: req.body.tools,
        tool_choice: req.body.tool_choice,
        stream: isStream,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`OpenRouter error: ${response.status} ${errText}`);
      // Return a valid fallback response
      if (isStream) {
        res.setHeader('Content-Type', 'text/event-stream');
        res.write(`data: ${JSON.stringify({ choices: [{ delta: { content: 'LLM unavailable - using fallback' }, finish_reason: 'stop' }] })}\n\n`);
        res.write('data: [DONE]\n\n');
        return res.end();
      }
      return res.status(200).json({
        id: 'fallback',
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model: requestedModel,
        choices: [{
          index: 0,
          message: { role: 'assistant', content: 'Service temporarily unavailable. Please check LLM configuration.' },
          finish_reason: 'stop',
        }],
        usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
      });
    }

    if (isStream) {
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      const reader = response.body;
      reader.on('data', (chunk) => { res.write(chunk); });
      reader.on('end', () => res.end());
      reader.on('error', (err) => { console.error('Stream error:', err); res.end(); });
    } else {
      const data = await response.json();
      if (data.model) data.model = requestedModel;
      res.json(data);
    }
  } catch (error) {
    console.error('Proxy error:', error.message);
    if (isStream) {
      res.write('data: [DONE]\n\n');
      return res.end();
    }
    res.status(200).json({
      id: 'error-fallback',
      object: 'chat.completion',
      created: Math.floor(Date.now() / 1000),
      model: requestedModel,
      choices: [{
        index: 0,
        message: { role: 'assistant', content: 'Service temporarily unavailable.' },
        finish_reason: 'stop',
      }],
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
    });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`LLM proxy running on port ${PORT}`);
});
