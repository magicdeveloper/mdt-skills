You are extracting atomic facts from one section of a document.

Source text file: {unit_path}
Source document language: {language} — output facts in THIS language only.

RULES (hard — no exceptions):
1. One fact per line. One line = exactly one fact/value/statement. Never merge facts in one line.
2. Every line is as short as possible: the useful fact only, exact meaning, numbers, names — nothing extra.
3. Never repeat a fact: if the same fact appears twice in the unit (including overlap pages), write it once, in its shortest wording.
4. Output only facts stated in the text. Never infer, compute, assume, or add values.
5. No headings, bullets, numbering, or commentary — plain lines only.
6. If the unit has nothing worth keeping, write the single line NO_FACTS — never pad, never an empty file.
7. Before writing: re-scan the unit text and confirm no useful fact is missing and none is repeated in your output.
8. Write the fact lines to the file first — it is your only deliverable. Then reply with one summary line (WRITTEN=<path> LINES=<count>).
