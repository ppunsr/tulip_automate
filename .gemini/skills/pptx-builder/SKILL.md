---
name: pptx-builder
description: Automates the generation of PowerPoint (.pptx) presentations. Use this skill to insert generated graphs (images) and text insights (findings) into specific slides of a given PowerPoint template.
---

# PPTX Builder Skill

This skill allows you to programmatically modify a PowerPoint template by inserting data visualizations and analytical text (findings) into specific slides.

## Usage

Use the `run_shell_command` tool to execute the `build_pptx.py` script. The script accepts a single JSON string argument detailing the required modifications.

**Bash:**
```bash
python3 <skill_dir>/scripts/build_pptx.py '<JSON_CONFIG_STRING>'
```

### JSON Configuration Format

The JSON string must contain the following keys:
*   `template_path`: The path to the input `.pptx` template file.
*   `output_path`: The desired path for the newly generated `.pptx` file.
*   `updates`: A list of objects detailing the updates for specific slides.

**Updates Object Fields:**
*   `slide_index`: (Required) The 0-based index of the slide to update (e.g., `4` for Slide 5).
*   `image_path`: (Optional) The path to the `.png` graph to insert.
*   `replace_shape_name`: (Optional) The name of an existing shape on the slide to delete (e.g., `"Chart 7"`) to make room for the new image.
*   `img_left_inches`: (Optional) X-coordinate for image (default: 1).
*   `img_top_inches`: (Optional) Y-coordinate for image (default: 1.5).
*   `img_width_inches`: (Optional) Width of the image (default: 8).
*   `finding_text`: (Optional) The analytical insight to add. The script will automatically locate an existing text box containing the word "Findings" and replace its text. If none exists, it will create a new text box.

**Example Configuration:**
```json
{
  "template_path": "/Users/sboora01/Tulip project/Tulip-automate/Tulip_example.pptx",
  "output_path": "/Users/sboora01/Tulip project/Tulip-automate/Monthly_Report_Output.pptx",
  "updates": [
    {
      "slide_index": 4,
      "image_path": "/Users/sboora01/Tulip project/Tulip-automate/line_friends_report_graph.png",
      "replace_shape_name": "Chart 7",
      "finding_text": "In March 2026, LINE gained 4,408 new friends, maintaining a steady organic growth rate."
    }
  ]
}
```

## Bundled Resources
*   `scripts/build_pptx.py`: The Python script that parses the JSON configuration and modifies the PowerPoint presentation using `python-pptx`.
