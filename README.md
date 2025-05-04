# 💵 KnockBank

<span style="margin-top: 4px">

![KnockBankLogo](./.github/assets/knock_bank_logo.svg)

</span>
</div>

KnockBank is a modern full stack banking platform that allows its users to deposit, withdrawal and transfer values to other accounts on the platform, also providing a graphic visualization of total inflows and outflows by month of the current year.

⸻

## ⚙️ Tech Stack

| Layer      | Tech                              |
|------------|-----------------------------------|
| Backend    | Python, APIFlask, SQLAlchemy                 |
| Frontend   | Typescript, Next.js 14 (App Router), TailwindCSS and React Hook Form |
| Database   | MySQL (via Docker)   |
| DevOps  | Docker, GitHub Actions, Pytest, ESLint |

⸻

## 🚀 Features
- 🔒 JWT-based authentication
- 💰 Account balance management with deposits, withdraw and transfer
- 💵 List of all of your transactions (bank statement)
- 💻 Simple, intuitive and Responsive UI 
- 📊 Graphic visualization of total inflows and outflows by month of the current year.
- 🧪 Automated integration tests of API 
- 🐳 Dockerized development environment

⸻

## 📂 Project Structure

<pre>

```
knock-bank
├── client/                # NextJS App
│   ├── src/           
│   │   ├── app/           # App Routing
│   │   ├── components/    # Global Components
│   │   ├── lib/           # Lib Modules
│   │   └── modules/       # App modules separated by domain
│   └── .env.exemple       # Env Variables Exemple
│
├── server/                # Flask APP
│   ├── knockbankapi/      # API Module
│   ├── migrations/        # Database Migrations
│   ├── tests/             # Automated tests with Pytest
│   └── .env.exemple       # Env Variables Exemple
│
├── .github/               # CI Config
├── docker-compose.yml			
└── README.md
```
</pre>

⸻

## 🪟 Demonstration

⸻

## 🚀 Getting Started

### 📦 Requirements
	• Python 3.12+
	• Node.js 20+
	• Docker & Docker Compose

⸻

## 🐳 Start with Docker

### Build and run everything

`docker-compose up --build`

Access the frontend at http://localhost:3000.
You also can access the backend API docs at http://localhost:5000/api/docs.

⸻

## 🧪 Run Tests

Backend tests (pytest):

- cd server
- uv sync
- uv run pytest

⸻

<!--

## 🧹 Pre-commit Hooks

### One-time setup
pre-commit install

### Run all hooks manually
pre-commit run --all-files

That’s looking super clean and professional, Leo! 🔥 Here’s the final section you can append to your README.md:

⸻

## 🧭 Next Steps
Check out the [Project board]() to see what’s coming next!
We’re actively working on new features like:
- User profile pages
- OAuth login
- Admin dashboard
- Genre-based book filters
- More AI enhancements

Stay tuned and feel free to contribute! -->