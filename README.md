
# Skylark Drones - Monday.com BI Agent

## 🚀 Quick Deploy (5 Minutes)

### Option 1: Streamlit Cloud (Recommended)

1. Upload this folder to a new GitHub repo
2. Go to https://streamlit.io/cloud
3. Deploy app.py
4. Add secrets:

MONDAY_API_TOKEN="your_token"
WORK_BOARD_ID="your_work_board_id"
DEALS_BOARD_ID="your_deals_board_id"

Done.

---

## 📌 What This Does

- Connects live to Monday.com (Read-only)
- Fetches Work Orders + Deals boards
- Cleans dates
- Answers simple BI questions
- No CSV hardcoding

---

## 📊 Example Questions

- How is our revenue looking?
- How many work orders do we have?

---

## 🏗 Tech Stack

- Streamlit (Frontend + Hosting)
- Pandas (Data Processing)
- Monday.com GraphQL API

---

## ⚠ Important

You must provide:
- Monday API Token
- Board IDs for Work Orders and Deals

