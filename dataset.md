# TakeMeter - Dataset Documentation

This document only accounts for the two dataset files used by the project:

```text
data/dataset.csv
data/dataset_600.csv
```

Raw scrape files, image-only post exports, dropped-row audits, and other intermediate data are local working files. They are not part of the committed dataset package. The only non-dataset outputs expected in the repo are the notebook outputs, such as `confusion_matrix.png` and `evaluation_results.json`.

---

## Shared Format

Both dataset files use the same notebook-ready schema:

| Column | Description |
|---|---|
| `text` | Reddit post title plus body text when available |
| `label` | One of `news`, `discussion`, or `question` |
| `notes` | Short provenance or annotation note |

The Colab notebook reads these files directly with:

```python
df = pd.read_csv(CSV_PATH)
```

No URL, date, score, comment count, or raw Reddit metadata is required for training. Those fields were useful during collection, but they are intentionally not part of the final committed dataset format.

---

## Label Taxonomy

The labels follow the rules in `taxonomy.md` and `planning.md`.

### `news`

A post that mainly shares an external announcement, paper, article, company update, event, course, tool release, or industry development.

The value is mostly in the linked content, not in the poster's own argument.

### `discussion`

A post where the author has a claim, take, concern, prediction, or observation they want the community to debate.

There is no single clean answer. The post is useful because it invites judgment.

### `question`

A post where the author is missing some understanding and wants an explanation.

A single informed person could answer it well by pointing to a known concept, source, paper, or standard explanation.

### Hard edge case rule

The grammar can be misleading. The intent matters more than punctuation.

If one informed person could answer the post correctly with a source or known explanation, label it `question`.

If the post needs community debate because there is no single settled answer, label it `discussion`.

---

## `data/dataset.csv`

`data/dataset.csv` is the smaller balanced dataset from the first collection pass.

It was generated from an earlier curated pool of r/QuantumComputing posts. The generation process was:

1. Normalize post text.
2. Remove near-duplicates within each label.
3. Keep legitimate short titles rather than dropping them automatically.
4. Balance classes by undersampling to the smallest class size.
5. Shuffle rows with a fixed random seed.
6. Write only `text`, `label`, and `notes`.

Final file summary:

| Label | Count |
|---|---:|
| `news` | 78 |
| `discussion` | 78 |
| `question` | 78 |
| **Total** | **234** |

Quality checks:

| Check | Result |
|---|---:|
| Blank `text` rows | 0 |
| Blank `label` rows | 0 |
| Unique `text` rows | 234 |

This file is useful as the clean starter-sized dataset. It is balanced, small, and easy to inspect manually.

---

## `data/dataset_600.csv`

`data/dataset_600.csv` is the larger curated dataset used for the final demo notebook.

It was generated from a larger Reddit scrape where title and body/description were available separately. The generation process was:

1. Combine title and body/description into one `text` field.
2. Drop rows with missing title or missing body text.
3. Move image-only or media-only posts out of the training set.
4. Apply the project taxonomy to produce initial labels.
5. Drop low-confidence rows rather than forcing ambiguous examples into a class.
6. Cap only the oversized class when needed, instead of forcing a perfectly balanced dataset.
7. Manually review the labels row by row after model error analysis.
8. Write only `text`, `label`, and `notes`.

Final file summary:

| Label | Count |
|---|---:|
| `news` | 160 |
| `discussion` | 197 |
| `question` | 226 |
| **Total** | **583** |

Quality checks:

| Check | Result |
|---|---:|
| Blank `text` rows | 0 |
| Blank `label` rows | 0 |
| Unique `text` rows | 583 |

This file is the main dataset for the current project result. It is not perfectly balanced, but it is cleaner than the larger raw scrape. The decision was to prefer label quality over hitting exactly 1000 rows.

---

## Why Only These Two Files

The project originally produced several intermediate files while collecting and cleaning Reddit data. Those files are useful for local debugging but they are not needed to run the notebook or grade the project.

The committed data surface should stay small:

| File | Purpose |
|---|---|
| `data/dataset.csv` | Small balanced dataset from the first pass |
| `data/dataset_600.csv` | Larger curated dataset for the final demo |
| `confusion_matrix.png` | Notebook output for the final model |
| `evaluation_results.json` | Notebook output with final metrics |

Everything else from scraping, media filtering, or dropped-row auditing should be treated as temporary local working data.

---

## Known Limitations

`dataset.csv` is balanced but smaller, so it is easier to inspect but less representative.

`dataset_600.csv` has more examples and body text, but it still contains difficult boundary cases. Most remaining confusion comes from posts that are grammatically questions but function as discussions, or posts that share links while also adding opinionated commentary.

The labels are good enough for a class demo, but a production classifier would need another review pass focused only on `discussion` vs `question` edge cases.
