---
name: value-setup
description: Set up or update a company's Cuvama value selling - its value profile and the SharePoint folder the team saves to. Use when someone asks to "set up Cuvama value selling", "set up our value profile", "update our value drivers", or is a value, sales or enablement leader getting their team started with value selling in Claude.
---

# Value setup (admin)

You help a value leader get their team started:

1. You agree where the team's files will live.
2. You draft the company's **value profile** from its website and save it there.

The profile records where the folder is. The sellers' plugin, **Cuvama Value Selling**, finds the profile by searching SharePoint, so sellers never need to know where the files are.

**Keep it quick and easy.**
- Do the research yourself.
- Ask no more than 4 questions in total.
- Never ask for anything technical, such as IDs or paths.
- Aim for under 10 minutes.

## 1. Check the connection

You need the Microsoft 365 connector. If it isn't available, stop and say: "I need your Microsoft 365 connection to save your team's files. Turn it on under Customize > Connectors, then ask me again."

## 2. Updating an existing profile?

If the admin wants to change an existing profile, first look for it:

1. Run `sharepoint_search` for `cuvama-value-profile.json`.
2. If you find exactly one, read it and use its `storage` details (`driveId`, `folderItemId`, `folderLink`). Don't ask for the folder again. Go to step 5, then save in place (step 6).
3. If you find none or several, ask for the folder link as in step 3.

For a first-time setup, continue with step 2b.

## 2b. Ask two things, in one message

Say, in your own words:

1. "What's your company website?"
2. "Where should your team's value selling files live? Pick or create a SharePoint folder your sellers can open, open it in your browser, and paste the address from the address bar."

## 3. Open the folder from its link

The Microsoft 365 connector can't open web links directly, so work out the folder's location yourself:

1. **Decode the link.** `%20` is a space and `%2F` is `/`. Find the folder's path within the site:
   - **Link with `id=` in it** (`.../Forms/AllItems.aspx?id=...`): the `id` value is the path, for example `/sites/Sales/Shared Documents/Projects/Value`.
   - **Direct link** (`https://contoso.sharepoint.com/sites/Sales/Shared%20Documents/Projects/Value`): the path is everything after the domain.
   - **Short sharing link** (contains `/:f:/`): you can't open it. Ask once for the address-bar link instead: "Open the folder in your browser and copy the address from the top of the window."
2. **Split the path into three parts:**
   - the site (`/sites/Sales`)
   - the library (the next part, usually `Shared Documents`)
   - the folder path inside the library (`Projects/Value`)
3. **Find the library's drive id.** Run `sharepoint_search` for a word from the folder path, with `folderName` set to the parent folder's name if there is one. Take the `driveId` of a result whose `webUrl` contains `<domain><site>/<library>/`. If nothing matches, try other words from the path or the site name, up to 4 tries.
4. **Find the folder's item id.** List the parent folder with `read_resource` on `file:///{driveId}/{parent folder path}`. The path never includes the library name; for a folder at the top of the library, use `drive:///` listings or search. Find the folder by name: its URI is `file:///{driveId}/{folderItemId}`.
5. **Confirm.** List the folder with `read_resource` on `file:///{driveId}/{folderItemId}`. An empty folder returns nothing, which is fine. If `cuvama-value-profile.json` is already there, read it and ask: "You already have a value profile. Update it, or start again?"

If you can't open the folder after these steps, tell the admin plainly what you tried. Ask them to check they have edit access to it.

## 4. Research and draft

Use web search and web fetch. Read the home page, the main product pages and the customer stories or case studies, about 6 pages in total. Search for "<company> case study" if the site doesn't link them. Work out the currency from the site; only ask if you really can't tell.

Draft:

- **What we sell**: 2 or 3 plain sentences.
- **Buyer roles**: 2 or 3 roles, each with what they care about.
- **Value drivers**: 4 to 6. Each one has:
  - a short name and description
  - 3 to 5 "signals", meaning phrases a prospect might say that point to this driver
  - 2 to 4 inputs
- **Case studies**: customer, result, link.

**Inputs rule**: a driver's annual benefit is the **product of its inputs**, so the inputs must multiply out to an annual amount in the currency. For example: people affected × hours saved per person per week × working weeks per year (46) × hourly cost. Write percentages as decimals (0.2, not 20%). Give every input a typical value and say where it came from: a case study link, the website, or "assumption".

## 5. Check with the admin

Show a short summary:

- One line on what they sell.
- The buyer roles.
- Each driver with its inputs and typical values.

Then ask: "Anything wrong or missing? Reply with changes, or say 'looks good'." Apply the changes. Do one round, or two if they ask for more.

## 6. Save the profile

Write `cuvama-value-profile.json` into the folder in this shape:

```json
{
  "schema": "cuvama-value-profile/1",
  "updatedAt": "2026-10-21T10:00:00Z",
  "updatedBy": "Name of the user",
  "company": { "name": "", "website": "", "whatWeSell": "" },
  "currency": "GBP",
  "storage": { "folderLink": "", "driveId": "", "folderItemId": "" },
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

- **New file**: use `sharepoint_upload_file` with `content` (plain text), the `driveId` and `parentItemId` set to the folder's item id.
- **Existing profile**: use `sharepoint_update_file` with the file's item id. Never create a second copy.
- **If the save is refused** because writes aren't allowed: tell the admin their Claude admin needs to allow Microsoft 365 write actions, then stop.
## 7. Finish

Reply briefly, with these three steps:

1. **Give your team access to the folder** in SharePoint, if they don't have it already: {folder link}.
2. **Get your team the sellers' plugin, Cuvama Value Selling.** Each seller adds it in Claude under **Customize > Plugins > Add > Add marketplace**, using https://github.com/alex-mgpricing/vsp-trial-4q, then selects **Add** next to **Cuvama Value Selling**. If you're a Claude Owner, you can install it for everyone instead, under **Organization settings > Plugins & skills**.
3. **Tell them** that the first time Claude saves a file, it asks permission to use SharePoint. They should choose **Always allow**.

Then add: "Your sellers can now paste call notes and ask for a value hypothesis. SharePoint can take up to an hour to make a new profile findable, so if someone tries straight away and Claude can't see it, wait a little. If you change the profile later, just ask me to update it."
