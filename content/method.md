# How these translations are made

This folder holds **provisional English translations** of Chinese Buddhist texts that have no
translation from our approved sources. Each is a best effort: it is **not official**.
It is offered free, so that anyone can read the text in English and judge for themselves how
each line was reached. This page sets out the whole method: the sources, the steps, the checks, the
measured error rate, and the known limits.

| Text | File | Status |
|---|---|---|
| 修華嚴奧旨妄盡還源觀 *Contemplation of the Profound Meaning of Huayan: Ending Delusion and Returning to the Source*, 法藏 Fazang (643–712), CBETA T1876 | [T1876.tsv](../T1876-wang-jin-huan-yuan-guan/) | Complete: preface, six gates, closing verse, and 淨源's Song-dynasty postscript (185 segments). Independently reviewed; line-by-line AI review in progress |

## 1. Who and what does the work

- **The translator is an AI model** (Anthropic's Claude), working under the direction of the
  project owner, a practising lay Buddhist. No line comes from a human translator. That is why
  every line carries its reasons, so a reader can check it.
- **The meaning comes from approved teachers.** The project owner vets which teachers' lectures may
  be learned from (the list: approved-teachers.txt).
  Where the Chinese allows more than one reading, the translation follows the reading an approved
  teacher gives in his lectures on that text, and cites the lecture and line. For T1876 that
  teacher is 體佛法師 (Venerable Tifo, 賢首禪苑), whose 36 lectures cover the whole text.
- **Every line is checked before it is published.** In the BTTS method (below), a translation is
  certified by someone fluent in both languages and experienced in study and practice. One person
  cannot check every line of every text, so here the line-by-line check is made by a second AI
  reviewer, working from the Chinese and the teacher's own words, and the project owner decides
  every line it flags (step 8). The site says, line by line, which check a line has passed: the AI
  review, or the owner's own review. Nothing is published as certified by a person unless a person
  reviewed it.
- **Everything published is labelled AI-generated**, with a link to this page, so a reader always
  knows how the English was made. The same practice is used for the project's published study notes.

## 2. Sources

| Role | Source | How it is used |
|---|---|---|
| The text | CBETA (Chinese Buddhist Electronic Text Association), Taishō edition, e.g. T1876. Licence CC BY-NC-SA 4.0 | The Chinese of every segment, verbatim. CBETA's reading is followed even where a teacher recites a variant; the variant is flagged |
| The reading | Lectures of an approved teacher, as the project's verbatim transcripts (`〔行NNN〕` = line number in that lecture's transcript) | Chooses between readings the Chinese allows. Never adds content |
| Quotations inside the text | The quoted work in CBETA (e.g. 華嚴經 T0279, 起信論 T1666, 寶藏論 T1857) | Every quotation is traced to its source, and a misattribution or reordering by the author is flagged |
| Terms | Digital Dictionary of Buddhism (DDB, Charles Muller); Soothill & Hodous (1937); 丁福保《佛學大辭典》 | To identify a term's sense. A dictionary never decides doctrine |
| House style | BDK English Tripiṭaka (Numata Center) and the Buddhist Text Translation Society (BTTS) | How established translators render recurring terms and names. Where they have translated a passage quoted inside our text, their English is quoted with citation |
| Translation principles | [BTTS Translation Guidelines](https://www.buddhisttexts.org/pages/translation-guidelines) (set out by Venerable Master Hsuan Hua) | Accuracy first; add none of the translator's own ideas; plain English, with Sanskrit only where English has no word; impartial; nothing erased in review |
| Cross-check | Published translations of the same text, where one exists (T1876: Thomas Cleary, *Entry into the Inconceivable*, University of Hawaii Press, 1983, pp. 147–170) | Read *after* our draft is committed, for comparison only. Never copied. Each difference that matters is recorded in §5 |

## 3. Principles

1. **Faithful before fluent.** Nothing is added and nothing is dropped. Awkward grammar may be
   smoothed. Ideas may not be added.
2. **The teacher chooses; he never adds.** A teacher's reading decides only between readings the
   Chinese itself allows, and the `basis` column cites where he gives it. His wider teaching on a
   passage belongs in the study notes, not in the translation.
3. **The Chinese is the authority.** Where a teacher recites a line differently from the canon,
   the translation follows the canon and the flag says what he said.
4. **Every doubt stays visible.** `⚠` marks an uncertain reading, a variant or a traced quotation.
   `[Tr.]` marks a note on a term: what the word is, never what the doctrine means.
5. **One term, one rendering,** unless the sense changes with context, and then the note says so.
   Indian names and terms take their Sanskrit form (tathāgatagarbha, samādhi). Chinese names take pinyin.
6. **Our own words.** The Buddha's teaching belongs to no one. A modern translator's English
   wording does, so published translations are read and learned from, cited, and never reproduced.

## 4. Steps for each section

1. **Fix the text.** Copy the CBETA Chinese verbatim and split it at clause or sentence boundaries, one
   segment per row.
2. **Gather the teacher's readings.** For each hard phrase, find where the teacher reads and
   explains it in his lectures, with line citations. These come from the project's study notes,
   which are themselves checked against the transcripts.
3. **Draft blind.** Translate from the Chinese, the teacher's readings and the dictionaries only.
4. **Commit before comparing.** The draft is committed to version control *before* any published
   translation of that section is opened. The commit is the proof that the draft was made
   independently.
5. **Check every citation and the coverage.** `scripts/provisional.py lint` matches each `basis` citation (lecture number + transcript lines) against the study note of that lecture, and checks that the Chinese column, joined, reproduces the CBETA text exactly — so no sentence is dropped. A finding is traced and corrected before going on.
6. **Cross-check.** Compare the draft with the published translation(s), segment by segment.
   Each difference is resolved by the Chinese and the teacher's reading, never by a translator's
   fame. A real error in our draft is corrected, and the correction is recorded in §5.
7. **Independent review** (done for T1876 — results): a blind back-translation into Chinese by a model
   that never sees the original; a fresh AI reviewer told to assume errors, looking for additions,
   omissions and doctrinal shifts; and a small model from a different AI family. Every objection becomes a visible flag or a recorded fix.
8. **Line-by-line review.** A second AI reviewer (`scripts/provisional.py ai-review`, Claude Opus in a fresh
   context, which never sees the translator's reasoning) judges every line and every term note. It is given
   the Chinese, the English, the flags, and the teacher's evidence copied from the project's files: his own
   words from the lecture transcript where he gives the reading (法師原話) and the study notes on the passage
   (筆記整理). It passes a line only when nothing is added, omitted or misread, the English does not
   contradict the teacher's reading, and the flags are accurate; for a term note, only when the English
   excerpt faithfully translates the cited transcript lines. Anything else, or any doubt, is flagged with the
   Chinese words at issue. The project owner decides every flagged line in the project's local 譯經 tab, where
   each line shows the same evidence, and may review any passed line; the owner's mark outranks the AI's.
   Verdicts are kept in `review/<T-id>/ai-review.json` and the owner's marks in
   `review/<T-id>/certification.json`; each records a hash of what it judged, so a line changed afterwards
   is checked again. A text is published only when every line has passed one of the two checks.
   A **second reviewer** from a different model family then judges every line and note the same way, with the
   same evidence (`ai-review --second`: a free model reached through the owner's local gateways, chosen by a
   calibration on rows with known errors and rows known to be correct — `review/T1876/calibration/`; each verdict
   names the model that gave it). The first reviewer is the same family as the
   translator and can share its blind spots; the second cannot share them in the same way. A reviewer's flag
   counts only if it quotes the Chinese words at issue and those words are in the line; otherwise the line is
   asked again on its own. Once a text has a second review, a line is cleared by AI only when **both** reviewers
   pass it, or when each flag has been checked against the sources — the CBETA text and the teacher's transcript —
   and either fixed (the changed line is then reviewed again) or answered in writing. Every written answer is kept
   with the review files (`review/<T-id>/resolutions.json`) and shown on the line's page. Only a genuine choice
   between the teacher's reading and the plain Chinese goes to the owner. How often the two reviewers disagree,
   and how the second reviewer was chosen, is reported in §5.

### Term notes and the reading guide

A reader of the English alone also gets notes on key terms and a short guide before the text
(`<T-id>.glossary.tsv`). Each note keeps three sources apart, and labels each: **what the term is**
(identification only, from the dictionaries and established translators' usage, never doctrine); **where
the author explains it** in the text itself; and **how the approved teacher explains it**: his own words
from one passage of a lecture, translated, with the lecture and transcript lines cited so the Chinese can
be read beside it. Repetitions and asides such as 「聽得懂嗎」 ("do you follow?") are left out of the
translation; nothing is added, and nothing is summarised in the translator's words. Where the teacher
departs from the usual account, the note says so (⚠). `provisional.py lint` checks that each term occurs
in the English, that every segment id exists, and that every cited transcript line exists. Every note and
guide paragraph goes through the same line-by-line review (step 8); one that has not passed is not published.

### Other readings

Where the Chinese of a line genuinely allows a second reading, the page can show it beside the main English as
**another reading**: its English, why the Chinese allows it, and where it comes from. The main English follows the
approved teacher's reading; the other reading is labelled as one the Chinese also allows (or, where the main
English follows the plain Chinese, as the teacher's own reading), never as a correction. It is added only when it
accords with the Buddha's teaching as the teacher presents it, and it goes through the same review as every line.

## 5. Measured accuracy

The method was tested by translating passages that *do* have published translations without
looking at those translations, then comparing:

| Test | Segments | Real meaning slips in our draft | Additions / omissions | Where the draft and the published one part |
|---|---|---|---|---|
| 圓覺經 普賢章 (vs Gregory, BDK) + 維摩詰經 入不二法門品 1–16 (vs McRae, BDK) | 32 | 1: 「云何復說修行如幻」 read as "practice is like illusion"; it is cultivating *the illusion-like samādhi* | 0 | 6 places, all defensible readings matching the teacher |
| T1876 preface + Gate 1 (vs Cleary) | 26 | 0 found | 0 | P04, P06, P07, P09: see the flags in the file. Cleary omits 消能所 (P07), drops 首 of 心首 (P09), and reads 百非息其攀緣 the other way round (P06). He agrees with the teacher's 病亡則藥亡 against CBETA (P04) |
| T1876 Gate 2 (vs Cleary) | 13 | 0 found | 0 | G07: Cleary ends the 華嚴 verse early, making its last two lines 法藏's prose; CBETA T0279 has them inside the verse |
| T1876 Gate 3 (vs Cleary) | 31 | 0 found | 0 | T12: Cleary leaves out the 煩惱 / 菩提 question pair and reads 今時修學之徒 as "those not cultivating"; T28: he renders 聖眾 (holy assembly) as "scripture"; T24: he presents 法藏's summary of 寶性論 as a quotation (T1611 gives the three errors in other words and order). He confirms the draft's uncertain parse at T31 |
| T1876 Gate 4 (vs Cleary, and against the quoted sources) | 33 | 1, found by tracing the quotation, not by Cleary: D33, the 雜集論 verse 「於不堅堅覺」 read as "taking the unfirm as firm"; the teacher reads 堅覺 as the firm awakening; corrected | 0 | Cleary leaves out the pair 理即事…事即理 (D05) and the mirror simile (D08); he adds "caused by ignorance, greed, and anger" to 三塗 (D32); 平地 "common ground" (D20, the teacher: the level ground a building needs); 被訶 "persecuted" (D22, 訶 = rebuked); he drops 等剎塵 (D28). Tracing also shows 法藏 quoting loosely: 起信論 joined from two passages (D14–15); 「非大沈非小浮」 not in 瑜伽師地論 (D12); 「尸羅不清淨，三昧不現前」 called scripture but found only in commentaries (D21); 雜集論 has 極 where 法藏 has 離 (D33) |
| T1876 Gate 5 (vs Cleary) | 22 | 0 found | 0 | F04: Cleary reads the title 《入佛境界經》 as a sentence ("And accordingly we enter the realm of Buddhahood") and gives the verse to "Scripture" — CBETA T0357 is that sutra; F11–12: 因緣俱離 / 不在緣 as "cause and effect" / "nor in effect" (緣 = conditions); F16: he drops 一乘教中 and 萬字. F13 寂怕 follows the teacher's 怕 = 泊 ("still and settled"; Cleary "void"). A check of the `basis` column found lesson numbers pointing at the wrong lecture — 10 in Gate 5, and 11 more in Gates 3–4 when the whole file was checked; each was traced to the note that holds that exact line range and corrected |
| T1876 Gate 6 + postscript (vs Cleary) | 59 | 0 found | 0 | H35: Cleary leaves out one of the four 十定品 clauses; H40: he leaves out both sentences on Sudhana's sudden realization and the principal tower; H39: he adds "principal and satellites reflecting each other"; H29: 如來 as "those who realize thusness". Tracing: the 金翅鳥 passage (H04) and the Sudhana story (H38) are 法藏's retellings of 華嚴經 T0279, not quotations; H15's 《論》 is 中邊分別論 T1599 with 法藏's changes; H16–17 are 契經 verses quoted in 大乘廣百論釋論 T1571; H23's 「一毛孔中無量剎」 is found nowhere else in CBETA. 淨源's postscript (Z01–Z08) is translated without a teacher's basis, since no approved teacher lectures it |
| T1876 independent review (all 184; files) | 184 | 0 doctrinal shifts, 0 omissions, 1 addition (D15, 妄 rendered "falsely"), 13 minor misreadings (e.g. D10 師於己見 is "taking its own views as teacher", not "teachers following their own views"; T24 道前 is "before the path of seeing"; H44 初心 is "the initial resolve"); all fixed | 0 | The adversarial reviewer also corrected three source flags: H23's verse **is** in 華嚴經 十地品 (with 內 for 中; the translator's exact-string search missed it), T10's verse is in 世主妙嚴品, and 寶藏論 only cites G05's line. One finding rejected (P16, the teacher's reading kept). The back-translation showed no meaning drift and exposed four ambiguous English sentences (D21, D25, T18, H41), now fixed. qwen2.5:7b raised 40 issues: 2 real (both also found by the reviewer), the rest false or style. A stricter citation check then found 4 citations naming lecture 15 for lines in lecture 14 (T21–T25); fixed |
| T1876 line-by-line AI review (all 185 lines and 31 notes) | 216 | First reviewer (Claude Opus 5.5): 31 flags, 28 of them real (missing ordinals, a wrong citation, source notes wrongly marked ✓, two dropped words, three loose renderings, readings brought to the teacher's, six glossary excerpts that left out his words) — all fixed and re-reviewed | 0 | Second reviewer (DeepSeek-V4-Flash, chosen by calibration): 25 flags; 3 led to fixes (P09 心首 and D18 熏修 read with the teacher; H16 records his 楞伽經 attribution, which CBETA does not bear out), 3 were unreadable and were asked again, the rest were answered in writing (`review/T1876/resolutions.json`, 20 rows, shown on each line). T31 follows the teacher's parse by the owner's decision, the other parse kept in its note |
| T1876 coverage lint | 185 | 0 | 1 omission found and fixed: the closing 「紀重校」 line of 淨源's postscript was missing (now Z09). The lint compares the joined Chinese column with CBETA character by character | — |

Across 216 segments: two real slips, nothing added or lost, with nothing added or lost. Caveats: the first
test's texts are famous, so the model may have seen their published translations before. "0 found"
means only that comparison with one published translation found none. It does not prove there are none.

## 6. Reading the files

Each `.tsv` is tab-separated: `seg` (segment id: P preface, G gate 2, …) · `zh` (CBETA Chinese,
verbatim) · `en` (the provisional English) · `basis` (the teacher's reading that decided it: lecture
number, transcript lines, a short summary in English) · `flags` (`⚠` doubts and traced quotations,
`[Tr.]` term notes).

## 7. Licence

The Chinese text is CBETA's, under CC BY-NC-SA 4.0 (attribution, non-commercial, share-alike).
Because each file carries that text, the files are shared under the same terms: free to use,
copy and share, with attribution, never sold.
