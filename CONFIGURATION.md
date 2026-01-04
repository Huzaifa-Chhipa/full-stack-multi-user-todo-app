# Configuration for Hugging Face Space Backend

To connect the frontend to your Hugging Face Space backend, you need to update the environment configuration.

## Setup

1. Create a `.env.local` file in the `frontend` directory with the following content:

```env
NEXT_PUBLIC_API_URL=https://huzaifachhipa-todo-backend.hf.space
```

2. The backend should already have permissive CORS settings to allow connections from the frontend.

## Important Notes

- The `.env.local` file is in `.gitignore` and should NOT be committed to the repository for security reasons
- The `NEXT_PUBLIC_API_URL` environment variable is used by the frontend to connect to the backend API
- Your Hugging Face Space URL: `https://huzaifachhipa-todo-backend.hf.space`