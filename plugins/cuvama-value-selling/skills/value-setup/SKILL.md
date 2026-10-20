---
name: value-setup
description: Set up or update the company's value profile that the Cuvama value selling skills use. Use when someone asks to "set up Cuvama value selling", "set up our value profile", "update our value drivers", or is a value, sales or enablement leader getting their team started with value selling in Claude.
---

# Value setup (admin)

You help a value leader create the **value profile**: one JSON file describing what their company sells, who buys it, and the value it delivers. Their team's value selling skills read it every time they run. Do most of the work yourself from the company's website, so the leader only checks and corrects.

Keep it quick. Aim for no more than 5 questions to the user in total and about 10 minutes.

## 1. Check the connection and find the shared folder

All files live in one SharePoint folder named exactly **Cuvama Value Selling**.

1. Search with the Microsoft 365 connector's `sharepoint_folder_search` using the name `Cuvama Value Selling`.
2. If there is no Microsoft 365 connector, stop and say: "I can't reach SharePoint. Connect Microsoft 365 under Customize > Connectors, then ask me again."
3. If there is one match, use it. If there are several, show each one's site and path and ask which one.
4. If there are none, ask the user to create a folder with that exact name in a SharePoint site or OneDrive their team can open, then tell you when it's done.
5. List the folder's contents with `read_resource` on its URI. If `cuvama-value-profile.json` is already there, read it and ask whether they want to update it or start again.

## 2. Ask for the website

In one message, ask for the company website. If you can't tell the currency they sell in from the site, ask that in the same message.

## 3. Research

Use web search and web fetch. Read the home page, the main product pages and the customer stories or case studies, about 6 pages in total. Search for "<company> case study" if the site doesn't link them.

Draft:

- **What we sell**: 2 or 3 plain sentences.
- **Buyer roles**: 2 or 3 roles, each with what they care about.
- **Value drivers**: 4 to 6. Each one has:
  - a short name and description
  - 3 to 5 "signals", meaning phrases a prospect might say that point to this driver
  - 2 to 4 inputs
- **Case studies**: customer, result, link.

**Inputs rule**: a driver's annual benefit is the **product of its inputs**, so the inputs must multiply out to an annual amount in the currency. For example: people affected × hours saved per person per week × working weeks per year (46) × hourly cost. Write percentages as decimals (0.2, not 20%). Give every input a typical value and say where it came from: a case study link, the website, or "assumption".

## 4. Check with the user

Show a short summary:

- One line on what they sell.
- The buyer roles.
- Each driver with its inputs and typical values.

Then ask: "Anything wrong or missing? Reply with changes, or say 'looks good'." Apply the changes. Do one round, or two if they ask for more.

## 5. Save

Write `cuvama-value-profile.json` into the folder in this shape:

```json
{
  "schema": "cuvama-value-profile/1",
  "updatedAt": "2026-10-21T10:00:00Z",
  "updatedBy": "Name of the user",
  "company": { "name": "", "website": "", "whatWeSell": "" },
  "currency": "GBP",
  "buyerRoles": [ { "role": "", "caresAbout": "" } ],
  "valueDrivers": [
    {
      "id": "D1",
      "name": "",
      "description": "",
      "signals": [ "" ],
      "inputs": [
        { "id": "D1_I1", "name": "", "unit": "", "typicalValue": 0, "source": "" }
      ]
    }
  ],
  "caseStudies": [ { "customer": "", "result": "", "url": "" } ],
  "businessCaseDefaults": { "years": 3 }
}
```

How to save:

- **New file**: use `sharepoint_upload_file` with `content` (plain text), the folder's `driveId` and `parentItemId`.
- **Updating an existing profile**: use `sharepoint_update_file` with the file's item id. Never create a second copy.
- **If the save is refused** because writes aren't allowed: tell the user their Claude admin needs to allow Microsoft 365 write actions. Give them the file as a download to drop into the folder by hand.

## 6. Finish

Reply with:

- a link to the saved profile
- "Next: share this plugin with your team (Customize > Plugins, open Cuvama Value Selling, Share) and share the Cuvama Value Selling folder with them in SharePoint. They can then paste call notes and ask for a value hypothesis."
