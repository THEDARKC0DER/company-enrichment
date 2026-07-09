import pandas as pd
import json
import os
import re
from dotenv import load_dotenv
from google import genai

# ---------------------------
# LOAD API KEY
# ---------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------------------
# CLEAN JSON FUNCTION
# ---------------------------
def extract_json(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)

    return text


# ---------------------------
# AI BATCH FUNCTION (20 companies)
# ---------------------------
def get_company_info_batch(companies):

    company_list_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(companies)])

    prompt = f"""
Return company information for ALL companies below.

Return ONLY valid JSON ARRAY.

Each item must follow this format:

{{
  "company": "",
  "website": "",
  "industry": "",
  "headquarters": "",
  "description": "",
  "listed_status": "",
  "stock_exchange": "",
  "ticker": ""
}}

Rules:
- listed_status must be one of: "public", "private", "unknown"
- If public company, include ticker + stock exchange
- If private, leave ticker and exchange empty
- Return ONLY JSON array
- No markdown
- No explanation
- Ensure ALL companies are included

Companies:
{company_list_text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    raw_text = response.text
    cleaned_text = extract_json(raw_text)

    try:
        return json.loads(cleaned_text)
    except Exception:
        return []


# ---------------------------
# READ EXCEL
# ---------------------------
df = pd.read_excel("companies.xlsx")
company_col = df.columns[-1]

# ---------------------------
# OUTPUT COLUMNS (UPDATED)
# ---------------------------
df["Website"] = ""
df["Industry"] = ""
df["Headquarters"] = ""
df["Description"] = ""
df["Listed Status"] = ""
df["Stock Exchange"] = ""
df["Ticker"] = ""

# ---------------------------
# PROCESS IN BATCHES OF 20
# ---------------------------
batch_size = 20

companies = df[company_col].fillna("").tolist()

for start in range(0, len(companies), batch_size):

    batch = [c for c in companies[start:start+batch_size] if c]

    if not batch:
        continue

    print(f"\nProcessing batch {start} to {start+len(batch)}")

    results = get_company_info_batch(batch)

    # map results back
    for item in results:

        name = item.get("company", "").strip().lower()

        for i in range(start, start + len(batch)):

            if str(df.at[i, company_col]).strip().lower() == name:

                df.at[i, "Website"] = item.get("website", "")
                df.at[i, "Industry"] = item.get("industry", "")
                df.at[i, "Headquarters"] = item.get("headquarters", "")
                df.at[i, "Description"] = item.get("description", "")

                df.at[i, "Listed Status"] = item.get("listed_status", "")
                df.at[i, "Stock Exchange"] = item.get("stock_exchange", "")
                df.at[i, "Ticker"] = item.get("ticker", "")

                break

# ---------------------------
# SAVE OUTPUT
# ---------------------------
df.to_excel("output.xlsx", index=False)

print("Done! output.xlsx created successfully.")