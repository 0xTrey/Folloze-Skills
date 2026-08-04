# Canonical Value Proposition Framework

Use the transcript plus approved call/deal context to personalize the existing four-card value widget. Preserve its structure, keep the canonical category order, and change only allowlisted text nodes.

## Fixed card order

Keep these three buyer-facing categories on every deal room:

1. **Build Speed & Scalability** — how the buyer can move from idea or brief to reusable, governed experiences faster and scale the motion without relying on development sprints.
2. **Personalization & Enrichment** — how the buyer can use account, audience, CRM, intent, or other approved context to make each experience more relevant.
3. **Analytics & Optimization** — how the buyer can understand engagement, improve content and journeys, and give sellers or marketers useful signals for the next action.

Use card 4 according to this rule:

- **Openness & AI Connectivity** when the call meaningfully discusses connecting Folloze to a third-party AI system such as Claude, ChatGPT, Gemini, an agent or LLM, MCP, or the buyer's AI stack.
- **Operational Scale & Reuse** when no external-AI use case appears. Remove AI, LLM, agent, MCP, Claude, ChatGPT, Gemini, and AI-ecosystem language from the buyer-facing card. Use the strongest call-supported angle involving reuse, governance, orchestration, seller activation, campaign operations, or scaling a repeatable motion.

Always preserve four card slots and their order. “Remove AI as an option” means remove unsupported AI/openness messaging and use the non-AI fallback in card 4; it does not mean delete the card or change the widget structure.

## Determine whether the AI card is allowed

Set `ai_signal_present=true` only when the transcript contains a relevant external-AI connection or workflow. A generic statement that AI is important, Folloze has AI, or the company uses AI somewhere is not enough.

Qualifying examples include:

- sending Folloze context or engagement data into Claude, ChatGPT, Gemini, or another LLM
- invoking Folloze through MCP, an agent, or an AI orchestration layer
- enriching or generating experiences from an external AI workflow
- connecting the buyer's AI stack to Folloze as part of the discussed operating model

If the evidence is ambiguous, set `ai_signal_present=false` and use Operational Scale & Reuse. Never introduce an AI-system value proposition merely because Folloze supports one.

## Build the private evidence map

Parse the authoritative transcript once. Produce a compact evidence object containing the hero goal, section subheader, four card decisions, timestamps, buyer-safe paraphrases, and AI-signal result. Pass only that compact object and the prepared buyer-facing text into later board-writing and verification steps; do not repeatedly place the full transcript into model context.

For cards 1–3, extract the call detail that should influence the subheadline/body and proof line:

- buyer motion, desired speed, team capacity, production bottleneck, or scale target
- audience, account, segment, campaign, CRM, intent, or enrichment requirement
- measurement, attribution, engagement signal, reporting, seller follow-up, or optimization need

For card 4, capture either the qualifying external-AI signal or the strongest non-AI operational-scale signal.

Each personalized phrase needs a private transcript timestamp and buyer-safe paraphrase. Approved deal context can clarify or validate a detail, but it cannot substitute for the transcript decision about AI. Do not expose raw quotes, attendee names, pricing, objections, internal tasks, or sensitive commercial details in the board.

Stop before publish when the transcript is too incomplete to make the three core cards meaningfully relevant to the buyer. Do not invent metrics, integrations, timelines, or business problems.

## Preserve category identity; personalize the supporting message

When the template's existing label and heading already express the correct category, keep them. Update:

- the overall section subheader
- each card's subheadline/body
- each card's proof line

Change a label or heading only when it has drifted from the canonical category, contains unsupported AI language, or must switch card 4 between AI and non-AI mode.

Write supporting messages as follows:

- connect the fixed value category to a real buyer motion or goal from the call
- use one or two concise sentences
- keep claims within documented Folloze capability
- use a compact, defensible proof line without unsupported metrics
- keep the four cards parallel in tone and visual length

## Allowed HTML changes

Allow changes only to:

- section subheader
- card 1 label, heading, body, and proof line
- card 2 label, heading, body, and proof line
- card 3 label, heading, body, and proof line
- card 4 label, heading, body, and proof line

Preserve:

- widget and wrapper identity
- CSS and responsive behavior
- scripts
- four-card order and structure
- inline SVG artwork
- eyebrow and main section heading
- accessibility and semantic markup

Compare original and edited HTML and reject any non-allowlisted change.

## Evidence receipt

Record a private receipt shaped like:

```json
{
  "section_subheader": "buyer-facing call-informed text",
  "ai_signal_present": false,
  "ai_evidence_ref": null,
  "card_4_mode": "operational_scale_reuse",
  "cards": [
    {
      "card": 1,
      "category": "build_speed_scalability",
      "evidence_ref": "transcript 00:12:40",
      "label": "buyer-facing label",
      "heading": "buyer-facing heading",
      "body": "call-informed buyer-facing subheadline/body",
      "proof_line": "buyer-facing proof line"
    }
  ],
  "core_categories_preserved": true,
  "ai_rule_passed": true,
  "private_language_removed": true,
  "html_diff_allowlist_passed": true,
  "desktop_visual_qa": "passed",
  "mobile_visual_qa": "passed"
}
```

Use `card_4_mode=openness_ai_connectivity` only when `ai_signal_present=true`; otherwise require `card_4_mode=operational_scale_reuse`. Keep evidence references private.

For the production fast path, the compact evidence object is the only transcript-derived input allowed after the evidence lane finishes. A targeted return to the transcript is permitted only when one required timestamp or ambiguity is explicitly identified; do not restart a broad transcript analysis.

## Visual QA

Verify the section in authenticated designer/preview after saving:

- all four cards render and remain in the canonical order
- the three core categories are recognizable and buyer-relevant
- card 4 contains no AI language when `ai_signal_present=false`
- no card overflows or becomes disproportionately tall
- labels, headings, bodies, and proof lines are readable at desktop and mobile breakpoints
- SVG artwork and layout remain unchanged
