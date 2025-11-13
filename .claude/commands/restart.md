---
description: Restart both backend and frontend servers
---

# Restart Servers

Execute the restart-servers.sh script to restart both the backend and frontend servers.

```bash
chmod +x restart-servers.sh && ./restart-servers.sh
```

This will:
1. Stop the backend server (port 8000)
2. Stop the frontend server (ports 3000/3001)
3. Start the backend server
4. Start the frontend server

After execution, display the server URLs:
- Backend: http://localhost:8000
- Frontend: http://localhost:3001
- API Docs: http://localhost:8000/docs
