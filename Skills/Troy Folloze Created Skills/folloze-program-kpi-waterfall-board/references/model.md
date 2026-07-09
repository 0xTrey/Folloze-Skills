# Program KPI Waterfall Board Model

## Standard Benchmarks

| Stage | Standard |
| --- | ---: |
| Accounts in market | 100% |
| Engaged accounts | 30% |
| Sales meetings scheduled | 10% |
| Pipeline opportunities | 50% |
| Closed deals | 30% |

## Core Calculations

- accounts in market = accounts targeted x selected in-market %
- engaged accounts = accounts in market x selected engage %
- sales meetings = engaged accounts x selected meeting %
- pipeline opportunities = sales meetings x selected pipeline %
- closed deals = pipeline opportunities x selected close %
- pipeline goal = average deal size x pipeline opportunities
- bookings = average deal size x closed deals

## Required Interactions

- add program
- duplicate active program
- remove program when more than one exists
- switch active program
- choose customer success manager: `Meghan Richardson`, `Matthew Brown`, or `Steven Nguyen`
- update details and assumptions
- switch benchmark mode between Standard and Custom
- edit custom benchmark values
- copy summary

Each interaction should either track `cta_click` when it is a CTA/button or a descriptive custom event such as `model_update`, `tab-switch`, `program_add`, `program_remove`, or `copy_summary`.

## Customer Name Personalization

Before saving a Folloze board, ask for the customer's name if it is not already provided. Replace `CUSTOMER_NAME_PLACEHOLDER` in the HTML template with the customer name so the first viewport is personalized.

## Program Type Options

- 1:1 ABM
- 1:few ABM
- 1:many ABM
- Executive program
- Event follow-up
- Digital deal room
- Renewal / QBR
- Customer expansion
- Other
- Web Engager Program
- Resource Center
- Enablement Program
- Newsletter
