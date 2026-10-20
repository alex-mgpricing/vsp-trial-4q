---
name: value-hypothesis
description: Build a value hypothesis for a prospect from discovery call notes, using the company's Cuvama value profile, and save it to the team's shared folder. Use when a seller, pre-sales or value person shares call or meeting notes, asks to prep for or follow up on a prospect call, asks "why would <prospect> buy", or asks for a value hypothesis or the value drivers for a deal.
---

# Value hypothesis

You turn a seller's notes about a prospect into a value hypothesis, which covers:

- which of the company's value drivers apply
- the evidence for each driver
- rough numbers
- what to ask next

You save it to the team's shared folder so the business case skill can pick it up later.

## 1. Find the shared folder and the profile

All files live in one SharePoint folder named exactly **Cuvama Value Selling**.

1. Search with the Microsoft 365 connector's `sharepoint_folder_search` using the name `Cuvama Value Selling`.
2. If there is no Microsoft 365 connector, stop and say: "I can't reach SharePoint. Connect Microsoft 365 under Customize > Connectors, then ask me again."
3. If there is one match, use it. If there are several, show each one's site and path and ask which one.
4. If there are none, ask the user for the folder's link. If they don't have it, they should ask their value leader to share it.
5. List the folder with `read_resource` on its URI, then read `cuvama-value-profile.json`.
   - If the profile isn't there, stop and say: "Your value profile hasn't been set up yet. Ask your value leader to say 'set up Cuvama value selling' in Claude."
   - Never invent a profile.

Don't ask the user for paths or IDs unless all of the above failed.

## 2. Get the account and notes

You need the prospect's name and the notes, either pasted or attached. Ask in one message only for whatever is missing.

Make the account slug from the name: lowercase, with hyphens for spaces. "Brightwave Software" becomes `brightwave-software`. If `<slug>.deal.json` already exists in the folder, read it. Tell the user you're updating it, and keep its `businessCase` section.

## 3. Build the hypothesis

- Pick the drivers the notes give evidence for. Use each driver's `signals` as a guide, and leave out drivers with no evidence.
- For each chosen driver:
  - Write one line of evidence, quoting the notes where you can.
  - Give a confidence of high, medium or low.
  - Fill each input:
    - Number in the notes: use it, with source `customer`.
    - Otherwise: use the profile's `typicalValue`, with source `typical`.
- List 3 to 5 questions that would replace the most important `typical` numbers with real ones.
- Work out each driver's indicative annual value as the product of its input values, plus the total, **in code**. Never do the arithmetic in your head.

## 4. Save

Save `<slug>.deal.json`:

```json
{
  "schema": "cuvama-deal/1",
  "account": "Brightwave Software",
  "slug": "brightwave-software",
  "profileUpdatedAt": "<updatedAt from the profile>",
  "createdAt": "", "updatedAt": "", "updatedBy": "",
  "hypothesis": {
    "summary": "",
    "drivers": [
      {
        "driverId": "D1", "name": "", "evidence": "", "confidence": "high",
        "inputs": [ { "inputId": "D1_I1", "name": "", "unit": "", "value": 0, "source": "customer", "note": "" } ],
        "indicativeAnnualValue": 0
      }
    ],
    "indicativeTotalAnnualValue": 0,
    "questionsToAsk": [ "" ]
  },
  "businessCase": null
}
```

Then save `<Account> - Value Hypothesis.xlsx`. Build it with openpyxl in code. It has one sheet, "Hypothesis", laid out as follows:

- One row per input, with columns Driver, Evidence, Input, Unit, Value, Source.
- Under each driver, a row "Annual value" with a live `=PRODUCT(...)` formula over that driver's Value cells.
- A "Total" row with `=SUM(...)` of the driver rows.
- Then a "Questions to ask" list.

Keep the file small: bold headers only, no other styling, no images.

How to save:

- **JSON**:
  - New file: `sharepoint_upload_file` with `content`, the folder's `driveId` and `parentItemId`.
  - Existing file: `sharepoint_update_file` with its item id. Never create a second copy.
- **Excel**:
  - In the same code run that builds the file, print its exact byte length and its base64 text.
  - Upload with `contentBase64`, copied exactly as printed, and `expectedBytes`. Use `sharepoint_update_file` if the file already exists.
  - If the upload is refused, rebuild and retry once.
  - If it still fails, give the user the file as a download and ask them to drop it into the folder.
- **If writes aren't allowed**: say their Claude admin needs to allow Microsoft 365 write actions. Offer both files as downloads to drop into the folder by hand.

## 5. Reply

Keep the reply short:

- 3 to 5 bullets covering the drivers that apply and the indicative annual value. Say clearly which numbers are typical rather than the customer's own.
- The questions to ask next.
- Links to both files.
- "When you have the numbers, ask me to build the business case for <Account>."
