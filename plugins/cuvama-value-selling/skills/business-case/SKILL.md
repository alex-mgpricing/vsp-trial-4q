---
name: business-case
description: Build or update the business case (ROI, payback, net value) for a prospect, starting from the value hypothesis saved in the team's Cuvama Value Selling folder. Use when a seller asks to "build the business case for <prospect>", "what's the ROI for <prospect>", "update the numbers for <prospect>", or wants a CFO-ready value summary for a deal.
---

# Business case

You build the business case for a prospect, starting from their saved deal file. You work the figures out in code using the exact method below, so the same inputs always give the same answer. Then you save the result back to the team's shared folder.

## 1. Find the shared folder, the profile and the deal

All files live in one SharePoint folder named exactly **Cuvama Value Selling**.

1. Search with the Microsoft 365 connector's `sharepoint_folder_search` using the name `Cuvama Value Selling`.
2. If there is no Microsoft 365 connector, stop and say: "I can't reach SharePoint. Connect Microsoft 365 under Customize > Connectors, then ask me again."
3. If there is one match, use it. If there are several, show each one's site and path and ask which one.
4. If there are none, ask the user for the folder's link.
5. List the folder with `read_resource` on its URI.
6. Read `cuvama-value-profile.json`. If it's missing, stop and say the value leader needs to run setup first.
7. Find the deal:
   - Look for `<slug>.deal.json`. The slug is the prospect name in lowercase, with hyphens for spaces.
   - If the name doesn't match exactly, pick the closest `.deal.json` file. If two are equally close, ask.
   - If there is no deal file, say so and offer to start from notes now. That runs the value hypothesis skill's steps first.

Don't ask the user for paths or IDs unless all of the above failed.

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

Keep the file small: bold headers only, no other styling, no images.

How to upload the Excel file:

- In the same code run that builds the file, print its exact byte length and its base64 text.
- Upload with `sharepoint_upload_file`, using `contentBase64` copied exactly as printed, with `expectedBytes`. Use `sharepoint_update_file` if the file already exists.
- If the upload is refused, rebuild and retry once.
- If it still fails, give the user the file as a download and ask them to drop it into the folder.

If writes aren't allowed at all, say their Claude admin needs to allow Microsoft 365 write actions. Offer the files as downloads.

## 5. Reply

Keep the reply short:

- Headline figures: annual benefit, net value over the period, ROI and payback, in the profile's currency, rounded to whole units.
- Which numbers are still typical rather than the customer's own.
- Links to the deal file and the Excel file.
