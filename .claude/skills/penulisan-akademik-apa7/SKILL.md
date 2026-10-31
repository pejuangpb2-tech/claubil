---
name: penulisan-akademik-apa7
description: Academic writing in English and Bahasa Melayu following APA Style 7th edition. Use for writing, editing, paraphrasing or proofreading an essay, assignment, thesis or dissertation chapter, research proposal, journal article, abstract or literature review; for in-text citations and reference lists (Rujukan / References); for APA headings, tables, figures and page format; and for checking a draft against APA 7. Triggers on "APA", "APA 7", "sitasi", "petikan", "rujukan", "senarai rujukan", "penulisan akademik", "tesis", "disertasi", "kertas kerja", "kajian literatur", "abstrak", "citation", "reference list", "academic writing".
---

# Penulisan Akademik APA 7 (English & Bahasa Melayu)

Write and check academic text that follows the *Publication Manual of the American Psychological Association* (7th ed., 2020). It works in English and in Bahasa Melayu; the Malay conventions follow the adaptations Malaysian universities commonly use.

## Ground rules

1. **Never invent a source.** Every citation and reference must come from material the person gave you or a source you actually checked. If an author, year, title, page, volume, issue or DOI is missing, write it as `[perlu disemak: ...]` / `[to verify: ...]`, never a guess.
2. **Ask once, then follow it**: language (English, Bahasa Melayu or both), the document type, and whether the institution has its own APA guide (e.g. a faculty thesis manual). An institutional guide overrides the defaults here, especially for Malay names and Malay abbreviations.
3. **Keep the person's meaning.** When editing, improve clarity, cohesion and register; do not add claims, data or findings. Mark any change of meaning you had to make.
4. **Paraphrase honestly.** A paraphrase changes wording and structure and still carries a citation. A direct quotation keeps the exact words, quotation marks and a page or paragraph number.

## Work loop

1. Identify the task: write, edit, paraphrase, cite, build the reference list, format, or audit.
2. Load the reference for the language: `references/apa7-english.md` or `references/apa7-melayu.md` (both for a bilingual document). Each holds citation rules, reference patterns with examples, headings, format, and register.
3. Do the work. Put citations in the text as you write, and build the reference list from exactly the works cited (every in-text citation has an entry, every entry is cited, except personal communications, which have no entry).
4. Run `references/semakan.md` (the checklist) over the result before handing it back, and list what is still `[perlu disemak]`.

## Output

- Return the finished text in the requested language. For a reference list, give it already sorted, with hanging indents described or applied (in a .docx use the docx skill and set a 0.5 in / 1.27 cm hanging indent).
- After the text, a short note: the conventions used (English or Malay labels, institutional overrides), and every item that still needs checking.
- When asked to audit, report findings as a table: location, problem, APA 7 rule, fix.
