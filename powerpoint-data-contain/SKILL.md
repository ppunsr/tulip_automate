---
name: powerpoint-data-contain
description: Manages the layout and data requirements for each PowerPoint slide. Use this to determine exactly what text, bullet points, and graphs a specific slide number requires, and to coordinate fetching that data via the query-orchestrator.
---

# PowerPoint Data Contain Skill

This skill acts as the master blueprint for the monthly report presentation. It defines exactly *what* elements (graphs, tables, bullet points, titles) must be present on each specific slide. 

When a user asks to "build slide X" or asks "what data goes on page Y", use this skill to look up the slide's content requirements and orchestrate the data fetching.

## Objective

To map a slide number to its required visual and text elements, and to instruct the agent to use the `query-orchestrator` to gather those elements before passing them to the `pptx-builder`.

## Workflow

### 1. Slide Requirement Lookup
When building a specific slide, refer to the following blueprint to determine its required contents. (Note: Refer to `config/slide_mapping.json` for the high-level titles).

**Slide Blueprints:**

*   **Slide 5 (Line Friends Growth):**
    *   **Requires Graph:** `graph/line_friends_report_graph.png` (Time-series line chart).
    *   **Requires Text:** 2-3 key findings bullet points about friend growth, organic baselines, and block rates.
    *   **Action:** Call `query-orchestrator` for "Slide 5 data" (which uses BigQuery).

*   **Slide 7 (Traffic Sources):**
    *   **Requires Graph:** `graph/traffic_sources_graph.png` (Time-series line chart).
    *   **Requires Text:** 2-3 key findings bullet points about ad spikes vs. organic traffic.
    *   **Action:** Call `query-orchestrator` for "Slide 7 data" (which uses BigQuery).

*   **Slide 8 (Registers vs. Points Collected):**
    *   **Requires Graph:** `graph/registers_vs_collecting_points_graph.png` (Bar chart).
    *   **Requires Metrics:** Data for "Users who Only Collected" and "Users who Collected & Redeemed".
    *   **Requires Demographic Data:** Top Customer Type Breakdown, specifically highlighting "Kiosk/Counter Beverage Shop" (ร้านขายเครื่องดื่มชง แบบซุ้ม หรือ เคาน์เตอร์).
    *   **Requires Text:** 2-3 key findings bullet points summarizing the collection/redemption behavior and the dominant customer segment.
    *   **Action:** Call `query-orchestrator` for "Slide 8 data" to get the combined PostgreSQL data (using both the collect/redeem snapshot and the customer type breakdown queries).

*   **Slide 14 (Loyalty Program User Types):**
    *   **Requires Table/Data:** Breakdown of collection vs redemption by customer type (e.g., Kiosk, Cafe).
    *   **Requires Text:** 2-3 key findings bullet points highlighting the dominant customer segments.
    *   **Action:** Call `query-orchestrator` for "Slide 14 data" to get the PostgreSQL breakdown.

### 2. Data Gathering Delegation
Once you know *what* the slide needs:
1.  **Invoke `query-orchestrator`**: Ask the `query-orchestrator` skill to execute the necessary queries and generate the data/graphs for this specific slide.
2.  **Verify Elements**: Ensure you have received back the correct `.png` path and the exact text strings (Key Findings) required by the blueprint.

### 3. Assembly Handoff
Once all required elements for the slide are gathered and verified, instruct the `pptx-builder` skill to insert these elements into the target `.pptx` template at the specified slide index.