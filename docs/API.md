# API

## Health

- `GET /health`

## Documents

- `POST /api/documents/preview`
  - Multipart field: `file`
  - Returns file preview, encoding, and byte size

## Knowledge Base

- `GET /api/knowledge/stats`
- `POST /api/knowledge/upload`
  - Multipart field: `file`
  - Optional form field: `operator`

## Chat

- `POST /api/chat`
  - JSON body:

```json
{
  "question": "春天穿什么颜色的衣服？",
  "session_id": "user_001"
}
```

