import json
import urllib.request
import urllib.error

API_KEY = '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'
MODEL_NAME = 'gpt-5.6-terra'

prompt = """You are an expert evaluator of Bengali text summarization. Evaluate the generated summary against the source article using the following criteria, each scored from 1 (poor) to 5 (excellent):

- Relevance: Focuses on the key information and main event.
- Completeness: Covers the important information from the source.
- Faithfulness: Contains no unsupported, fabricated, or contradicted information.
- Coherence: Clear, logical, and well organized.
- Conciseness: Avoids unnecessary information and repetition.
- Fluency: Natural, grammatical, and readable Bengali.

Base your evaluation ONLY on the source article. Do not use external knowledge or assumptions. Penalize any information in the summary that is unsupported or contradicted by the source.

Return ONLY valid JSON in this format:
{
  "relevance": score,
  "completeness": score,
  "faithfulness": score,
  "coherence": score,
  "conciseness": score,
  "fluency": score
}

SOURCE:
টেস্ট সংবাদ নিবন্ধ

SUMMARY:
টেস্ট সারসংক্ষেপ"""

url = 'https://api.openai.com/v1/chat/completions'
headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
payload = {
    'model': MODEL_NAME,
    'messages': [{'role': 'user', 'content': prompt}],
    'max_completion_tokens': 300,
    'response_format': {'type': 'json_object'}
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print('RESPONSE:', resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTP ERROR:', e.code, e.read().decode('utf-8'))
except Exception as e:
    print('ERROR:', e)
