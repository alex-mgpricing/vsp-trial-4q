---
name: value-hypothesis
description: Build a value hypothesis for a prospect from discovery call notes, using your company's value profile, and save it to your team's SharePoint folder. Use when a seller, pre-sales or value person shares call or meeting notes, asks to prep for or follow up on a prospect call, asks "why would a prospect buy", or asks for a value hypothesis or the value drivers for a deal.
---

# Value hypothesis

You turn a seller's notes about a prospect into a value hypothesis, which covers:

- which of the company's value drivers apply
- the evidence for each driver
- rough numbers
- what to ask next

You save it to your team's SharePoint folder so the business case skill can pick it up later.

## 1. Find your team's folder

Your value leader set up a value profile, `cuvama-value-profile.json`, in a SharePoint folder your team can open. Find it yourself. Never ask the user where the files are.

1. If there is no Microsoft 365 connector, stop and say: "I need your Microsoft 365 connection to reach your team's files. Turn it on under Customize > Connectors, then ask me again."
2. Run `sharepoint_search` for `cuvama-value-profile.json`. Keep only results whose file name is exactly `cuvama-value-profile.json`.
   - **One result:** read it with `read_resource`. Its `storage` section gives the team folder: `driveId` and `folderItemId`. Use them for every read and save, with `parentItemId` set to the `folderItemId`. Search can be out of date, so treat this result only as a pointer to the folder. The profile you use is the one you read from the folder in step 3.
   - **Several results:** read each one and ask which to use, naming each by its company name and folder.
   - **None:** stop and say: "I can't see your team's value profile. Ask your value leader to share the value selling folder with you, then ask me again. If they set it up in the last hour, SharePoint may still be catching up." Never invent a profile.
3. List the team folder with `read_resource` on `file:///{driveId}/{folderItemId}`. Read `cuvama-value-profile.json` from that listing. This is the current profile. If it isn't in the folder, use the copy you found in step 2.

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

Don't build a spreadsheet at this stage, because saving one takes a couple of minutes. The business case skill builds the spreadsheet. If the user asks for a hypothesis spreadsheet, build it the same way as the business case spreadsheet: numbers only, with live formulas.

How to save:

- **JSON**:
  - New file: `sharepoint_upload_file` with `content`, the folder's `driveId` and `parentItemId`.
  - Existing file: `sharepoint_update_file` with its item id. Never create a second copy.
- **If writes aren't allowed**: say their Claude admin needs to allow Microsoft 365 write actions. Offer the file as a download to drop into the folder by hand.

## 5. Reply

Keep the reply short:

- 3 to 5 bullets covering the drivers that apply and the indicative annual value. Say clearly which numbers are typical rather than the customer's own.
- The questions to ask next.
- A link to the deal file.
- "When you have the numbers, ask me to build the business case for <Account>."
