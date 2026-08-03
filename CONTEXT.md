# Catalyst

Catalyst is a standalone toolbox application. It opens to a home screen listing available Tools; the first Tool is the Daily Report Generator, which turns a daily export of social media monitoring data into a fixed-format PowerPoint presentation and PDF.

## Language

**Catalyst**:
The standalone toolbox application itself — opens to a home screen listing available Tools.
_Avoid_: The app, the program

**Tool**:
A single feature accessible from Catalyst's home screen (e.g. the Daily Report Generator). New capabilities are added as new Tools, not as changes to existing ones.
_Avoid_: Feature, module

**Comment**:
One row of monitoring data — a public social media post or reply that mentions the monitored account, along with its author, link, country, follower count, and tone. Specific to the Daily Report Generator Tool.
_Avoid_: Mention, post, entry

## Relationships

- **Catalyst** hosts one or more **Tools**
- The **Daily Report Generator** is a **Tool** that reads **Comments** from an Excel file
