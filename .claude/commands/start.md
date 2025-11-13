---
description: Start both backend and frontend servers
---

# Start Servers

Start both the backend and frontend servers in the background.

## Backend Server
```bash
cd backend && source venv/bin/activate && nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 & echo $!
```

## Frontend Server
```bash
cd frontend && nohup npm run dev > frontend.log 2>&1 & echo $!
```

After execution, display the server URLs:
- Backend: http://localhost:8000
- Frontend: http://localhost:3001
- API Docs: http://localhost:8000/docs

Wait a few seconds for the servers to fully start up, then verify they are running on the expected ports.
