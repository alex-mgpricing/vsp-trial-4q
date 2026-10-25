---
name: business-case
description: Build or update the business case (ROI, payback, net value) for a prospect, starting from the value hypothesis saved in your team's SharePoint folder. Use when a seller asks to "build the business case for a prospect", "what's the ROI for a prospect", "update the numbers for a prospect", or wants a CFO-ready value summary for a deal.
---

# Business case

You build the business case for a prospect, starting from their saved deal file. You work the figures out in code using the exact method below, so the same inputs always give the same answer. Then you save the result back to your team's SharePoint folder.

## 1. Find your team's folder and the deal

Your value leader set up a value profile, `cuvama-value-profile.json`, in a SharePoint folder your team can open. Find it yourself. Never ask the user where the files are.

1. If there is no Microsoft 365 connector, stop and say: "I need your Microsoft 365 connection to reach your team's files. Turn it on under Customize > Connectors, then ask me again."
2. Run `sharepoint_search` for `cuvama-value-profile.json`. Keep only results whose file name is exactly `cuvama-value-profile.json`.
   - **One result:** read it with `read_resource`. Its `storage` section gives the team folder: `driveId` and `folderItemId`. Use them for every read and save, with `parentItemId` set to the `folderItemId`. Search can be out of date, so treat this result only as a pointer to the folder. The profile you use is the one you read from the folder in step 3.
   - **Several results:** read each one and ask which to use, naming each by its company name and folder.
   - **None:** stop and say: "I can't see your team's value profile. Ask your value leader to share the value selling folder with you, then ask me again. If they set it up in the last hour, SharePoint may still be catching up." Never invent a profile.
3. List the team folder with `read_resource` on `file:///{driveId}/{folderItemId}`. Read `cuvama-value-profile.json` from that listing. This is the current profile. If it isn't in the folder, use the copy you found in step 2.
4. Find the deal:
   - Look for `<slug>.deal.json`. The slug is the prospect name in lowercase, with hyphens for spaces.
   - If the name doesn't match exactly, pick the closest `.deal.json` file. If two are equally close, ask.
   - If there is no deal file, say so and offer to start from notes now. That runs the value hypothesis steps first.

## 2. Fill the gaps

From the deal file, list the inputs whose source is still `typical` or `assumed`. In **one** message, ask for:

- any of those numbers the user knows (they can say "use typical")
- the investment, if it isn't in the deal file yet: the annual fee and the one-off cost

Update the inputs the user gives you to source `customer`.

## 3. Calculate in code, with this exact method

Run this in code. Never do the arithmetic in your head, and don't change the method.

```python
from math import prod

def business_case(drivers, annual_fee, one_off_cost, years):
    lines = []
    for d in drivers:
        annual = prod(i["value"] for i in d["inputs"])
        lines.append({"driverId": d["driverId"], "name": d["name"], "annualBenefit": round(annual, 2)})
    total_annual = round(sum(l["annualBenefit"] for l in lines), 2)
    total_benefit = round(total_annual * years, 2)
    total_cost = round(one_off_cost + annual_fee * years, 2)
    net_value = round(total_benefit - total_cost, 2)
    roi_pct = round(net_value / total_cost * 100, 1) if total_cost else None
    payback_months = round((one_off_cost + annual_fee) / (total_annual / 12), 1) if total_annual else None
    return {"lines": lines, "totalAnnualBenefit": total_annual, "years": years,
            "totalBenefit": total_benefit, "totalCost": total_cost, "netValue": net_value,
            "roiPct": roi_pct, "paybackMonths": payback_months}
```

`years` comes from the profile's `businessCaseDefaults.years`, or 3 if that is missing.

## 4. Save

Update the deal file **in place** using `sharepoint_update_file` with its item id. Never create a second copy.

- Keep the `hypothesis` section, with the updated input values and sources.
- Set `updatedAt` and `updatedBy`.
- Set `businessCase` to:

```json
{
  "method": "cuvama-bc/1",
  "calculatedAt": "",
  "investment": { "annualFee": 0, "oneOffCost": 0 },
  "results": { "...": "the dictionary returned by business_case()" }
}
```

Then save `<Account> - Business Case.xlsx`. Build it with openpyxl in code, as two sheets:

- **"Inputs"**: one row per input, with columns Driver, Input, Unit, Value, Source.
- **"Business case"**:
  - one row per driver, with an annual benefit cell holding a live `=PRODUCT(...)` formula over that driver's Inputs cells
  - total annual benefit (`=SUM`)
  - years
  - total benefit
  - annual fee and one-off cost
  - total cost
  - net value
  - ROI %
  - payback months

All of these are live formulas, so the sheet recalculates if someone changes an input.

Keep the file as small as possible, because every extra kilobyte slows the save:
- numbers and short labels only, with no evidence, notes or questions text
- bold headers only, no other styling, no images

Before you start the upload, tell the user in one line: "Saving the spreadsheet to SharePoint, this takes a minute or two."

How to upload the Excel file:

- In the same code run that builds the file, print its exact byte length and its base64 text.
- Upload with `sharepoint_upload_file`, using `contentBase64` copied exactly as printed, with `expectedBytes`. Use `sharepoint_update_file` if the file already exists.
- If the upload is refused, rebuild and retry once.
- If it still fails, give the user the file as a download and ask them to drop it into the folder.

If writes aren't allowed at all, say their Claude admin needs to allow Microsoft 365 write actions. Offer the files as downloads.

## 5. Reply

Keep the reply short:

- Headline figures, shown exactly as stored in the deal file so they never differ between conversations:
  - annual benefit and net value over the period, in the profile's currency, in whole units
  - ROI to one decimal place
  - payback in months to one decimal place
- Which numbers are still typical rather than the customer's own.
- Links to the deal file and the Excel file.
