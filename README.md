# Company Enrichment Tool

This script reads company names from `companies.xlsx`, fetches company information using the Gemini API, and updates the provided `output.xlsx` file with the enriched data.

## Files Required

Make sure these files are in the same folder:

- `company_enrichment.py`
- `companies.xlsx`
- `output.xlsx`
- `.env`

---

## 1. Install Python Libraries

Open a terminal in the project folder and run:

```bash
pip install pandas openpyxl python-dotenv google-genai
```

---

## 2. Add Your Gemini API Key

Create a file named `.env` and add:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Gemini API key.

---

## 3. Add Company Names

Open `companies.xlsx` and enter the company names in the **last column**.

Example:

| Company   |
| --------- |
| Microsoft |
| Google    |
| Apple     |

Save the file.

---

## 4. Run the Script

```bash
python company_enrichment.py
```

(Replace `company_enrichment.py` with your script name if it's different.)

---

## 5. Check the Result

After the script finishes, open **`output.xlsx`**.

It will contain the original company names along with:

- Website
- Industry
- Headquarters
- Description
- Listed Status
- Stock Exchange
- Ticker

---

## If You Get an Error

- **Missing library?** Run:

  ```bash
  pip install pandas openpyxl python-dotenv google-genai
  ```

- **API key error?** Check that your `.env` file contains:

  ```env
  GEMINI_API_KEY=your_api_key_here
  ```

- **Excel file not found?** Make sure `companies.xlsx` and `output.xlsx` are in the same folder as the Python script.
# company-enrichment
