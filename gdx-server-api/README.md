# 🚀 GDX APPLICATION

This is a **backend boilerplate** for gdx application project built for APIs and **Alembic** for database migrations.  

It provides a clean structure to:  
- Manage database models and schemas.  
- Run migrations easily using Alembic.  
- Serve APIs efficiently with FastAPI and Uvicorn.  
- Scale for production with async database support.  

---

## ⚙️ Setup & Run Instructions

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create a new Alembic revision
```bash
alembic revision --autogenerate -m "init tables"
```

### Step 3: Apply migrations
```bash
alembic upgrade head
```

### Step 4: Run the FastAPI application
```bash
uvicorn app.main:app --reload
```

---

✅ App will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
📖 API docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
