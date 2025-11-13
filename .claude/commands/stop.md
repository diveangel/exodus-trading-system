---
description: Stop both backend and frontend servers
---

# Stop Servers

Execute the stop-servers.sh script to stop both the backend and frontend servers.

```bash
chmod +x stop-servers.sh && ./stop-servers.sh
```

This will:
1. Stop the backend server running on port 8000
2. Stop the frontend server running on ports 3000/3001
3. Clean up all related processes
