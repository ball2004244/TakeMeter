# TakeMeter: planning.md

> Complete this document before collecting any data.
> Update it before starting any stretch features.

---

## Community

**Chosen community:** r/QuantumComputing

r/QuantumComputing is a text-heavy subreddit where researchers, students, and quantum computing nerds talk about hardware, algorithms, error correction, and theory.

It is a good fit for this classifier because the post types are different in a way that regular users would understand. In other word, the verbal boundary is clear. That gives the model real signal instead of forcing fake labels onto messy data.

The subreddit also has enough activity to collect 200+ examples manually without scraping. The labels match patterns the community already cares about, especially around low-effort hype, beginner questions, and technical discussion.

---

## Labels

### `news`

A post that mainly shares an external announcement, paper, article, company update, or industry development.

The value is mostly in the linked content, not in the poster's own argument. The poster may add a short reaction, but they are not building a real claim.

> *Example 1:* "Microsoft's Majorana 2 Topological Quantum Computer"
> *Example 2:* "QpiAI Achieves High-Speed Quantum Error Correction on Superconducting Systems"

### `discussion`

A post where the author has a claim, take, concern, prediction, or observation they want the community to debate.

There is no single correct answer. The post is useful because it invites judgment from people with different levels of expertise.

> *Example 1:* "When will SC qubits start to die off?"
> *Example 2:* "What do you think of QuEra's 'Fault-tolerance in 2028' - is it a bold claim?"

### `question`

A post where the author is missing some understanding and wants an explanation.

A single informed person could answer it well by pointing to a known concept, source, paper, or standard explanation.

> *Example 1:* "I don't get generalized amplitude damping"
> *Example 2:* "Why don't we just perform another transform in the Fourier basis after QFT?"

---

## Hard Edge Cases

**Ambiguous post:** *"What do you think actually counts as a quantum measurement?"*

This looks like a question, but it is not asking for one clean answer. It invites debate about interpretation, definitions, and philosophy.

**Decision rule:** If one informed person could answer the post correctly with a source or known explanation, label it `question`.

If the post needs community debate because there is no single settled answer, label it `discussion`.

Use this rule especially for posts that start with phrases like:

* "What do you think..."
* "Why do we..."
* "Why don't we..."
* "Is it fair to say..."
* "When will..."

The grammar can be misleading. The intent matters more than the punctuation.

**Second edge case:** *"Google just dropped their Willow paper. SC is clearly winning the hardware race and neutral atoms are already obsolete."*

This post shares a real announcement but then builds a bold claim from it. The news is just the setup. The actual content is the poster's argument.

**Decision rule:** If the post's primary value is in the linked content, label it `news`. If the poster uses the news as a launching pad to make their own claim or take a side, label it `discussion`. Ask: would the post still have something to say if you removed the link? If yes, it is `discussion`.

**Additional difficult cases encountered during annotation:**

* ""
* ""
* ""

---

## Data Collection Plan

**Source:** r/QuantumComputing

Posts will be collected manually from `/hot`, `/new`, and `/top` from the past year.

**Target distribution:** Around 67 examples per label, or roughly one third per class.

This keeps the dataset balanced enough that the model cannot win by overpredicting one label.

If any label drops below 20% after 200 examples, collect more examples from that label before training.

**What to do if a label is underrepresented:**

* `news`: easiest to find in `/new`
* `question`: appears in regular posts and weekly help threads
* `discussion`: requires more browsing, but shows up in `/hot` and longer debate posts

**Format:** One CSV file with these columns:

* `text`: post title plus body, if body exists
* `label`: `news`, `discussion`, or `question`
* `notes`: optional notes for ambiguous examples

**Split:** The notebook handles the split automatically: 70% train, 15% validation, 15% test.

---

## Evaluation Metrics

**Primary metric:** F1 per class.

**Why F1 instead of only accuracy:** Accuracy can hide bad behavior. If the dataset ends up 50% `question`, a dumb model could predict `question` every time and still get 50% accuracy.

F1 per class shows whether the model actually learned each label. This matters because a classifier that fails on one class is not useful, even if the overall accuracy looks fine.

**Also reporting:**

* Overall accuracy, for the zero-shot baseline comparison
* Confusion matrix, to see which labels get mixed up
* Macro F1, as one summary score across all three labels

---

## Definition of Success

The classifier is good enough for a moderation or research tool if:

* Macro F1 is at least 0.70 on the test set
* No class has F1 below 0.60
* The fine-tuned model beats the zero-shot baseline by at least 10 percentage points on macro F1

If it misses these thresholds, the next step is more data, cleaner labels, or a tighter taxonomy. Shipping below that would mostly produce noise.

---

## AI Tool Plan

**Label stress testing:** Give Claude the three label definitions and the hard edge case rule. Ask it to generate 10 posts near the boundary between `discussion` and `question`.

If those posts cannot be labeled cleanly with the current rule, tighten the definitions before annotating the full dataset.

**Annotation assistance:** Use Claude to pre-label batches of 20 to 30 posts.

Each batch should include the label definitions and ask for one label per post. Every pre-label must be reviewed manually before it is accepted. No skimming.

The final AI usage section should disclose which examples were pre-labeled.

**Failure analysis:** After fine-tuning, paste the wrong predictions into Claude and ask it to look for patterns, such as:

* Short posts getting misclassified
* Discussion posts with question marks getting labeled as `question`
* News posts without links getting confused with `discussion`

Any pattern Claude suggests must be verified by manually rereading the examples before it goes into the report.
