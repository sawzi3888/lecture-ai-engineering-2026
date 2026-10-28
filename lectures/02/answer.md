# Lecture 02 Answers

## Exercises

### Model and training settings

- **Base model:** `Qwen/Qwen3.5-0.8B`
- **Training method:** LoRA without quantization
- **Epochs:** 20
- **Learning rate:** 0.0002
- **LoRA rank (`r`):** 16
- **LoRA alpha:** 32
- **Maximum sequence length:** 512
- **Random seed:** 42
- **Generation:** Greedy decoding (`do_sample=False`)
- **Training executed myself:** Yes. I ran the Colab training and evaluation using a T4 GPU.

### Before and after training

| Metric | Before training | After training |
|---|---:|---:|
| Number of test questions | 21 | 21 |
| Format compliance | 95.24% | 100% |
| Content accuracy | 19.05% | 100% |
| Both criteria satisfied | 19.05% | 100% |
| Evaluation time | 27.6 s | 32.2 s |

**Questions that regressed in the main evaluation:** None.

The model learned to produce valid JSON and answers matching the expected protocol rules. However, the evaluation used keyword matching, so some semantically correct short answers were marked incorrect before training. The improvement therefore reflects both better adherence to the expected answer format and better matching of the reference wording.

### Remaining failures after training

No failures were observed among the 21 main test questions. However, an additional knowledge test revealed an unsupported assertion.

### Section 6: Knowledge questions

| Question | Before training | After training |
|---|---|---|
| Hospital ethics committee approval | Needs review | Unsupported assertion |
| Required external validation sample size | Needs review | Needs review |
| ICF code for impaired memory | Unsupported assertion | Needs review |
| Severity scale (grounded control) | Asserted correctly | Asserted correctly |

For the ethics committee question, the trained model stated that the protocol had been developed by a hospital ethics committee, although the FAQ provided no such information. This illustrates a limitation of fine-tuning: perfect performance on a small predefined test set does not guarantee reliable decisions on unfamiliar questions.

### What changed and what stayed the same?

After LoRA fine-tuning, the model followed the required JSON output structure more consistently and reproduced the expected answers to familiar protocol questions. It also improved its decisions about requesting confirmation for some unsupported questions.

However, unsupported assertions remained possible. Training improved performance on the evaluation set without eliminating the risk of hallucination.

## Homework

### Level attempted

**Implementation**

### Settings or data changed

I replaced the original fictional course FAQ with a fictional ICF annotation protocol to explore its potential relevance to clinical annotation research.

The protocol contained five rules:

1. Assign ICF codes only when the clinical description provides sufficient evidence.
2. Record severity on a scale from 0 to 4.
3. Flag cases with missing clinical information for human review.
4. Require human assessment of conflicting annotations.
5. Include both ICF code and severity fields in prediction records.

I created grounded questions using paraphrases of these rules and ungrounded questions asking about information absent from the protocol, such as specific clinical codes, severity assignments, training requirements, and evaluation thresholds.

For ungrounded questions, the expected output contained `needs_review: true` and the phrase "Confirmation is needed."

I kept the original JSON output format and LoRA training configuration.

### Results

The main evaluation improved from 19.05% to 100% content accuracy across 21 questions, with format compliance increasing from 95.24% to 100%.

However, supplementary questions revealed that the trained model could still make unsupported assertions. The ethics committee example was particularly informative because the original model requested review, while the fine-tuned model made an unsupported claim.

### Additional experiment: 4-bit quantization

I also compared the untrained model in 32-bit and 4-bit precision.

| Metric | 32-bit | 4-bit |
|---|---:|---:|
| Model weight-memory footprint | 3.01 GB | 0.76 GB |
| Format compliance | 95.24% | 100% |
| Content accuracy | 19.05% | 14.29% |
| Evaluation time | 27.6 s | 29.3 s |

Quantization reduced the measured weight-memory footprint by approximately 74.8%. Content accuracy decreased by one question, although this small difference is insufficient to establish a general performance disadvantage.

This was an inference-only quantization experiment, not QLoRA training.

### Discussion: When is fine-tuning suitable?

Fine-tuning is suitable when a task requires a consistent output structure, terminology, or response pattern, and representative training examples are available. In this experiment, LoRA successfully adapted the model to the fictional ICF protocol and its required JSON output.

However, fine-tuning alone is insufficient when a task requires reliable handling of missing evidence, unfamiliar clinical situations, or uncertain decisions. The supplementary knowledge test demonstrated that the model could still produce unsupported claims after achieving perfect scores on the main evaluation.

For a real ICF annotation system, I would consider combining explicit coding rules, evidence retrieval, uncertainty assessment, and human review. Evaluation should include independent clinical examples, reliable reference annotations, and measures beyond exact keyword matching.

The most important finding was that **high evaluation accuracy and reliable evidence-based judgment are distinct properties**.
