
# SHL Assessment Recommendation System

A full-stack web application that recommends the most relevant SHL assessments based on a user’s natural language job description query.

🚀 **Live Demo:** [https://delightful-malabi-2819e6.netlify.app/](https://delightful-malabi-2819e6.netlify.app/)

---

## 📌 Features

- 🔍 **Scraper**: Uses Selenium and BeautifulSoup to scrape SHL’s product catalog.
- 🧠 **Recommender API**: Built with FastAPI, it processes the query and returns recommended assessments.
- 🌐 **Frontend**: Responsive and user-friendly web interface for submitting queries and viewing results.
- ☁️ **Deployed**: Frontend on Netlify and backend API hosted via Render.

---

## 📁 Project Structure

```
shl-assessment-recommender/
│
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── recommender.py          # Recommender logic using embeddings
│   └── requirements.txt
│
├── scraper/
│   ├── scrape.py               # Selenium + BeautifulSoup scraper
│   └── embed.py                # Helper functions for data cleaning/storage
│
├── frontend/
│   ├── index.html              # Main HTML page
│   ├── script.js               # Handles form submission and rendering
│   └── styles.css              # Styling
│
├── README.md                   # This file
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/shl-assessment-recommender.git
cd shl-assessment-recommender
```

---

### 2. Scraping SHL Assessments

```bash
cd scraper
pip install -r requirements.txt
python scrape.py
```

This script will extract the assessment descriptions, metadata, and URLs from the SHL site and save them into a usable format (e.g., CSV or JSON).

---

### 3. Start FastAPI Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

- The API will be available at: `http://127.0.0.1:8000`
- Endpoint: `/api/v1/recommend?query=Java developer`

---

### 4. Run the Frontend Locally

You can use any static server. Here’s one using Python:

```bash
cd frontend
python -m http.server 8000
```

Now, open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🌐 Deployment

### Frontend (Netlify)

1. Push the `frontend/` folder to a GitHub repo.
2. Connect the repo to [Netlify](https://www.netlify.com/).
3. Set the build folder to `frontend`.

✅ Deployed: [https://delightful-malabi-2819e6.netlify.app/](https://delightful-malabi-2819e6.netlify.app/)

---

### Backend (Render)

1. Push `backend/` to a separate GitHub repo (or same).
2. Create a new Web Service on [Render](https://render.com/).
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add CORS settings in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔍 Example Query

Try: **"Java developer with knowledge of Spring Boot and REST APIs"**

Expected output: SHL tests related to Java, backend, and programming skills.

---

## 🧠 Technologies Used

- **Backend**: FastAPI, Sentence Transformers
- **Scraping**: Selenium, BeautifulSoup
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Netlify, Render

---

## 🧑‍💻 Author

- **Name**: Junaid Ul Islam
- **LinkedIn**: [LinkedIn](https://www.linkedin.com/in/junaid-ul-islam-b06874255/)
- **GitHub**: [Github](https://github.com/desmondvidic)

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
