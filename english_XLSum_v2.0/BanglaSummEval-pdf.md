BanglaSummEval: Reference-Free Factual Consistency
Evaluation for Bangla Summarization
Ahmed Rafid1,∗, Rumman Adib1, , Fariya Ahmed1,
∗ ∗
Ajwad Abrar1, Mohammed Saidul Islam2
1Department of Computer Science and Engineering,
Islamic University of Technology, Bangladesh
2York University, Canada
{ahmedrafid, rummanadib, fariyaahmed, ajwadabrar}@iut-dhaka.edu,
saidulis@yorku.ca
Abstract summarization (Zhang et al., 2025). Profes-
sionalsoftenhavetodealwithlargevolumesof
Evaluating factual consistency is essen- data, where relevant information is frequently
tial for reliable text summarization, par- buried under irrelevant statements. LLMs can
ticularly in high-stakes domains such as
assist by summarizing reports and filtering
healthcare and news. However, most ex-
out important information (Khan et al., 2023).
isting evaluation metrics overlook Bangla,
Therefore, it is essential that LLM-generated
a widely spoken yet under-resourced lan-
guage, and often depend on reference sum- summariesretainimportantinformationwhile
maries. We introduce BanglaSummEval, remaining factually consistent with the source
a reference-free, question-answering-based text.
framework for evaluating factual consis- Consequently, an evaluation metric that
tency in Bangla summarization. The pro-
can precisely measure factual consistency be-
posed method assesses both factual ac-
tween a source document and its summary
curacy and content coverage through au-
is crucial for comparing LLM performance
tomatically generated questions and an-
in terms of generating summaries. We ex-
swers derived from the source document
and the summary. A single multilingual plored several factual evaluation metrics and
instruction-tuned language model handles found that QuestEval (Scialom et al., 2021)
question generation, question answering, provides a robust evaluation framework with-
candidate answer extraction, and question out requiring human-annotated reference sum-
importance weighting. This unified de-
maries. QuestEval addresses key limitations
sign reduces system complexity and com-
of traditional metrics through its reference-
putational cost. To capture semantic con-
free, question-answering-based approach, eval-
sistency beyond surface-level overlap, we
use BERTScore-Recall for answer compar- uating both factual consistency and content
ison. We validate BanglaSummEval on relevance.
300human-writtensummariesfromeduca- However, none of the existing evaluation
tional and medical domains, demonstrat- metrics support Bangla, the seventh most spo-
ing strong correlation with expert human
ken language in the world, with over 240 mil-
judgments (Pearson’s r = 0.694, Spear-
lion speakers. While traditional lexical over-
man’s ρ = 0.763). By providing in-
lap metrics such as ROUGE and BLEU are
terpretable, step-wise diagnostics along-
widely used for summary evaluation, they are
sidereliableevaluationscores,BanglaSum-
mEval offers a practical and transparent fundamentally limited for factual consistency
solution for factual consistency evaluation assessment, as they rely on surface-level sim-
in low-resource language settings. ilarity rather than semantic accuracy. These
limitations are particularly severe for morpho-
1 Introduction
logically rich languages like Bangla, where
paraphrasing and flexible word order are com-
The integration of Large Language Models
mon. A factual consistency evaluation metric
(LLMs) into healthcare and other service sec-
for Bangla would facilitate the development
tors is increasing rapidly. For example, there
of more effective Bangla summarization mod-
is a growing use of LLMs for medical report
els. Inthispaper,wepresentBanglaSummEval,
∗These authors contributed equally to this work. an adaptation of the QuestEval framework for
595
ProceedingsoftheSecondWorkshoponLanguageModelsforLow-ResourceLanguages(LoResLM2026),pages595–608
March29,2026©2026AssociationforComputationalLinguistics

Bangla. Beyond providing Bangla language inference (NLI) (Bowman et al., 2015) model
support, our adaptation improves the trans- to predict if the source supports, refutes, or
parency of LLM evaluation by enabling step- is neutral towards each claim. FactScore ex-
wise analysis of the evaluation process. This tracts atomic factual statements from gener-
allows researchers to explicitly identify where ated outputs and validates them against the
LLMs fail and pinpoint instances of factual in- sourceusingretrievalandinference. QAFactE-
consistency or hallucination. Such diagnostic val is a question-answering-centric metric
capability facilitates targeted model improve- which creates a large pool of QA pairs derived
ments rather than treating factual evaluation from the candidate text and answers them
as an end-to-end score. Our major contribu- using the source, then compares the answers
tions are as follows: with reference-ground-truth answers or using
|       |           |                 |     |     |     |       | confidence | scores. |                |     |     |        |       |
| ----- | --------- | --------------- | --- | --- | --- | ----- | ---------- | ------- | -------------- | --- | --- | ------ | ----- |
| 1. We | introduce | BanglaSummEval, |     |     | the | first |            |         |                |     |     |        |       |
|       |           |                 |     |     |     |       | None       | of the  | aforementioned |     |     | highly | cited |
factualconsistencyevaluationmetricthat
|          |          |                 |     |     |        |     | metrics     | have                               | out-of-the-box |          |     | support      | for |
| -------- | -------- | --------------- | --- | --- | ------ | --- | ----------- | ---------------------------------- | -------------- | -------- | --- | ------------ | --- |
| supports | Bangla.  |                 |     |     |        |     |             |                                    |                |          |     |              |     |
|          |          |                 |     |     |        |     | Bangla.     | Infacttherearenoestablishedfactual |                |          |     |              |     |
| 2. We    | evaluate | BanglaSummEval, |     |     | demon- |     |             |                                    |                |          |     |              |     |
|          |          |                 |     |     |        |     | consistency |                                    | metrics        | designed |     | specifically | for |
stratingitsstrongcorrelationwithhuman Bangla, nor major open-source tools or bench-
| judgments |            | on factual |              | consistency.  |           |       |          |             |            |             |                 |          |         |
| --------- | ---------- | ---------- | ------------ | ------------- | --------- | ----- | -------- | ----------- | ---------- | ----------- | --------------- | -------- | ------- |
|           |            |            |              |               |           |       | marks    | tailored    | to this    | language.   |                 | This     | lack of |
|           |            |            |              |               |           |       | coverage | presents    | a          | significant |                 | research | oppor-  |
| 3. We     | enhance    | the        | transparency |               | of        | LLM-  |          |             |            |             |                 |          |         |
|           |            |            |              |               |           |       | tunity   | considering |            | the growing |                 | use of   | LLMs    |
| based     | evaluation |            | by           | incorporating |           | step- |          |             |            |             |                 |          |         |
|           |            |            |              |               |           |       | and the  | distinct    | linguistic |             | characteristics |          | in      |
| wise      | analysis   | and        | explicit     | error         | localiza- |       |          |             |            |             |                 |          |         |
Bangla.
| tion.This |               | enables | precise | identification |     | of  |         |          |           |        |                |             |     |
| --------- | ------------- | ------- | ------- | -------------- | --- | --- | ------- | -------- | --------- | ------ | -------------- | ----------- | --- |
|           |               |         |         |                |     |     | Our     | proposed |           | metric | BanglaSummEval |             |     |
| factual   | failure       | points. |         |                |     |     |         |          |           |        |                |             |     |
|           |               |         |         |                |     |     | works   | to fill  | this      | gap    | using          | an approach |     |
| Figure    | 1 illustrates |         | the     | architecture   |     | of  |         |          |           |        |                |             |     |
|           |               |         |         |                |     |     | similar | to       | QuestEval |        | (QA-           | based       | and |
BanglaSummEval.
|                  |                  |            |            |         |       |        | referenceless). |      | Prior    |             | studies   | have        | shown   |
| ---------------- | ---------------- | ---------- | ---------- | ------- | ----- | ------ | --------------- | ---- | -------- | ----------- | --------- | ----------- | ------- |
| 2 Related        |                  | Work       |            |         |       |        | QuestEval’s     |      | superior | correlation |           | with        | human   |
|                  |                  |            |            |         |       |        | judgment        | in   | factual  | consistency |           | assessments |         |
| Domains          | like healthcare, |            | education, |         | news  | are    |                 |      |          |             |           |             |         |
|                  |                  |            |            |         |       |        | compared        | to   | metrics  | like        | BERTScore |             | and     |
| highly sensitive |                  | to factual |            | errors, | where | relia- |                 |      |          |             |           |             |         |
|                  |                  |            |            |         |       |        | ROUGE.          | Thus | our      | metric      | does      | not         | require |
bility is the priority. Some of the key influ- human-written reference summaries or labels,
ential metrics currently available for such crit- making it more scalable for low-resource lan-
| ical evaluation |        | are QAGS |        | (Tam      | et al., | 2023), |                |              |          |             |              |                |        |
| --------------- | ------ | -------- | ------ | --------- | ------- | ------ | -------------- | ------------ | -------- | ----------- | ------------ | -------------- | ------ |
|                 |        |          |        |           |         |        | guages         | like Bangla. |          | It produces |              | interpretable, |        |
| SummaC          | (Laban | et al.,  | 2022), | FactScore |         | (Min   |                |              |          |             |              |                |        |
|                 |        |          |        |           |         |        | question-based |              | outputs, |             | facilitating |                | deeper |
et al., 2023), QuestEval (Scialom et al., 2021) analysis of model errors.
| , QAFactEval |          | (Fabbri    | et  | al., 2022) | which | il-  |               |     |     |     |     |     |     |
| ------------ | -------- | ---------- | --- | ---------- | ----- | ---- | ------------- | --- | --- | --- | --- | --- | --- |
| lustrate     | the core | approaches |     | currently  | in    | this |               |     |     |     |     |     |     |
|              |          |            |     |            |       |      | 3 Methodology |     |     |     |     |     |     |
field.
QuestEval is an advanced metric that eval- In this section, we describe our adaptation
uates factuality in summaries and text genera- of the QuestEval framework for evaluating
tionbygeneratingandansweringquestionsus- Bangla summarization. While we retain the
ing both the generated output and the source. core mathematical formulation of precision
Unlikemanymetrics,QuestEvaldoesnotneed and recall defined in QuestEval, our method,
gold-reference annotations and assesses both BanglaSummEval (see Figure 1), introduces
recall and precision by generating questions a unified model architecture with model spe-
from each side. It delivers robust correla- cific answer confidence calculation and seman-
tion with human assessments and facilitates tic scoring to suit low-resource Bangla eval-
explainable diagnostics, highlighting gaps in uation.Though we largely retain the archi-
specific information coverage. tecture and core pipeline of QuestEval, our
SummaC decomposes a machine-generated major contributions lie in the extensions re-
summary into individual factual claims or sen- quired to make the framework effective and
tences, then formulates the natural language reliable for Bangla.This includes identifying
596

|     |     | Figure | 1: Overview |     | of the proposed | BanglaSummEval |     | architecture. |     |     |     |     |
| --- | --- | ------ | ----------- | --- | --------------- | -------------- | --- | ------------- | --- | --- | --- | --- |
pre-trained and fine-tuned models suitable for Semanticsimilarity BERT-P BERT-R BERT-F1
| this architecture |     | in  | Bangla | and | evaluating |     |     |     | BanglaT5 |     |     |     |
| ----------------- | --- | --- | ------ | --- | ---------- | --- | --- | --- | -------- | --- | --- | --- |
their performance using task-specific datasets. QA 0.55 0.55 0.65 0.59
|                 |     |              |     |      |          | QG  |     | 0.61 |     | 0.61 | 0.68 | 0.64 |
| --------------- | --- | ------------ | --- | ---- | -------- | --- | --- | ---- | --- | ---- | ---- | ---- |
| BanglaSummEval, |     | instantiates |     | four | key com- |     |     |      |     |      |      |      |
mT5-Base
| ponents:                  | question | answering |     | (QA),         | question   |     |     |      |     |      |      |      |
| ------------------------- | -------- | --------- | --- | ------------- | ---------- | --- | --- | ---- | --- | ---- | ---- | ---- |
|                           |          |           |     |               |            | QA  |     | 0.59 |     | 0.59 | 0.64 | 0.61 |
| generation                | (QG),    | candidate |     | answer        | extraction |     |     |      |     |      |      |      |
|                           |          |           |     |               |            | QG  |     | 0.61 |     | 0.61 | 0.64 | 0.62 |
| (NER)andthequeryweighter. |          |           |     | Itusesasingle |            |     |     |      |     |      |      |      |
Qwen3-8B-bnb-4bit
unified large language model (LLM). This uni- QA 0.62 0.62 0.73 0.67
fied approach reduces deployment complexity QG 0.75 0.75 0.79 0.77
| and computational |     | overhead. |              |     |     |          |            | Qwen3-14B-bnb-4bit |         |      |            |      |
| ----------------- | --- | --------- | ------------ | --- | --- | -------- | ---------- | ------------------ | ------- | ---- | ---------- | ---- |
|                   |     |           |              |     |     | QA       |            | 0.63               |         | 0.63 | 0.72       | 0.67 |
|                   |     |           |              |     |     | QG       |            | 0.76               |         | 0.76 | 0.82       | 0.79 |
| 3.1 Unified       |     | Model     | Architecture |     |     |          |            |                    |         |      |            |      |
|                   |     |           |              |     |     | Table 1: | Evaluation |                    | Metrics |      | Comparison | for  |
We employ a 4-bit quantized version of the BanglaT5, mT5-Base, Qwen3-8B-bnb-4bit, and
| Qwen3-14B-Instruct |              | model     |            | (Yang et        | al., 2025) |                    |     |             |     |          |          |       |
| ------------------ | ------------ | --------- | ---------- | --------------- | ---------- | ------------------ | --- | ----------- | --- | -------- | -------- | ----- |
|                    |              |           |            |                 |            | Qwen3-14B-bnb-4bit |     |             | on  | QA       | and QG   | Tasks |
| provided           | by Unsloth   |           | named      | Qwen3-14B-bnb-  |            | (BanglaRQA         |     | Dataset)    |     |          |          |       |
| 4bit as            | the backbone |           | for all    | four components |            |                    |     |             |     |          |          |       |
| (QA, QG,           | NER          | and query | weighter). |                 |            |                    |     |             |     |          |          |       |
|                    |              |           |            |                 |            | weprompted         |     | eachmodelto |     | generate | twoques- |       |
| For                | selecting    | the       | best       | backbone,       | a sys-     |                    |     |             |     |          |          |       |
tematic benchmarking was conducted on the tions per passage and compared the generated
|            |                    |         |     |                |      | questions | against |          | ground-truth |      | questions   | us- |
| ---------- | ------------------ | ------- | --- | -------------- | ---- | --------- | ------- | -------- | ------------ | ---- | ----------- | --- |
| four large | language           | models: |     | BanglaT5,      | mT5- |           |         |          |              |      |             |     |
|            |                    |         |     |                |      | ing the   | same    | metrics. |              | This | yielded 300 | QA  |
| Base,      | Qwen3-8B-bnb-4bit, |         |     | and Qwen3-14B- |      |           |         |          |              |      |             |     |
bnb-4bit. These models have been evalu- pairs and 300 QG pairs for comprehensive as-
ated on the BanglaRQA (Ekram et al., 2022) sessment of both capabilities.
corpus. We evaluated each model’s ques- As shown in Table 1, the model with
tion answering (QA) and question generation the best performance for all evaluation met-
(QG) capabilities using 150 passages from the rics (BERTScore-F1: 0.67 QA, 0.79 QG)
dataset. For QA evaluation, we prompted was Qwen3-14B-bnb-4bit. Qwen3-8B-bnb-
each model to answer two ground-truth ques- 4bit was a close competitor to Qwen3-14B-
tions per passage and measured answer simi- bnb-4bit, and the performance of BanglaT5
larityusingBERTScore(Precision/Recall/F1) and mT5 was quite low which makes the ef-
and semantic similarity. For QG evaluation, fectiveness of instruction tuning in multiple
597

languages highly evident. Qwen3-14B-bnb- question q using the QG prompt:
| 4bit was | therefore | chosen | based | on  | excellent |     |     |     |     |     |     |
| -------- | --------- | ------ | ----- | --- | --------- | --- | --- | --- | --- | --- | --- |
multi-lingual ability in low-resource environ- q = QG(C,r) (1)
ments, theabilitytofollowtheBanglainstruc-
tion set and resource eﬀiciency. Through our To ensure the generated question is valid
single model paradigm based on task-specific andanswerablewefeedthegeneratedquestion
statements shown in Appendix A.1, it is en- q back into the QA component with context
|            |     |        |            |     |           | to obtain | a   | predicted | answer |     | QA(C,q). |
| ---------- | --- | ------ | ---------- | --- | --------- | --------- | --- | --------- | ------ | --- | -------- |
| sured that | our | entire | evaluation |     | framework | C         |     |           |        | a   | =        |
is lightweight and can be executed on a low- The pair (q,r) is accepted if and only if the
resource environment such as a free tier cloud semantic similarity between the predicted an-
GPU environment (Kaggle/Colab). swer a and the original candidate r is equal to
|     |     |     |     |     |     | or greater | than | a threshold |     | τ (see | Appendix |
| --- | --- | --- | --- | --- | --- | ---------- | ---- | ----------- | --- | ------ | -------- |
A.3):
| 3.2 Candidate |     | Answer | Extraction |     |     |     |     |     |     |     |     |
| ------------- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
Reference-less evaluation requires extracting (q,r) (C) sim(a,r) τ (2)
|             |     |            |     |      |             |     | ∈   | P   | ⇐⇒  |     | ≥   |
| ----------- | --- | ---------- | --- | ---- | ----------- | --- | --- | --- | --- | --- | --- |
| information | or  | facts from | the | text | to serve as |     |     |     |     |     |     |
ground-truthanswersforgeneratingquestions.
|     |     |     |     |     |     | where | sim( | , ) is a | semantic | similarity | func- |
| --- | --- | --- | --- | --- | --- | ----- | ---- | -------- | -------- | ---------- | ----- |
· ·
Following previous work (Wang et al., 2020), tion described below.
| we focus | on named | entities | and | nouns | as can- |              |     |            |     |        |     |
| -------- | -------- | -------- | --- | ----- | ------- | ------------ | --- | ---------- | --- | ------ | --- |
|          |          |          |     |       |         | 3.4 Semantic |     | Similarity |     | Metric |     |
didate answers.
Large language models have been shown to Unlike the original QuestEval, which uses
perform comparably to supervised baselines token-level F1 score for answer comparison,
on NER tasks, with particularly strong per- we employ BERTScore Recall (Zhang et al.,
formance in low-resource settings (Dai et al., 2020)tocapturesemanticsimilarityinBangla.
2023),andQwen3’sextensivemultilingualpre- Semantic similarity is used only for compari-
training across 119 languages (Yang et al., son between ground truths and answer gener-
2025) makes it well-suited for Bengali named ated on questions asked since document-level
entity extraction. Thus, to keep our frame- similarity metrics are fundamentally limited
| work light, | we reused |     | Qwen3-14B-bnb-4bit |     | as  |                |     |             |     |       |            |
| ----------- | --------- | --- | ------------------ | --- | --- | -------------- | --- | ----------- | --- | ----- | ---------- |
|             |           |     |                    |     |     | for factuality |     | evaluation. |     | As Ye | et al. ob- |
a Bangla named entity and noun extractor us- serve,“similarity-basedmetricsareinsuﬀicient
ing specific prompts (Appendix A.1.3) , which for precisely detecting factual errors, because
aligns with our unified model approach and high similarity cannot guarantee factual con-
removes the necessity of using any external sistency” (Ye et al., 2024). By decompos-
NER models which would consume additional ing evaluation into atomic QA pairs, we over-
resources in an already resource constrained come this limitation by isolating specific fac-
| setup.   |           |           |           |           |         | tual claims | for        | targeted | comparison. |         |     |
| -------- | --------- | --------- | --------- | --------- | ------- | ----------- | ---------- | -------- | ----------- | ------- | --- |
|          |           |           |           |           |         | The         | similarity | function | is          | defined | as: |
| The NER  | component |           | takes     | a context | C and   |             |            |          |             |         |     |
| produces | a set     | of unique | candidate |           | answers |             |            |          |             |         |     |
(C), consisting of named entities and nouns sim(x,y) = BERTScore (y,x) (3)
R
G
| present          | in C. |                    |     |     |     |           |                    |           |            |         |              |
| ---------------- | ----- | ------------------ | --- | --- | --- | --------- | ------------------ | --------- | ---------- | ------- | ------------ |
|                  |       |                    |     |     |     | where x   | is the             | reference | answer     |         | and y is the |
|                  |       |                    |     |     |     | candidate | answer.            |           |            |         |              |
| 3.3 Constructing |       | Answer-Conditioned |     |     |     |           |                    |           |            |         |              |
|                  |       |                    |     |     |     | For       | the document-level |           |            | summary | evalua-      |
| Question         |       | Sets               |     |     |     |           |                    |           |            |         |              |
|                  |       |                    |     |     |     | tion, the | traditional        |           | similarity |         | metrics such |
Both precision and recall metrics in our frame- as ROUGE or BLEU underperform since
work rely on a set of high-quality question- they are based on surface-level lexical over-
answer pairs derived from a source text. For a lap, which cannot effectively handle the mor-
given context C (either the source document phological richness of the Bangla language or
D or the summary S), we construct a filtered paraphrasing. Contrastively, BERTScore is
set of pairs through a similarity based appropriateforanswer-levelcomparisoninour
(C)
P
filtering process. First, for each candidate an- QA framework. The key distinction lies in
swer r (C), we generate a corresponding granularity: our decomposition into atomic
|     | ∈ G |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
598

Metric Pearson_r Pearson_p MAE RMSE hibit stronger correlation with human judg-
SemanticMetrics ments than lexical and character-level alter-
BERTScore-Recall 0.673 6.12E-41 29.317 43.194
natives. BERTScore-Recall, computed us-
BERTScore-F1 0.624 1.02E-33 29.896 42.975
CosineSimilarity 0.592 1.04E-29 26.511 33.845 ingXLM-RoBERTa-base, achievesthehighest
LexicalMetrics Pearson correlation (r = 0.673) and the low-
chrF 0.666 8.88E-40 27.273 37.215
Token-F1 0.496 4.61E-20 41.343 55.217 est p-value, indicating a strong and statisti-
BLEU 0.249 1.30E-05 60.761 72.391
cally significant alignment with human judg-
ExactMatch 0.296 1.91E-07 54.433 69.831
ments. This is followed by BERTScore-F1
Character-levelMetrics
CERSimilarity 0.470 7.43E-18 39.744 54.495 (r = 0.624) and cosine similarity (r = 0.592),
WERSimilarity 0.366 5.69E-11 50.266 65.489
both showing moderate-to-strong correlations.
Table2: Correlationofautomaticmetricswithhu- These results confirm that semantic similar-
man judgments on Bangla. ity metrics are more robust for evaluating fac-
tual consistency in Bangla, as they capture
meaning beyond surface-level lexical overlap.
QA pairs transforms the problem from holis-
Consequently, we select BERTScore-Recall for
tic document similarity to targeted verifica-
BanglaSummEval, as it enables accurate com-
tion of individual factual claims. For answer-
parison even when answers are phrased differ-
level comparison, the answer is typically a
ently but convey equivalent meaning.
shortentitymentionornounphrase,forwhich
BERTScore’s semantic embeddings excel at 3.5 Precision: Verification against
capturing meaning despite morphological vari- Source
ationbetweendifferentexpressionsofthesame
Precision measures the extent to which infor-
fact. Unlike document-level metrics that con-
mation in the summary S is supported by the
flate multiple quality dimensions, answer-level
source document D. We first generate the
BERTScore focuses exclusively on the seman-
setofself-validatedquestion-answerpairsfrom
tic equivalence of specific facts, which directly
the summary, (S). We then attempt to an-
addresses factual consistency verification. By P
swer these questions using the source docu-
utilizing contextualized embeddings from mul-
ment D as context. The precision score is cal-
tilingual models such as XLM-RoBERTa-base
culated as the average semantic similarity be-
(Conneauetal.,2019), BERTScore-Recallcan
tween the summary-derived answers and the
robustly capture semantic meaning across lex-
source-derived answers:
ically different but factually equivalent expres-
sions, making it highly suitable for factual ver- 1
Prec(D,S) = sim(QA(D,q),r)
ification in our decomposed abstractive sum- (S)
marization evaluation framework.
|P | (q,r∑)
∈P
(S)
(4)
To empirically validate this choice, we A high precision score indicates that the
benchmarked lexical, semantic, and hybrid claims made in the summary (represented by
metrics against human-annotated scores using r) are consistent with the information retriev-
300 stratified samples from the BanglaRQA able from the source document.
dataset (Ekram et al., 2022). Answers were
generated using TigerLLM-1B-it (Raihan and 3.6 Recall: Coverage of Important
Zampieri, 2025) and evaluated by human an- Information
notators (the annotation guideline is provided Recall measures how much of the key infor-
in Appendix C), each with over 14 years of ex- mation from the source document D is pre-
perience in the Bangla language. Annotators served in the summary S. We generate the
rated factual accuracy on a continuous scale set of question-answer pairs from the source,
from 0.0 to 1.0. Correlation with human judg- (D). FollowingQuestEval,insteadofstrictly
P
ments was measured using Pearson’s correla- comparing answer strings, we measure the an-
tion coeﬀicient (r) and Spearman’s rank corre- swerability of each source question given the
lation coeﬀicient (ρ), along with MAE, RMSE, summary. We define an answerability score
and L2-norm deviation. Ans(S,q) based on the model’s confidence
As shown in Table 2, semantic metrics ex- in generating an answer versus producing an
599

Human
Source Summary BanglaSummEval
Score
মানুেষর সুন্দর মুখ েদেখ আনিন্দত হেয়া না।
সব্ভােব েস সুন্দর নয়, েদখেত সুন্দর হেলও
তার সব্ভাব, তার স্পশর্, তার রীিতনীিতেক মা- বািহয্ক েসৗন্দযর্ নয়, সব্ভােবর েসৗন্দযর্ই মানুষ-
নুষঘৃণাকের।দুঃসব্ভােবরমানুষমানুেষরহৃদ-
েক িবচােরর মাপকািঠ। খারাপ সব্ভােবর মানু-
েয়জব্ালাওেবদনােদয়।তারসুন্দরমুেখমানুষ
ষও বািহয্ক েসৗন্দেযর্র অিধকারী হেত পাের।
তৃিপ্ত পায় না। অেবাধ েলােকরা মানুেষর রূপ 0.73 0.76
আর যারা খারাপ সব্ভােবর তারাও সুন্দর সব্ভা-
েদেখমুগ্ধহয়এবংতারফলেভাগকের।যার
েবরমানুষেকপছন্দকের।তাইকেঠারপিরশৰ্ম
সব্ভাব মন্দ, েস িনেজও দুিষ্কৰ্য়াশীল, িমথয্াবাদী,
ও সাধনার মাধয্েম সুন্দর সব্ভােবর অিধকারী
দুমর্িতেকঘৃণাকের।মানুষিনেজসব্ভােবসুন্দর
হেত হেব।
নাহেলওেসসব্ভােবরেসৗন্দযর্েকভােলাবােস।
সব্ভাবগঠেনকিঠনপিরশৰ্মওসাধনাচাই,নই-
েল শয়তানেক পরািজত করা সম্ভব নয়।
আমার ১০ . ০৯ . ১৯ তািরখ েথেক েডঙ্গু
জব্র হইেছ । আজেক ১০ িদন হল । এনএস১
পিজিটভ আসেছ । এর পর েথেক প্লািটেলট আমার ১০ . ০৯ . ১৯ তািরখ েথেক েডঙ্গু
কেম যািচ্ছল । গত ৩ িদন যাবত প্লািতেলট
জব্র , আজেক ১০ িদন হল । এনএস ১ পিজ-
বাড়েছ।সবর্েশষআজেকরিরেপােটর্১৫০০০০ 0.77 0.77
িটভআসেছ।প্লািটেলটকেমযািচ্ছল,৩িদন
আসেছ । আমার শরীর িকছুটা দুবর্ল । এছাড়া
যাবত প্লািতেলট বাড়েছ । আজেকর িরেপােটর্
আর েতমন েকান সমসয্া েনই । আিম কখন
১৫০০০০ আসেছ । শরীর িকছুটা দুবর্ল ।
বুঝেত পারব েয আমার েডঙ্গু জব্র ভাল হেয়
েগেছ । আমার িক আর িসিভিস েটস্ট করার
দরকার আেছ ?
Table 3: Example evaluation samples from BanglaSummEval (see Appendix B for English translation)
unanswerable token. Let aˆ be the answer gen- and nouns but not all of these named enti-
erated by the model for question q given sum- ties carry important facts about the source
mary S, and let ϵ be a representative unan- D. Thus, questions generated from them do
swerable string (e.g., “unanswerable”). We not contribute equally to the factual evalua-
computethelength-normalizedlog-probability tion of a summary. Some questions capture
for a sequence y as: central facts or entities critical to the docu-
ment’s meaning (e.g., “Who performed the ac-
y
ℓ(y) = 1 | | logP(y S,q,y ) (5) tion?” or “What was the main outcome?”),
t <t
y | while others correspond to peripheral details.
| | ∑ t=1
To account for this variance in informational
The answerability score is then defined as the
importance, we used a query weighter compo-
normalized probability of the candidate an-
nent. The predicted query weights are used to
swer relative to the unanswerable candidate:
compute the weighted recall score in Eq. 7.
exp(ℓ(aˆ))
Ans(S,q) = (6) The weighting mechanism is implemented
exp(ℓ(aˆ))+exp(ℓ(ϵ))
using the same unified Qwen3-14B-bnb-4bit
To account for the relative importance of dif-
model through a lightweight scoring prompt
ferent facts, we employ a query weighting
(seeAppendixA.1.4). Thismodelwasselected
function W(q,D) [0,1], which predicts the
basedonpreliminaryhumanevaluation,which
∈
importance of a question q given the source
demonstrated its ability to produce reliable
D (more details in the next section). The
and consistent weighting judgments. Reusing
weighted recall is computed as:
the same model across components also helps
W(q,D) Ans(S,q) keep the overall framework lightweight and
Rec(D,S) = (q,r) ∈P (D) W(q · ,D) avoidsintroducingadditionalmodeldependen-
∑ (q,r) (D)
∈P (7) cies.
∑
Given a question and its source context, the
3.7 Query Weighter: Importance
model is asked to numerically rate the ques-
Weighted Evaluation
tion’s importance on a continuous scale from
The NER module, responsible for generating 0.0(trivialorirrelevant)to1.0(highlycentral).
candidate answers, extracts named entities The prompt explicitly distinguishes between
600

high-importance questions which contain core biased toward Qwen3-generated content, we
entities, events, or relationships as well as low- deliberately selected summaries from diverse
importanceonesrelatedtominororabsentde- sources: the NCTB dataset, which were
tails. The final recall computation therefore written by professional human writers and
becomes a weighted aggregation where each edited for curriculum relevance, and from
question contributes proportionally to its esti- BanglaCHQ-Summ, which were created by six
mated informativeness. This ensures that fac- medical informatics experts (four experts in
tual consistency evaluation remains sensitive medical informatics and two experts in both
totherelativeimportanceofinformationunits medical informatics and medicine) following
rather than treating all factual elements uni- standardized annotation guidelines. All 300
| formly.   |        |     |     |     |     |     | summaries  | in    | our        | evaluation |      | set are      | human- |
| --------- | ------ | --- | --- | --- | --- | --- | ---------- | ----- | ---------- | ---------- | ---- | ------------ | ------ |
|           |        |     |     |     |     |     | written    | which | eliminates |            | any  | potential    | eval-  |
| 3.8 Final | Metric |     |     |     |     |     |            |       |            |            |      |              |        |
|           |        |     |     |     |     |     | uator bias | that  | could      | arise      | from | preferential |        |
The final BanglaSummEval score is the har- scoring of Qwen3-generated content. Three
| monic mean | of  | the precision |     | and | recall | scores, |               |     |          |      |     |       |        |
| ---------- | --- | ------------- | --- | --- | ------ | ------- | ------------- | --- | -------- | ---- | --- | ----- | ------ |
|            |     |               |     |     |        |         | native Bangla |     | speakers | with | 14+ | years | of ex- |
providing a balanced measure of factual con- perience rated each summary’s factual con-
sistency and important content coverage: sistency on a 0–1 scale. Table 5 shows
|            |     |             |     |          |     |     | strong   | correlation |          | across | all    | metrics.     | Pear- |
| ---------- | --- | ----------- | --- | -------- | --- | --- | -------- | ----------- | -------- | ------ | ------ | ------------ | ----- |
|            |     | 2 Prec(D,S) |     | Rec(D,S) |     |     |          |             |          |        |        |              |       |
|            |     |             |     |          |     |     | son’s r, | which       | measures |        | linear | relationship |       |
| Score(D,S) | =   | ·           |     | ·        |     | (8) |          |             |          |        |        |              |       |
Prec(D,S)+Rec(D,S)
|     |     |     |     |     |     |     | between | BanglaSummEval |     |     | scores | and | human |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------------- | --- | --- | ------ | --- | ----- |
4 Results Analysis judgements shows a value of 0.694, indicating
|     |     |     |     |     |     |     | a moderately |     | strong | positive |     | correlation | be- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------ | -------- | --- | ----------- | --- |
4.1 Computational Eﬀiciency tween human judgement and our framework
We evaluate BanglaSummEval’s computa- whilsttheextremelylowp-value(3.84 10 11)
−
×
tional cost on a single NVIDIA T4 GPU confirms that the correlation is highly statisti-
|             |     |           |     |     |          |     | cally significant. |     |     |     |     |     |     |
| ----------- | --- | --------- | --- | --- | -------- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
| (16GB VRAM) |     | available |     | on  | Kaggle’s | or  |                    |     |     |     |     |     |     |
Google Colab’s free tier. Table 4 reports av- Spearman’s ρ which measures the mono-
erage execution times and memory (VRAM) tonic relationship using rank-based correla-
|              |           |     |          |          |     |     | tion shows     | a   | value | of 0.763, | suggesting |     | that      |
| ------------ | --------- | --- | -------- | -------- | --- | --- | -------------- | --- | ----- | --------- | ---------- | --- | --------- |
| usage across | different |     | document | lengths. |     |     |                |     |       |           |            |     |           |
|              |           |     |          |          |     |     | BanglaSummEval |     | ranks | summaries |            |     | in a very |
DocumentLength Time(Min) Memory(GB) QAPairs similar order to human evaluations with the p-
Short( 10entities) 10 12.7 8–12 value showing extreme statistical significance.
∼
Medium( 20entities) 25 12.7 16–22 Kendall’sτ valueof0.644alsoindicatesstrong
∼
Long( 30+entities) 55 12.7 28–35 agreement between our framework and human
∼
|                |           |            |     |          |          |     | judgement.     | The | coeﬀicient |      | of             | determination |        |
| -------------- | --------- | ---------- | --- | -------- | -------- | --- | -------------- | --- | ---------- | ---- | -------------- | ------------- | ------ |
| Table 4:       | Execution | time       | and | memory   | usage    | for |                |     |            |      |                |               |        |
|                |           |            |     |          |          |     | R2 of 0.481    |     | indicates  | that |                |               |        |
| BanglaSummEval |           | on varying |     | document | lengths. |     |                |     |            |      | BanglaSummEval |               |        |
|                |           |            |     |          |          |     | scores explain |     | 48.1%      | of   | the            | variance      | in hu- |
The evaluation pipeline processes an aver- man judgments. While not perfect, owing
age document-summary pair in approximately to the fact that human judgments inherently
|             |      |        |         |       |     |        | contain | subjective |     | variations |     | this evaluation |     |
| ----------- | ---- | ------ | ------- | ----- | --- | ------ | ------- | ---------- | --- | ---------- | --- | --------------- | --- |
| 25 minutes, | with | linear | scaling | based |     | on the |         |            |     |            |     |                 |     |
number of extracted entities. The 4-bit quan- score is a reasonable fit. Mean Absolute Er-
tization keeps peak memory (VRAM) under ror (MAE) of 0.020 indicates that on average,
|                 |     |            |     |              |     |       | BanglaSummEval |          | scores   | deviate |             | by only     | 2 per-  |
| --------------- | --- | ---------- | --- | ------------ | --- | ----- | -------------- | -------- | -------- | ------- | ----------- | ----------- | ------- |
| 13GB, enabling  |     | deployment |     | on free-tier |     | cloud |                |          |          |         |             |             |         |
| GPUs.           |     |            |     |              |     |       | centage        | points   | from     | human   | scores,     | suggesting  |         |
|                 |     |            |     |              |     |       | high practical |          | accuracy | in      | score       | prediction. |         |
| 4.2 Correlation |     | Analysis   |     |              |     |       |                |          |          |         |             |             |         |
|                 |     |            |     |              |     |       | Since          | no prior | factual  |         | consistency |             | evalua- |
We validated BanglaSummEval against ex- tion metric specifically designed or adapted
pert annotations on randomly sampled a to- for the Bangla language exists in the liter-
tal of 300 source-summary pairs both from ature, we could not perform direct compar-
NCTB dataset (Chowdhury et al., 2021) and isons with equivalent baselines. This positions
BanglaCHQ-Summ (Khan et al., 2023) (see BanglaSummEval as the first such metric for
Table 3). To ensure our evaluation is not Bangla summarization, and the reported cor-
601

Metric Value p-value models such as Qwen3-14B-bnb-4bit may still
inherit biases originating from high-resource
Pearson’s r 0.694 3.84 × 10 − 11
Spearman’s ρ 0.763 2.54 × 10 − 14 training data. Future work should therefore
Kendall’s τ 0.644 9.04 × 10 − 14 investigate bias mitigation strategies, includ-
R2 0.481 — ingadversarialevaluationandsystematicfeed-
MAE 0.020 — back from native Bangla speakers.
Table 5: Correlation analysis between
6 Conclusion
BanglaSummEval F1 scores and human judg-
ments (n=300). This paper introduced BanglaSummEval, a
reference-freeframeworkforevaluatingfactual
consistency in Bangla summarization. The
relations with human judgments serve as the
method combines question generation, ques-
primary benchmark for its effectiveness in this
tion answering, semantic comparison, and im-
low-resource setting.
portance weighting within a single multilin-
While BanglaSummEval does not claim to
gual instruction-tuned language model. This
fundamentally improve LLM hallucination de-
design enables interpretable evaluation with-
tection rates compared to end-to-end evalua-
out relying on gold-standard reference sum-
tion approaches, it provides a critical advan-
maries. Experiments on multiple Bangla sum-
tage by removing the black-box abstraction
marization datasets show strong correlation
inherent in holistic metrics. By decompos-
with expert human judgments. These results
ing the evaluation process into interpretable
validate BanglaSummEval as a reliable auto-
steps such as question and answer generation,
mated proxy for factual consistency assess-
semantic matching, and question importance
ment.
weighting, our framework enables researchers
to identify exactly where and why an LLM Beyond overall scores, BanglaSummEval
fails to detect factual inconsistencies. This provides step-wise diagnostic signals. These
step-by-step breakdown facilitates targeted di- signals help identify where factual inconsisten-
agnosisofmodelweaknesses,whetherinentity cies occur. This supports more targeted anal-
recognition, question formulation, or answer ysis of model behavior. By addressing the
generation, thereby supporting more informed lack of evaluation tools for Bangla, this work
model development and refinement. contributes to more reliable evaluation in low-
resource language settings. Future work will
These results validate BanglaSummEval as explore domain-specific adaptation, improved
an effective automated proxy for human eval- semanticencoders, andextensionstootherun-
uation in Bangla summarization, particularly derrepresented languages.
for applications requiring transparent, inter-
Limitations
pretable quality assessment.
There are several practical constraints that in-
5 Implications for Low-Resource
fluencedourframework’sdesignaswellitsper-
NLP Research
formance. First, we relied on lightweight mod-
This study advances linguistic fairness by en- els due to limited computational resources,
ablingfactualconsistencyevaluationforanun- ensuring compatibility with freely available
derrepresented language. The reference-free GPUs on platforms such as Google Colab
nature of the proposed framework removes re- and Kaggle. To minimize memory require-
liance on human-annotated summaries, facili- ments, we used a single shared model instance
tating faster and lower-cost evaluation. In ad- (Qwen3-14B-bnb-4bit) for multiple compo-
dition, the framework provides diagnostic in- nents, e.g. question generation, question an-
sightsintoLLMbehavior,allowingresearchers swering, and entity extraction, rather than
to identify specific failure modes in Bangla, deploying separate specialized models. To
such as hallucinations and stages where mod- further reduce memory usage and enable de-
els struggle to preserve factual information. ployment on limited VRAM environments, we
Despite these advantages, instruction-tuned adopted 4-bit quantization, which can lead to
602

References
| minor    | degradation |          | in model | precision. |              |     |        |            |             |       |             |             |         |
| -------- | ----------- | -------- | -------- | ---------- | ------------ | --- | ------ | ---------- | ----------- | ----- | ----------- | ----------- | ------- |
| Second,  | for         | semantic |          | similarity | scoring,     | we  |        |            |             |       |             |             |         |
|          |             |          |          |            |              |     | Samuel | R. Bowman, |             | Gabor | Angeli,     | Christopher |         |
| employed | BERTScore   |          | using    |            | XLM-RoBERTa- |     |        |            |             |       |             |             |         |
|          |             |          |          |            |              |     | Potts, | and        | Christopher |       | D. Manning. |             | 2015. A |
base, which, while eﬀicient, may not fully cap- large annotated corpus for learning natural lan-
ture subtle semantic nuances in Bangla com- guageinference. InProceedingsofthe2015Con-
|         |               |           |          |         |             |          | ference          | on          | Empirical | Methods       |     | in Natural   | Lan-   |
| ------- | ------------- | --------- | -------- | ------- | ----------- | -------- | ---------------- | ----------- | --------- | ------------- | --- | ------------ | ------ |
| pared   | to larger     | encoders. |          |         |             |          |                  |             |           |               |     |              |        |
|         |               |           |          |         |             |          | guage            | Processing, |           | pages632–642, |     | Lisbon,      | Portu- |
| Lastly, | the           | overall   |          | scoring | performance |          |                  |             |           |               |     |              |        |
|         |               |           |          |         |             |          | gal. Association |             | for       | Computational |     | Linguistics. |        |
| is not  | substantially |           | stronger |         | than        | directly |                  |             |           |               |     |              |        |
prompting a general-purpose LLM to assess Radia Rayan Chowdhury, Mir Tafseer Nayeem,
|                       |                  |     |            |         |               |       | Tahsin         | Tasnim      |     | Mim,          | Md.     | Saifur | Rahman     |
| --------------------- | ---------------- | --- | ---------- | ------- | ------------- | ----- | -------------- | ----------- | --- | ------------- | ------- | ------ | ---------- |
| summary               | quality.         |     | Our        | unified | architecture, |       |                |             |     |               |         |        |            |
|                       |                  |     |            |         |               |       | Chowdhury,     |             | and | Taufiqul      | Jannat. | 2021.  | Unsu-      |
| while computationally |                  |     | eﬀicient,  |         | introduces    | the   |                |             |     |               |         |        |            |
|                       |                  |     |            |         |               |       | pervised       | abstractive |     | summarization |         |        | of Bengali |
| risk of               | self-reinforcing |     | evaluation |         | loops.        | Since |                |             |     |               |         |        |            |
|                       |                  |     |            |         |               |       | textdocuments. |             |     | InProceedings |         | of the | 16th Con-  |
the same model performs extraction, question ference of the European Chapter of the Associ-
|                        |            |     |              |            |         |          | ation         | for Computational |              |     | Linguistics: |             | Main Vol- |
| ---------------------- | ---------- | --- | ------------ | ---------- | ------- | -------- | ------------- | ----------------- | ------------ | --- | ------------ | ----------- | --------- |
| generation,            | answering, |     | and          | weighting, |         | system-  |               |                   |              |     |              |             |           |
|                        |            |     |              |            |         |          | ume,          | pages             | 2612–2617,   |     | Online.      | Association | for       |
| atic misunderstandings |            |     | of           | the        | source  | text may |               |                   |              |     |              |             |           |
|                        |            |     |              |            |         |          | Computational |                   | Linguistics. |     |              |             |           |
| propagate              | through    |     | all pipeline |            | stages, | result-  |               |                   |              |     |              |             |           |
ing in internally consistent but factually in- Alexis Conneau, Kartikay Khandelwal, Naman
|         |              |     |     |       |     |         | Goyal, | Vishrav | Chaudhary, |     | Guillaume |     | Wenzek, |
| ------- | ------------ | --- | --- | ----- | --- | ------- | ------ | ------- | ---------- | --- | --------- | --- | ------- |
| correct | evaluations. |     | The | model | may | prefer- |        |         |            |     |           |     |         |
entially generate questions that it can confi- Francisco Guzmán, Edouard Grave, Myle Ott,
|        |         |             |     |         |     |           | Luke         | Zettlemoyer, |               | and | Veselin        | Stoyanov. | 2019.  |
| ------ | ------- | ----------- | --- | ------- | --- | --------- | ------------ | ------------ | ------------- | --- | -------------- | --------- | ------ |
| dently | answer, | potentially |     | missing |     | more dis- |              |              |               |     |                |           |        |
|        |         |             |     |         |     |           | Unsupervised |              | cross-lingual |     | representation |           | learn- |
criminative questions that would better test ing at scale. CoRR, abs/1911.02116.
factual consistency.
Thislimitationlargelyreflectstherestricted DaoyuanDaiand1others.2023. Gpt-ner: Named
|         |             |     |      |     |            |     | entity   | recognition |                 | via large | language | models.           | In  |
| ------- | ----------- | --- | ---- | --- | ---------- | --- | -------- | ----------- | --------------- | --------- | -------- | ----------------- | --- |
| ability | of existing |     | LLMs | to  | understand | and |          |             |                 |           |          |                   |     |
|         |             |     |      |     |            |     | Findings | of          | the Association |           |          | for Computational |     |
generate Bangla, rather than shortcomings of Linguistics: NAACL 2023.
| the framework |     | itself. | As  | more | capable | Bangla- |     |     |     |     |     |     |     |
| ------------- | --- | ------- | --- | ---- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
oriented or multilingual models become avail- SyedMohammedSartajEkram,AdhamArikRah-
|           |               |     |               |           |         |             | man,    | Md.     | Sajid   | Altaf, | Mohammed |            | Saidul Is- |
| --------- | ------------- | --- | ------------- | --------- | ------- | ----------- | ------- | ------- | ------- | ------ | -------- | ---------- | ---------- |
| able, the | framework     |     | can           | be        | readily | adapted     |         |         |         |        |          |            |            |
|           |               |     |               |           |         |             | lam,    | Mehrab  | Mustafy |        | Rahman,  | Md         | Mezbaur    |
| without   | architectural |     | modification. |           |         |             |         |         |         |        |          |            |            |
|           |               |     |               |           |         |             | Rahman, | Md      | Azam    |        | Hossain, | and        | Abu Rai-   |
| These     | trade-offs    |     | were          | necessary |         | to preserve |         |         |         |        |          |            |            |
|           |               |     |               |           |         |             | han     | Mostofa | Kamal.  |        | 2022.    | BanglaRQA: | A          |
accessibility and scalability for researchers benchmark dataset for under-resourced Bangla
languagereadingcomprehension-basedquestion
| working              | in low-resource |        |           | settings. | However, | fu-        |             |              |        |             |                 |             |          |
| -------------------- | --------------- | ------ | --------- | --------- | -------- | ---------- | ----------- | ------------ | ------ | ----------- | --------------- | ----------- | -------- |
|                      |                 |        |           |           |          |            | answering   |              | with   | diverse     | question-answer |             | types.   |
| ture versions        |                 | of the | framework |           | could    | investi-   |             |              |        |             |                 |             |          |
|                      |                 |        |           |           |          |            | In Findings |              | of the | Association |                 | for         | Computa- |
| gate mixed-precision |                 |        | or        | low-rank  |          | adaptation |             |              |        |             |                 |             |          |
|                      |                 |        |           |           |          |            | tional      | Linguistics: |        | EMNLP       |                 | 2022, pages | 2518–    |
techniques, as well as multi-model approaches 2532, Abu Dhabi, United Arab Emirates. Asso-
to address circular bias and better balance ef- ciation for Computational Linguistics.
| ficiency | with           | performance. |     |             |     |         |           |         |             |       |     |             |      |
| -------- | -------------- | ------------ | --- | ----------- | --- | ------- | --------- | ------- | ----------- | ----- | --- | ----------- | ---- |
|          |                |              |     |             |     |         | Alexander | Fabbri, | Chien-Sheng |       |     | Wu, Wenhao  | Liu, |
| While    | BanglaSummEval |              |     | effectively |     | detects |           |         |             |       |     |             |      |
|          |                |              |     |             |     |         | and       | Caiming | Xiong.      | 2022. |     | QAFactEval: | Im-  |
entity errors (incorrect names, numbers, proved QA-based factual consistency evalua-
dates), it has inherent limitations in captur- tion for summarization. In Proceedings of the
|             |     |              |         |      |            |          | 2022       | Conference |             | of the   | North             | American    | Chap- |
| ----------- | --- | ------------ | ------- | ---- | ---------- | -------- | ---------- | ---------- | ----------- | -------- | ----------------- | ----------- | ----- |
| ing complex |     | relational   | errors. |      | QuestEval, | the      |            |            |             |          |                   |             |       |
|             |     |              |         |      |            |          | ter of     | the        | Association |          | for Computational |             | Lin-  |
| framework   | we  | adapted,     |         | like | most       | QA-based |            |            |             |          |                   |             |       |
|             |     |              |         |      |            |          | guistics:  | Human      |             | Language | Technologies,     |             | pages |
| approaches  |     | is optimized |         | for  | atomic     | fact ex- |            |            |             |          |                   |             |       |
|             |     |              |         |      |            |          | 2587–2601, |            | Seattle,    | United   | States.           | Association |       |
traction and comparison. Sophisticated rela- for Computational Linguistics.
| tional           | errors | such       | as complex |              | causal | chains, |            |        |         |        |          |        |        |
| ---------------- | ------ | ---------- | ---------- | ------------ | ------ | ------- | ---------- | ------ | ------- | ------ | -------- | ------ | ------ |
|                  |        |            |            |              |        |         | Alvi Khan, |        | Fida    | Kamal, | Mohammad |        | Abrar  |
| implicit         | role   | reversals, |            | or multi-hop |        | tempo-  |            |        |         |        |          |        |        |
|                  |        |            |            |              |        |         | Chowdhury, |        | Tasnim  |        | Ahmed,   | Md     | Tah-   |
| ral dependencies |        |            | may be     | missed       | if     | the NER |            |        |         |        |          |        |        |
|                  |        |            |            |              |        |         | mid        | Rahman | Laskar, |        | and      | Sabbir | Ahmed. |
and QG components do not explicitly identify 2023. BanglaCHQ-summ: An abstractive
|                     |         |     |              |     |        |           | summarization |                | dataset  |     | for medical |                | queries in |
| ------------------- | ------- | --- | ------------ | --- | ------ | --------- | ------------- | -------------- | -------- | --- | ----------- | -------------- | ---------- |
| these relationships |         |     | as important |     | facts. | Future    |               |                |          |     |             |                |            |
|                     |         |     |              |     |        |           | Bangla        | conversational |          |     | speech.     | In Proceedings |            |
| work could          | enhance |     | relational   |     | error  | detection |               |                |          |     |             |                |            |
|                     |         |     |              |     |        |           | of the        | First          | Workshop |     | on          | Bangla         | Language   |
throughexplicitrelationextractionmodulesor
|     |     |     |     |     |     |     | Processing |     | (BLP-2023), |     | pages85–93, |     | Singapore. |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | ----------- | --- | ---------- |
knowledge graph-based approaches. Association for Computational Linguistics.
603

Philippe Laban, Tobias Schnabel, Paul N Bennett, Evaluating text generation with bert. Preprint,
| andMartiAHearst.2022. |        |              |                   | Summac: |             | Re-visiting |       | arXiv:1904.09675. |     |         |         |         |     |
| --------------------- | ------ | ------------ | ----------------- | ------- | ----------- | ----------- | ----- | ----------------- | --- | ------- | ------- | ------- | --- |
| nli-based             | models |              | for inconsistency |         |             | detection   | in    |                   |     |         |         |         |     |
| summarization.        |        | Transactions |                   |         | of the      | Association |       |                   |     |         |         |         |     |
| for Computational     |        |              | Linguistics,      |         | 10:163–177. |             |       |                   |     |         |         |         |     |
|                       |        |              |                   |         |             |             |       | A Implementation  |     |         | Details |         |     |
| Sewon                 | Min,   | Kalpesh      | Krishna,          |         | Xinxi       | Lyu,        | Mike  |                   |     |         |         |         |     |
| Lewis,                | Wen    | tau          | Yih,              | Pang    | Wei         | Koh,        | Mohit |                   |     |         |         |         |     |
|                       |        |              |                   |         |             |             |       | A.1 System        |     | Prompts | for     | Unified |     |
| Iyyer,                | Luke   | Zettlemoyer, |                   | and     | Hannaneh    |             | Ha-   |                   |     |         |         |         |     |
jishirzi. 2023. Factscore: Fine-grained atomic Model Components
| evaluation  |     | of factual | precision         |     | in long | form | text |            |     |       |         |      |        |
| ----------- | --- | ---------- | ----------------- | --- | ------- | ---- | ---- | ---------- | --- | ----- | ------- | ---- | ------ |
| generation. |     | Preprint,  | arXiv:2305.14251. |     |         |      |      |            |     |       |         |      |        |
|             |     |            |                   |     |         |      |      | We present | the | exact | prompts | used | to in- |
Nishat Raihan and Marcos Zampieri. 2025. Tiger- stantiate the QA, QG, and NER compo-
LLM-afamilyofBanglalargelanguagemodels.
|     |     |     |     |     |     |     |     | nents from | the | single | Qwen3-14B-bnb-4bit |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------ | ------------------ | --- | --- |
InProceedingsofthe63rdAnnualMeetingofthe backbone model. All prompts are format-
| Association |          | for Computational |     |       | Linguistics |         | (Vol- |           |     |       |      |          |      |
| ----------- | -------- | ----------------- | --- | ----- | ----------- | ------- | ----- | --------- | --- | ----- | ---- | -------- | ---- |
|             |          |                   |     |       |             |         |       | ted using | the | Qwen3 | chat | template | with |
| ume         | 2: Short | Papers),          |     | pages | 887–896,    | Vienna, |       |           |     |       |      |          |      |
Austria. Association for Computational Linguis- enable_thinking=False to disable internal
| tics.  |          |             |     |     |       |         |      | reasoning | tokens. |     |     |     |     |
| ------ | -------- | ----------- | --- | --- | ----- | ------- | ---- | --------- | ------- | --- | --- | --- | --- |
| Thomas | Scialom, | Paul-Alexis |     |     | Dray, | Patrick | Gal- |           |         |     |     |     |     |
linari, Sylvain Lamprier, Benjamin Piwowarski, A.1.1 Question Answering (QA)
| Jacopo | Staiano, |     | and Alex | Wang. | 2021. | Queste- |     |     |     |     |     |     |     |
| ------ | -------- | --- | -------- | ----- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
Prompt
| val:  | Summarization |                   | asks | for | fact-based |     | evalua- |        |           |     |             |     |          |
| ----- | ------------- | ----------------- | ---- | --- | ---------- | --- | ------- | ------ | --------- | --- | ----------- | --- | -------- |
| tion. | Preprint,     | arXiv:2103.12693. |      |     |            |     |         |        |           |     |             |     |          |
|       |               |                   |      |     |            |     |         | The QA | component |     | is prompted | to  | generate |
Derek Tam, Anisha Mascarenhas, Shiyue Zhang, a short, factual answer (1–2 words) given a
| Sarah | Kwan,      | Mohit | Bansal, |         | and         | Colin | Raffel. |         |              |     |            |     |     |
| ----- | ---------- | ----- | ------- | ------- | ----------- | ----- | ------- | ------- | ------------ | --- | ---------- | --- | --- |
|       |            |       |         |         |             |       |         | context | and question |     | in Bangla. |     |     |
| 2023. | Evaluating |       | the     | factual | consistency |       | of      |         |              |     |            |     |     |
largelanguagemodelsthroughnewssummariza-
tion. In Findings of the Association for Com- QA System Prompt
| putational |          | Linguistics: |     | ACL         | 2023, | pages      | 5220– |     |     |     |     |     |     |
| ---------- | -------- | ------------ | --- | ----------- | ----- | ---------- | ----- | --- | --- | --- | --- | --- | --- |
| 5255,      | Toronto, | Canada.      |     | Association |       | for Compu- |       |     |     |     |     |     |     |
System:
| tational   | Linguistics.      |           |             |           |        |            |        |           |              |       |         |                     |      |
| ---------- | ----------------- | --------- | ----------- | --------- | ------ | ---------- | ------ | --------- | ------------ | ----- | ------- | ------------------- | ---- |
|            |                   |           |             |           |        |            |        | পৰ্সঙ্গ   | এবং পৰ্েশ্নর | উপর   | িভিত্ত  | কের উত্তর           | িদন। |
| Alex Wang, |                   | Kyunghyun |             | Cho,      | and    | Mike       | Lewis. |           |              |       |         |                     |      |
|            |                   |           |             |           |        |            |        | শুধুমাতৰ্ | সংিক্ষপ্ত    | উত্তর | িদন (এক | বা দুই শ(cid:320))। |      |
| 2020.      | Asking            |           | and         | answering |        | questions  | to     |           |              |       |         |                     |      |
| evaluate   | the               | factual   | consistency |           | of     | summaries. |        | User:     |              |       |         |                     |      |
| Preprint,  | arXiv:2004.04228. |           |             |           |        |            |        |           |              |       |         |                     |      |
|            |                   |           |             |           |        |            |        | পৰ্সঙ্গ:  | {context}    |       |         |                     |      |
| An Yang,   | Anfeng            |           | Li,         | Baosong   | Yang,  | Beichen    |        | পৰ্শ্ন:   | {question}   |       |         |                     |      |
| Zhang,     | Binyuan           |           | Hui,        | Bo        | Zheng, | Bowen      | Yu,    |           |              |       |         |                     |      |
| Chang      | Gao,              | Chengen   |             | Huang,    | Chenxu | Lv,        | Chu-   |           |              |       |         |                     |      |
jie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, English Translation:
| Feng                       | Hu, Hao   | Ge, | Haoran            | Wei, | Huan           | Lin, | Jia- |           |        |     |              |     |          |
| -------------------------- | --------- | --- | ----------------- | ---- | -------------- | ---- | ---- | --------- | ------ | --- | ------------ | --- | -------- |
| longTang,and41others.2025. |           |     |                   |      | Qwen3technical |      |      |           |        |     |              |     |          |
| report.                    | Preprint, |     | arXiv:2505.09388. |      |                |      |      |           |        |     |              |     |          |
|                            |           |     |                   |      |                |      |      | • System: | Answer |     | the question |     | based on |
Yuxuan Ye, Edwin Simpson, and Raul Santos the context and question. Provide only
| Rodriguez.  |     | 2024.       | Using | similarity    |     | to        | evalu- |         |        |      |        |         |     |
| ----------- | --- | ----------- | ----- | ------------- | --- | --------- | ------ | ------- | ------ | ---- | ------ | ------- | --- |
|             |     |             |       |               |     |           |        | a short | answer | (one | or two | words). |     |
| ate factual |     | consistency |       | in summaries. |     | Preprint, |        |         |        |      |        |         |     |
arXiv:2409.15090.
Kai Zhang, Xiangyu Meng, Xiaoxuan Yan, Ji- • User: Context: {context}
aqi Ji, Jingwen Liu, Hao Xu, Haochen Zhang, Question: {question}
| Dongyang  |      | Liu, Jiahui |       | Wang,     | Xiaohan | Wang,  | Ji-  |     |     |     |     |     |     |
| --------- | ---- | ----------- | ----- | --------- | ------- | ------ | ---- | --- | --- | --- | --- | --- | --- |
| aming     | Gao, | Yue         | Wang, | Chengming |         | Shao,  | Wen- |     |     |     |     |     |     |
| jun Wang, |      | Jingcheng   |       | Li, Ming  | Zheng,  | Yichen |      |     |     |     |     |     |     |
Yang, and Yixuan Tang. 2025. Revolutionizing A.1.2 Question Generation (QG)
| health | care: | The | transformative |     | impact | of  | large |     |     |     |     |     |     |
| ------ | ----- | --- | -------------- | --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
Prompt
| language | models |     | in medicine. |     | Journal | of  | Medi- |     |     |     |     |     |     |
| -------- | ------ | --- | ------------ | --- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- |
cal Internet Research, 27:e59069. The QG component generates a short, contex-
tuallygroundedquestionconditionedonapro-
TianyiZhang,VarshaKishore,FelixWu,KilianQ.
| Weinberger, |     | and | Yoav | Artzi. | 2020. | Bertscore: |     | vided answer | span. |     |     |     |     |
| ----------- | --- | --- | ---- | ------ | ----- | ---------- | --- | ------------ | ----- | --- | --- | --- | --- |
604

QG System Prompt A.1.4 Question Weighting
(Importance Scorer) Prompt
System:
The question weighter component scores each
পৰ্সঙ্গ এবং উত্তেরর উপর িভিত্ত কের একিট সং-
question’s importance for a given source docu-
িক্ষপ্ত পৰ্শ্ন ৈতির করুন।
ment on a scale from 0.0 to 1.0.
পৰ্শ্নিটএমনহেতহেবেযপৰ্সেঙ্গিজজ্ঞাসাকরাহেল,
উত্তর আপনার পৰ্দত্ত উত্তর হয়। Question Weighter Prompt
User:
System:
পৰ্সঙ্গ: {context} তুিম একজন পৰ্শ্ন মূলয্ায়নকারী। পৰ্দত্ত পৰ্সঙ্গ এবং
উত্তর: {answer}
পৰ্শ্ন িবেবচনা কের, পৰ্শ্নিট কতটা গুরুতব্পূণর্ তা মূ-
লয্ায়ন কেরা।
English Translation:
গুরুতব্পূণর্ পৰ্শ্ন (উচ্চ েস্কার):
• System: Generate a short question based ￿ মূল তথয্ সম্পেকর্ িজজ্ঞাসা কের (েক, কী,
on the context and answer. The question কখন, েকাথায়)
must be such that when asked in the con-
text, the response is the provided answer. ￿ পৰ্সেঙ্গর েকন্দৰ্ীয় িবষয়বস্তু সম্পেকর্
￿ পৰ্ধান বয্িক্ত, স্থান, ঘটনা সম্পেকর্
• User: Context: {context}
Answer: {answer}
গুরুতব্হীন পৰ্শ্ন (িনম্ন েস্কার):
A.1.3 Named Entity and Noun ￿ তুচ্ছ িববরণ সম্পেকর্
Extraction (NER) Prompt
￿ পৰ্সেঙ্গ উেল্লখ েনই এমন িবষয় সম্পেকর্
The NER component extracts named entities
and nouns from Bangla text and returns them
￿ অপৰ্াসিঙ্গক তথয্
as a comma-separated list.
শুধুমাতৰ্ একিট সংখয্া (0.0 েথেক 1.0) িদেয় উত্তর
NER System Prompt দাও। েকান বয্াখয্া না।
System: User:
আপিন একিট মেডল যা বাংলা ভাষায় পৰ্দত্ত পাঠয্ পৰ্সঙ্গ: {context}
েথেকনামযুক্তসত্তাএবংিবেশষয্িনষ্কাশনকেরএবং পৰ্শ্ন: {question}
েসগুিল একিট অসংখয্ািয়ত তািলকা িহসােব পৰ্দান গুরুতব্ েস্কার (0.0-1.0):
কের, কমা দব্ারা পৃথক (েমাট নামযুক্ত সত্তা এবং
িবেশেষয্র সংখয্া উেল্লখ করার পৰ্েয়াজন েনই)। English Translation:
েকান অিতিরক্ত বয্াখয্া ছাড়াই বাংলা ভাষায় আউট-
• System: You are a question evaluator.
পুট েফরত িদন।
Considering the given context and ques-
User: tion,evaluatehowimportantthequestion
পৰ্সঙ্গ: {context} is.
Important Questions (High Score):
English Translation:
– Asks about key information (who,
• System: You are a model that extracts what, when, where)
named entities and nouns from texts pro-
– About the central theme of the con-
vided in Bangla and provides them as an
text
unnumbered list, separated by commas
– About main persons, places, events
(no need to mention the total number of
named entities and nouns). Return the Unimportant Questions (Low Score):
output in Bangla language without any
– About trivial details
additional explanations.
– About topics not mentioned in con-
• User: Context: {context} text
605

| –      | Irrelevant | information |          |      |     |       |
| ------ | ---------- | ----------- | -------- | ---- | --- | ----- |
| Answer | with       | only        | a number | (0.0 | to  | 1.0). |
No explanation.
| • User:    | Context: |            | {context}  |     |     |     |
| ---------- | -------- | ---------- | ---------- | --- | --- | --- |
| Question:  |          | {question} |            |     |     |     |
| Importance |          | Score      | (0.0-1.0): |     |     |     |
A.2 Hyperparameters
Table6: Generationhyperparametersforallmodel
components.
| Parameter         |              |                          | QA/QG/NER          |           | Weighter  |      |
| ----------------- | ------------ | ------------------------ | ------------------ | --------- | --------- | ---- |
| Model             |              |                          | Qwen3-14B-bnb-4bit |           |           |      |
| Temperature       |              |                          | 0.0                |           |           | 0.0  |
| Sampling          |              |                          | Greedy             |           | Greedy    |      |
| MaxNewTokens      |              | 256(QA),150(QG),512(NER) |                    |           |           | 10   |
| RepetitionPenalty |              |                          | 1.1                |           |           | 1.0  |
| MaxSequenceLength |              |                          | 2048               |           |           | 2048 |
| A.3 Filtering     |              | Threshold                |                    |           |           |      |
| We set            | the semantic |                          | similarity         | threshold |           | τ =  |
| 0.60 for          | filtering    | question-answer          |                    |           | pairs     | dur- |
| ing the           | construction |                          | of (C).            | This      | threshold |      |
P
waschosenempiricallytobalanceprecision(re-
movingill-formedQApairs)andrecall(retain-
| ing valid     | pairs          | with             | paraphrased   | answers). |            |      |
| ------------- | -------------- | ---------------- | ------------- | --------- | ---------- | ---- |
| A.4 BERTScore |                |                  | Configuration |           |            |      |
| We use        | the bert-score |                  | Python        | library   |            | with |
| the following | configuration: |                  |               |           |            |      |
| • Model:      |                | xlm-roberta-base |               |           | (multilin- |      |
gual)
| • Language |     | code:  | bn (Bengali) |      |           |     |
| ---------- | --- | ------ | ------------ | ---- | --------- | --- |
| • Metric:  |     | Recall | component    | only | (R)       |     |
| • Device:  |     | CUDA   | (GPU)        | when | available |     |
606

| B English |     | Translated | Result |     | Table |     |     |     |     |
| --------- | --- | ---------- | ------ | --- | ----- | --- | --- | --- | --- |
Human
| Source | (English) |     |     | Summary |     | (English) |     |     | BanglaSummEval |
| ------ | --------- | --- | --- | ------- | --- | --------- | --- | --- | -------------- |
Score
I did not find joy in seeing a Outer beauty is not important; 0.73 0.76
| beautiful       | face.          | In character, | the         | inner       | character  | is         | the true     |           |     |
| --------------- | -------------- | ------------- | ----------- | ----------- | ---------- | ---------- | ------------ | --------- | --- |
| person is       | not beautiful; |               | even if     | measure.    |            | People     | with bad     |           |     |
| visually        | attractive,    | people        | hate        | character   |            | can still  | be outwardly |           |     |
| their behavior, |                | touch,        | and         | attractive. |            | Even       | those with   | bad       |     |
| manners.        | Ill-tempered   |               | people hurt | character   |            | appreciate | those        | with      |     |
| others’ hearts. |                | One does      | not feel    | good        | character. |            | Hence,       | one must  |     |
| satisfaction    | from           | their         | handsome    | strive      | and        | work       | hard to      | cultivate |     |
| face. Naive     | people         | get           | dazzled by  | good        | character. |            |              |           |     |
| appearances     | and            | suffer        |             |             |            |            |              |           |     |
| consequences.   |                | Those with    | bad         |             |            |            |              |           |     |
| character       | also           | despise       | misdeeds    |             |            |            |              |           |     |
| and lies.       | Even           | if a person   | is not      |             |            |            |              |           |     |
| naturally       | good-looking,  |               | they love   |             |            |            |              |           |     |
| virtuous        | character.     | Building      | good        |             |            |            |              |           |     |
| character       | requires       | hard          | work and    |             |            |            |              |           |     |
practice.
Since 10.09.19 I have had dengue From 10.09.19 I have had dengue 0.77 0.77
| fever, today   | makes       | 10      | days. NS1        | fever.    | Today       | is day      | 10.         | NS1 is              |     |
| -------------- | ----------- | ------- | ---------------- | --------- | ----------- | ----------- | ----------- | ------------------- | --- |
| is positive.   | Platelets   | were    |                  | positive. |             | Previously, | platelets   |                     |     |
| decreasing,    | but         | for the | last 3 days      | were      | decreasing; |             | in the last | 3 days              |     |
| they are       | increasing. | Today’s |                  | they      | have        | increased.  | Latest      | report              |     |
| report shows   | 150,000.    |         | My body is       | shows     | 150,000.    | My          | body        | feels               |     |
| somewhat       | weak.       | There   | is no other      | somewhat  |             | weak.       |             |                     |     |
| major problem. |             | When    | will I know      |           |             |             |             |                     |     |
| my dengue      | is cured?   |         |                  |           |             |             |             |                     |     |
|                |             |         | Table 7: English |           | translation |             | of example  | evaluation samples. |     |
607

| C   | Human   | Evaluation  |     |     | Guidelines |     | for |           |                |         |               |     |            |
| --- | ------- | ----------- | --- | --- | ---------- | --- | --- | --------- | -------------- | ------- | ------------- | --- | ---------- |
|     |         |             |     |     |            |     |     | Error     | Categories     |         | and Penalties |     |            |
|     | Factual | Consistency |     |     |            |     |     |           |                |         |               |     |            |
|     |         |             |     |     |            |     |     | Intrinsic | Hallucination: |         | Direct        |     | contradic- |
|     |         |             |     |     |            |     |     | tion      | (e.g.,         | “black” | vs. “white”)  |     | — Heavy    |
Objective
penalty
| Annotators |     | evaluate | whether |     | generated |     | sum- |     |     |     |     |     |     |
| ---------- | --- | -------- | ------- | --- | --------- | --- | ---- | --- | --- | --- | --- | --- | --- |
mariesarefactuallyconsistentwithsourcedoc- Extrinsic Hallucination: Unsupported ad-
uments by identifying hallucinations, contra- ditions(e.g.,addingreasonsnotinsource)
|          |     |                 |     |        |     |      |         | —   | Moderate-heavy |     | penalty |     |     |
| -------- | --- | --------------- | --- | ------ | --- | ---- | ------- | --- | -------------- | --- | ------- | --- | --- |
| dictions |     | and unsupported |     | claims |     | on a | 0.0–1.0 |     |                |     |         |     |     |
scale.
|      |          |     |     |     |     |     |     | Entity | Error: | Incorrect | names,  | numbers, | or  |
| ---- | -------- | --- | --- | --- | --- | --- | --- | ------ | ------ | --------- | ------- | -------- | --- |
| Core | Question |     |     |     |     |     |     | dates  | —      | Moderate  | penalty |          |     |
“Does the source document explicitly state or Relation Error: Wrong relationships be-
strongly imply this information?” tween entities — Heavy penalty
| Scoring |     | Rubric |     |     |     |     |     | Special          | Cases |     |                 |     |         |
| ------- | --- | ------ | --- | --- | --- | --- | --- | ---------------- | ----- | --- | --------------- | --- | ------- |
|         |     |        |     |     |     |     |     | • Simplification |       |     | vs. Distortion: |     | Correct |
Score Level Description simplification of complex ideas scores 1.0;
0.8 - 1.0 Perfect All information fully sup- oversimplification that changes meaning
|     |     |     | ported;         |            | no hallucinations, |             |     |        |      |     |     |     |     |
| --- | --- | --- | --------------- | ---------- | ------------------ | ----------- | --- | ------ | ---- | --- | --- | --- | --- |
|     |     |     |                 |            |                    |             |     | scores | 0.9. |     |     |     |     |
|     |     |     | contradictions, |            |                    | or mislead- |     |        |      |     |     |     |     |
|     |     |     | ing             | inferences |                    |             |     |        |      |     |     |     |     |
0.5 - 0.8 Good Mainfactscorrect;minorin- • Omissions: Missing information affects
accuracies or subtle unsup- recall, not consistency; only penalize if
porteddetailsthatdonotal-
|     |       |       |                    |         |              |         |     | omission    |     | makes | remaining | information |     |
| --- | ----- | ----- | ------------------ | ------- | ------------ | ------- | --- | ----------- | --- | ----- | --------- | ----------- | --- |
|     |       |       | ter                | meaning |              |         |     |             |     |       |           |             |     |
| 0.2 | - 0.5 | Mixed | Equal              | mix     | of supported |         | and | misleading. |     |       |           |             |     |
|     |       |       | unsupportedclaims; |         |              | approx- |     |             |     |       |           |             |     |
|     |       |       | imately            | half    | hallucinated |         | or  |             |     |       |           |             |     |
contradictory
|            | 0 - 0.2  | Poor      | Mostly      | unsupported        |              | or          | con-    |     |     |     |     |     |     |
| ---------- | -------- | --------- | ----------- | ------------------ | ------------ | ----------- | ------- | --- | --- | --- | --- | --- | --- |
|            |          |           | tradictory; |                    | invented     | details,    |         |     |     |     |     |     |     |
|            |          |           | quotes,     | or                 | events       |             |         |     |     |     |     |     |     |
| Evaluation |          | Procedure |             |                    |              |             |         |     |     |     |     |     |     |
| 1.         | Read     | the       | source      | document           |              | carefully   |         |     |     |     |     |     |     |
|            | to       | identify  | core        | facts,             | entities     |             | (names, |     |     |     |     |     |     |
|            | dates,   | places),  | and         | narrative.         |              |             |         |     |     |     |     |     |     |
| 2.         | Analyze  | the       | summary     |                    | sentence-by- |             |         |     |     |     |     |     |     |
|            | sentence | rather    |             | than holistically. |              |             |         |     |     |     |     |     |     |
| 3.         | Verify   | each      | claim       | against            |              | the source: |         |     |     |     |     |     |     |
|            | •        | Found     | in source   |                    | Correct      |             |         |     |     |     |     |     |     |
→
|     | •   | Not found | in  | source | Hallucination |     |     |     |     |     |     |     |     |
| --- | --- | --------- | --- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
→
penalty
|     | •   | Differs | from | source | Contradiction |     |     |     |     |     |     |     |     |
| --- | --- | ------- | ---- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
→
penalty
| 4.  | Detect   | entity | errors |               | (incorrect |         | names, |     |     |     |     |     |     |
| --- | -------- | ------ | ------ | ------------- | ---------- | ------- | ------ | --- | --- | --- | --- | --- | --- |
|     | numbers, | dates, | or     | relationships |            | between |        |     |     |     |     |     |     |
entities).
| 5.  | Assign | score          | based | on      | proportion |     | of ac- |     |     |     |     |     |     |
| --- | ------ | -------------- | ----- | ------- | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- |
|     | curate | vs. inaccurate |       | claims. |            |     |        |     |     |     |     |     |     |
608