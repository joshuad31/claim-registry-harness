# Distillation: finding the needles

Your sources are the haystack. The needles are the few passages that should change how much you believe each rival answer.

Distillation is boiling the pile down to those passages. It is not a summary. A summary keeps a little of everything; distillation keeps only what bears on your question.

How it works:

1. An AI asks NotebookLM one narrow question about one to three named sources.
2. NotebookLM answers from those sources, with a citation beside each number.
3. A second AI scores the answer: did it shift the balance between the rival answers?
4. The next questions go where a shift is most likely.
5. Afterwards each answer is cut into single findings, and each finding's quotation is checked against the source file.

A good question is one whose answer could move the balance. Asking those first is the quickest way through the pile.

Two limits. NotebookLM can miss a passage, so every question is logged and the list can be checked for gaps. And checking that a quotation is real is mechanical; checking that it means what the finding says still takes judgment.

Next: [Who does what](roles.md)
