# 💵 KnockBank

![knock_bank_logo](.github/assets/knock_bank_logo.svg)

KnockBank is a modern full stack banking platform that allows its users to deposit, withdrawal and transfer values to other accounts on the platform, also providing a graphic visualization of total inflows and outflows by month of the current year.

⸻

## ⚙️ Tech Stack

| Layer      | Tech                              |
|------------|-----------------------------------|
| Backend    | Python, FastAPI, SQLAlchemy        |
| Frontend   | Typescript, Next.js 14 (App Router), TailwindCSS, React Hook Form |
| Database   | MySQL (via Docker)   |
| DevOps  | Docker, GitHub Actions, Pytest |
| Lint  | Ruff, ESLint |

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
├── server/                # FastAPI APP
│   ├── src/           
│   │   ├── app/           # App Modules
│   │   ├── core/          # Global Configurations
│   │   ├── migrations/    # Database Migrations
│   │   ├── tests/         # Automated Tests
│   │   └── utils/         # Utilities Module
│   └── .env.exemple       # Env Variables Exemple
│
├── .github/               # CI Config
├── docker-compose.yml			
└── README.md
```
</pre>

⸻

## 🪟 Demonstration

### Auth Features

> Sign Up and Sign In

[sign-up-and-sign-in.webm](https://github.com/user-attachments/assets/7429cb94-42ad-4f2d-bc50-fcf613a0bc06)

### Account Management

> Transactions Management (Deposit, Withdraw and Transferences)

[account-balance-management.webm](https://github.com/user-attachments/assets/e49672c0-7ae9-4d8e-ac30-af2b313dcda9)

> View of the Account that received the transaction

[account-balance-other-account.webm](https://github.com/user-attachments/assets/a1282d9e-901c-4f2f-b094-47e894bfe194)

> Updating Account Personal Info

[updating-account-info.webm](https://github.com/user-attachments/assets/b4bbdbd3-e787-4882-b4f7-5cdac5609154)

> Blocking Account

[block-account.webm](https://github.com/user-attachments/assets/39a0b07a-1e99-449e-88e7-cf238a81431a)

⸻

## 📱Mobile

> Initial Page 

![home_mobile](.github/assets/home_mobile.png)

> Dashboard

![dashboard_mobile](.github/assets/dashboard_mobile.png)

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

You also can access the backend API docs at http://localhost:8000/api/docs.

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
