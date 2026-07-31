# Brand DNA Extractor

Brand DNA Extractor is an advanced, AI-driven platform designed to streamline brand analysis and visual identity extraction for agencies, marketers, and developers. By simply inputting a company's website URL, the application autonomously scrapes and synthesizes deep structural data—including typography, color palettes, CSS variables, and strategic metadata. 

Powered by Google Gemini and a robust FastAPI backend, the system acts as a virtual senior brand strategist. It interprets raw web structure into a cohesive "Brand DNA" profile, articulating the brand's core values, target audience, personality, and tone of voice. The results are elegantly displayed within a modern, glassmorphic Next.js dashboard, providing teams with immediate strategic insights. 

To bridge the gap between analysis and presentation, the platform features an automated export pipeline that transforms the extracted data into ultra-premium, agency-quality PDF reports using ReportLab, ensuring that high-fidelity brand guidelines are always just one click away.

## 🚀 Features

- **Automated Brand Scraper**: Asynchronously scrapes any website to intelligently extract raw brand data, including CSS variables, typography, headers, and meta descriptions.
- **AI Brand Strategist**: Utilizes Google Gemini to process the raw scraped data and synthesize a comprehensive "Brand DNA" profile (Tone of Voice, Core Values, Target Audience, Brand Personality, and Color Palette).
- **Beautiful Dashboard**: A modern, glassmorphic UI to view and manage all extracted brand identities.
- **Premium PDF Export**: Generates ultra-premium, agency-quality PDF reports of the extracted Brand DNA (powered by ReportLab), complete with dynamically rendered color swatches and typography.

---

## 🛠️ Tech Stack

**Frontend (`/client`)**
- Next.js (App Router)
- React 19
- Tailwind CSS v4
- `shadcn/ui` + Lucide Icons
- Axios

**Backend (`/server`)**
- Python 3.14+
- FastAPI (with standard uvicorn ASGI server)
- `uv` (Fast Python Package Installer & Resolver)
- BeautifulSoup4 & httpx (Web Scraping)
- Google GenAI SDK (Gemini)
- ReportLab (PDF Generation)
- SQLModel / SQLAlchemy (SQLite Database ORM)

---

## 📦 Getting Started

### 1. Backend Setup

Ensure you have [uv](https://github.com/astral-sh/uv) installed to manage the Python environment.

```bash
cd server

# Install dependencies and setup virtual environment
uv sync

# Create a .env file and add your Gemini API Key
echo 'GEMINI_API_KEY="your_api_key_here"' > .env

# Run the development server
uv run uvicorn app.main:app --reload
```
The FastAPI server will typically run on `http://localhost:8000`. You can visit `http://localhost:8000/docs` for the API documentation.

### 2. Frontend Setup

Make sure you have Node.js 20+ installed.

```bash
cd client

# Install dependencies
npm install

# Run the Next.js development server
npm run dev
```
The web app will run on `http://localhost:3000`.

---

## 🏗️ Project Structure

```text
├── client/                 # Next.js frontend application
│   ├── app/                # App router (pages, layouts)
│   ├── components/         # Reusable UI components (shadcn, brand cards)
│   └── package.json        # Frontend dependencies
│
├── server/                 # FastAPI backend application
│   ├── app/
│   │   ├── core/           # Scraping logic, AI Agent integration, PDF generation
│   │   ├── brands/         # Brand DNA routes and controllers
│   │   ├── users/          # Authentication & credit system
│   │   └── models/         # SQLModel database schemas
│   ├── brand_dna.db        # SQLite database
│   └── pyproject.toml      # uv / pip dependencies
│
└── README.md
```

## 🎨 Design Principles
This project uses modern web design patterns:
- **Glassmorphism & Dark Mode**: Used heavily in the dashboard interfaces for a premium aesthetic.
- **Clean Minimalism**: The exported PDFs follow a strict, high-end agency deck layout with mathematically perfect typographic leading and grid-aligned color swatches.
