|     | SummEval: |     |     | Re-evaluating | Summarization          |     | Evaluation |     |     |     |     |
| --- | --------- | --- | --- | ------------- | ---------------------- | --- | ---------- | --- | --- | --- | --- |
|     |           |     |     | R.Fabbri†∗    | WojciechKrys´cin´ski‡∗ |     |            |     |     |     |     |
Alexander
| BryanMcCann‡ |     |     |     | Xiong‡ | RichardSocher‡ |     | DragomirRadev†‡ |     |     |     |     |
| ------------ | --- | --- | --- | ------ | -------------- | --- | --------------- | --- | --- | --- | --- |
Caiming
|     |     |     |     | †              | ‡                  |     |     |     |     |     |     |
| --- | --- | --- | --- | -------------- | ------------------ | --- | --- | --- | --- | --- | --- |
|     |     |     |     | YaleUniversity | SalesforceResearch |     |     |     |     |     |     |
{alexander.fabbri,dragomir.radev}@yale.edu,
{kryscinski,cxiong}@salesforce.com
richard@socher.org
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
bryan.mccann.is@gmail.com
|     |     | Abstract |     |     | Thefieldhasbenefitedfromadvancesinneural |               |     |            |     |         |       |
| --- | --- | -------- | --- | --- | ---------------------------------------- | ------------- | --- | ---------- | --- | ------- | ----- |
|     |     |          |     |     | network                                  | architectures |     | (Sutskever |     | et al., | 2014; |
The scarcity of comprehensive up-to-date Bahdanau et al., 2014; Vinyals et al., 2015;
studiesonevaluationmetricsfortextsummari-
|        |         |         |           |           | Vaswani | et al., | 2017) | as well | as  | the availability |     |
| ------ | ------- | ------- | --------- | --------- | ------- | ------- | ----- | ------- | --- | ---------------- | --- |
| zation | and the | lack of | consensus | regarding |         |         |       |         |     |                  |     |
oflarge-scaledatasets(Sandhaus,2008;Hermann
evaluation protocols continue to inhibit pro- et al., 2015; Grusky et al., 2018; Narayan et al.,
gress.Weaddresstheexistingshortcomingsof
|     |     |     |     |     | 2018). Recent |     | advances | in  | pretrained | language |     |
| --- | --- | --- | --- | --- | ------------- | --- | -------- | --- | ---------- | -------- | --- |
summarizationevaluationmethodsalongfive
models,suchasBERT(Devlinetal.,2019),have
dimensions: 1) we re-evaluate 14 automatic motivated a corresponding shift to pretraining
evaluation metrics in a comprehensive and methodsinsummarization(LiuandLapata,2019;
consistentfashionusingneuralsummarization
|       |         |            |        |            | Zhang et | al., 2019b; |     | Dong | et al., | 2019; | Ziegler |
| ----- | ------- | ---------- | ------ | ---------- | -------- | ----------- | --- | ---- | ------- | ----- | ------- |
| model | outputs | along with | expert | and crowd- |          |             |     |      |         |       |         |
etal.,2019;Raffeletal.,2019;Lewisetal.,2019).
sourcedhumanannotations;2)weconsistently A standard dataset for training summarization
| benchmark | 23  | recent summarization |     | models |        |                      |     |     |        |          |     |
| --------- | --- | -------------------- | --- | ------ | ------ | -------------------- | --- | --- | ------ | -------- | --- |
|           |     |                      |     |        | models | is the CNN/DailyMail |     |     | corpus | (Hermann |     |
usingtheaforementionedautomaticevaluation
etal.,2015),originallyaquestionansweringtask,
metrics;3)weassemblethelargestcollection
|     |     |     |     |     | which was | repurposed |     | for | summarization |     | by  |
| --- | --- | --- | --- | --- | --------- | ---------- | --- | --- | ------------- | --- | --- |
ofsummariesgeneratedbymodelstrainedon
|     |     |     |     |     | Nallapati | et al. | (2016). | The | dataset | consists | of  |
| --- | --- | --- | --- | --- | --------- | ------ | ------- | --- | ------- | -------- | --- |
theCNN/DailyMailnewsdatasetandshareit
newsarticlesandassociatedhuman-createdbullet-
inaunifiedformat;4)weimplementandshare
|     |     |     |     |     | point summaries. |     | The | ROUGE |     | (Lin, | 2004b) |
| --- | --- | --- | --- | --- | ---------------- | --- | --- | ----- | --- | ----- | ------ |
atoolkitthatprovidesanextensibleandunified metric, which measures lexical overlap between
| API for | evaluating  | summarization |              | models      |                  |            |                           |            |     |      |           |
| ------- | ----------- | ------------- | ------------ | ----------- | ---------------- | ---------- | ------------------------- | ---------- | --- | ---- | --------- |
|         |             |               |              |             | generated        | and target |                           | summaries, | is  | then | typically |
| across  | a broad     | range         | of automatic | metrics;    |                  |            |                           |            |     |      |           |
|         |             |               |              |             | usedtogetherwith |            | crowd-sourcedhumanannota- |            |     |      |           |
| and 5)  | we assemble |               | and share    | the largest |                  |            |                           |            |     |      |           |
tionsformodelevaluation.Whilethecurrentsetup
| and most   | diverse, | in terms | of        | model types, |                          |     |     |     |         |             |     |
| ---------- | -------- | -------- | --------- | ------------ | ------------------------ | --- | --- | --- | ------- | ----------- | --- |
|            |          |          |           |              | hasbecomestandardized,we |     |     |     | believe | severalfac- |     |
| collection | of       | human    | judgments | of model-    |                          |     |     |     |         |             |     |
torspreventamorecompletecomparisonofmod-
| generatedsummariesonthe |           |         | CNN/Daily | Mail       |           |            |           |     |     |            |     |
| ----------------------- | --------- | ------- | --------- | ---------- | --------- | ---------- | --------- | --- | --- | ---------- | --- |
|                         |           |         |           |            | els, thus | negatively | impacting |     | the | progressof | the |
| dataset                 | annotated | by both | expert    | judges and | field.    |            |           |     |     |            |     |
crowd-sourceworkers.Wehopethatthiswork
|           |         |        |          |         | As noted | by  | Hardy | et al. | (2019), | recent | papers |
| --------- | ------- | ------ | -------- | ------- | -------- | --- | ----- | ------ | ------- | ------ | ------ |
| will help | promote | a more | complete | evalua- |          |     |       |        |         |        |        |
vastlydifferintheirevaluationprotocol.Existing
| tion protocol |          | for text summarization |            | as well    |                 |         |              |        |             |             |         |
| ------------- | -------- | ---------------------- | ---------- | ---------- | --------------- | ------- | ------------ | ------ | ----------- | ----------- | ------- |
|               |          |                        |            |            | work often      | limits  | model        |        | comparisons |             | to only |
| as advance    | research | in                     | developing | evaluation |                 |         |              |        |             |             |         |
|               |          |                        |            |            | a few baselines |         | and          | offers | human       | evaluations |         |
| metrics       | that     | better correlate       |            | with human |                 |         |              |        |             |             |         |
|               |          |                        |            |            | which are       | largely | inconsistent |        | with        | prior       | work.   |
judgments.
|     |     |     |     |     | Additionally, | despite |     | problems | associated |     | with |
| --- | --- | --- | --- | --- | ------------- | ------- | --- | -------- | ---------- | --- | ---- |
1 Introduction ROUGE when used outside of its original setting
|     |     |     |     |     | (Liu and | Liu, 2008; |     | Cohan | and Goharian, |     | 2016) |
| --- | --- | --- | --- | --- | -------- | ---------- | --- | ----- | ------------- | --- | ----- |
Text summarization aims to compress long doc- as well as the introduction of many variations
ument(s)intoashort,fluent,andhuman-readable
|     |     |     |     |     | on ROUGE | (Zhou | et  | al., 2006; | Ng  | and | Abrecht, |
| --- | --- | --- | --- | --- | -------- | ----- | --- | ---------- | --- | --- | -------- |
form that preserves the most salient information 2015;Ganesan,2015;ShafieiBavanietal., 2018)
fromthesourcedocument. and other text generation metrics (Peyrard,2019;
∗Equalcontributionsfromauthors Zhao et al., 2019; Zhang et al., 2020; Scialom
391
TransactionsoftheAssociationforComputationalLinguistics,vol.9,pp.391–409,2021.https://doi.org/10.1162/tacla00373
ActionEditor:Andre´F.T.Martins.Submissionbatch:8/2020;Revisionbatch:11/2020;Published4/2021.
|     |     | (cid:3)c 2021AssociationforComputationalLinguistics.DistributedunderaCC-BY4.0license. |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

et al., 2019; Clark et al., 2019), ROUGE has evaluating against multiple references results in
remainedthedefaultautomaticevaluationmetric. higher correlation scores with human judgments
We believe that the shortcomings of the current —however,asingle-referencesettingissufficient
evaluation protocol are partially caused by the for the metric to be effective. Owczarzak et al.
lack of easy-to-useresourcesforevaluation, both (2012) studied the effects of inconsistencies in
in the form of simplified evaluation toolkits and human annotations on the rankings of evalu-
largecollectionsofmodeloutputs. atedsummarizationsystems.Resultsshowedthat
Inparallel,thereisanissuewithhowevaluation system-levelrankingswererobustagainstannota-
metrics are evaluated themselves. Many of the tion inconsistencies, but summary-level rankings
currently used metrics were developed and as- werenotstableinsuchsettingsandlargelybenefit
sessed using the Document Understanding Con- from improving annotator consistency. Rankel
ference (DUC) and Text Analysis Conference et al. (2013) analyzed the performance of differ-
(TAC)shared-tasksdatasets(DangandOwczarzak ent variants of the ROUGE metric using TAC
2008,2009).However,ithasrecentlybeenshown datasets.The authorsfoundthat higher-orderand
that the mentioned datasets contain human judg- lesscommonlyreportedROUGEsettingsshowed
ments for model outputs scoring on a lower a higher correlation with human judgments. In a
scalecomparedtocurrentsummarizationsystems similar line of work, Graham (2015) conducted
puttingintoquestionthetrueperformanceofthose a large-scale study of the effectiveness of dif-
metricsinthenewsetting(Peyrard,2019). ferent ROUGE metric variants and compared it
Weaddressthesegapsincomplementaryways: againsttheBLEUmetricontheDUCdatasets.Its
1)Were-evaluate14automaticevaluationmetrics resultshighlighted severalsuperior,non-standard
in a comprehensive and consistent fashion using ROUGE settings that achieved strong correla-
outputs from recent neural summarization mod- tions with human judgments on model-generated
els along with expert and crowd-sourced human summaries.InChagantyetal.(2018),theauthors
annotations; 2) We consistently benchmark 23 investigated using an automatic metric to reduce
recent summarization models using the afore- thecostofhumanevaluation without introducing
mentioned automatic evaluation metrics; 3) We bias.Togetherwiththestudy,theauthorsreleased
releasealignedsummarizationmodeloutputsfrom a set of human judgments over several model
23 papers (44 model outputs) published between outputs, limited to a small set of model types.
2017 and 2019 trained on the CNN/DailyMail Peyrard (2019) showed that standard metrics are
dataset to allow for large-scale comparisons of inagreementwhendealingwithsummariesinthe
recent summarization models; 4) We release a scoringrangefoundinTACsummaries,butvastly
toolkit of 14 evaluation metrics with an exten- differ in the higher-scoring range found in cur-
sible and unified API to promote the reporting rent models. The authors reported that additional
of additional metrics in papers; 5) We collect human annotations on modern model outputs
and release expert, as well as crowd-sourced, are necessary to conduct a conclusive study of
human judgments for 16 model outputs on 100 evaluationmetrics.Hardyetal.(2019)underscore
articles over 4 dimensions to further research the differencesin approachesto human summary
into human-correlated evaluation metrics. Code evaluation while proposing a highlight-based
and data associated with this work is avail- reference-less evaluation metric. Other work has
able at https://github.com/Yale-LILY examinedtheproblemswith applyingROUGEin
/SummEval. settings such as meeting summarization (Liu and
Liu,2008)andsummarizationofscientificarticles
(Cohan and Goharian, 2016). We build upon this
2 Related Work
lineofresearchbyexamining theperformanceof
Previous work examining the research setup of several automatic evaluation methods, including
text summarization can be broadly categorized ROUGEanditsvariants,againsttheperformance
intothreegroups,basedonthesubjectofanalysis: ofexperthumanannotators.
evaluationmetrics,datasets,andmodels. Inrelationtodatasets,Dernoncourtetal.(2018)
Dealing with evaluation methods, Lin (2004a) presented a detailed taxonomy of existing sum-
examinedtheeffectivenessoftheROUGEmetric marization datasets. The authors highlighted the
invariousDUCtasks.Theauthorsconcludedthat differences in formats of available corpora and
392
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026

called for creating a unified data standard. In consistent, side-by-side re-evaluation of summa-
a similar line of research, Grusky et al. (2018) rization model outputs and evaluation methods.
offered a thorough analysis of existing corpora, We also share resources that we hope will prove
focusing their efforts on news summarization usefulforfutureworkinanalyzingandimproving
datasets.Theauthorsalsointroducedseveralmet- summarizationmodelsandmetrics.
ricsforevaluatingtheextractivenessofsummaries Shortly before publishing this paper, a library
that are included in the toolkit implemented as for developing summarization metrics was re-
partofthiswork.Krys´cin´skietal.(2020)showed leased by Deutsch and Roth (2020). Our toolkit
that news-related summarization datasets, such iscomplementarytotheirworkastheirtoolkitin-
as CNN/DailyMail, contain strong layout biases. cludesonly3ofour12evaluationmetrics.
The authors revealed that datasets in the current
format,whereeachnewsarticleisassociatedwith 3 EvaluationMetrics and
a single reference summary, leave the task of Summarization Models
summarization underconstrained. The paper also
highlightedtheproblemofnoisy,low-qualitydata We briefly introduce metrics included in our
inautomaticallycollectednewsdatasets. evaluation toolkit as well as the summarization
Looking into models, Zhang et al. (2018a) models for which outputs were collected at the
analyzed the level of abstraction of several timeofreleasingthismanuscript.
recent abstractive summarization models. The
authors showed that word-level extractive mod- 3.1 EvaluationMetrics
els achieved a similar level of abstraction to
Our selection of evaluation methods includes
fully abstractive models. In Kedzie et al. (2018),
severalrecentlyintroducedmetricsthathavebeen
the authors examined the influence of various
applied to both text generation and summariza-
model components on the quality of content
tion, standard machine translation metrics, and
selection. The study revealed that in the cur-
othermiscellaneousperformancestatistics.
rent setting the training signal is dominated by
ROUGE (Lin, 2004b), (Recall-Oriented
biases present in summarization datasets pre-
Understudy for Gisting Evaluation), measures
venting models from learning accurate content
thenumberofoverlappingtextualunits(n-grams,
selection. Krys´cin´ski et al. (2020) investigate the
wordsequences)betweenthegeneratedsummary
problem of factual correctness of text summa-
andasetofgoldreferencesummaries.
rization models. The authors concluded that the
ROUGE-WE(NgandAbrecht,2015)extends
issue of hallucinating facts touches up to 30% of
ROUGE by using soft lexical matching based
generated summaries and list common types of
on the cosine similarity of Word2Vec (Mikolov
errorsmadebygenerativemodels.Closelyrelated
etal.,2013)embeddings.
to that work, Maynez et al. (2020) conducted
S3
(Peyrard et al., 2017) is a model-based
a large-scale study of abstractive summariz-
metric that uses previously proposed evaluation
ers from the perspective of faithfulness. The
metrics, such as ROUGE, JS-divergence, and
authors reached similar conclusions, stating that
ROUGE-WE, as input features for predicting the
improving factual faithfulness is a critical issue
evaluation score. The model is trained on human
in summarization. The results also showed that
judgmentdatasetsfromTACconferences.
currently available evaluation methods, such as
ROUGEandBertScore,arenotsufficienttostudy BertScore (Zhang et al., 2020) computes sim-
the problem at hand. Durmus et al. (2020) and ilarity scoresby aligning generatedand reference
Wangetal.(2020)similarlyexaminefaithfulness summariesonatoken-level.Tokenalignmentsare
evaluation, both proposing question answering computed greedily to maximize the cosine simi-
frameworks as a means of evaluating factual larity between contextualized token embeddings
consistency. fromBERT.
Insights and contributions coming from our MoverScore (Zhao et al., 2019) measures the
work are complementary to the conclusions of semantic distance between a summary and refer-
previous efforts described in this section. To the encetextbymakinguseoftheWordMover’sDis-
best of our knowledge, this is the first work in tance(Kusneretal.,2015)operatingovern-gram
neural text summarization to offer a large-scale, embeddingspooledfromBERTrepresentations.
393
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026

Sentence Mover’s Similarity (SMS) (Clark each summary word belongs. Compression ratio
et al., 2019) extends Word Mover’s Distance to is defined as the word ratio between the articles
viewdocumentsasabagofsentenceembeddings andits summaries:In addition to these measures,
aswellasavariationwhichrepresentsdocuments we also include the percentage of n-grams in
asbothabagofsentencesandabagofwords. thesummarynotfoundintheinputdocumentasa
noveltyscoreandthepercentageofn-gramsinthe
| SummaQA |     | (Scialom | et  | al., 2019) | applies | a   |     |     |     |     |     |     |     |
| ------- | --- | -------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
BERT-basedquestion-answeringmodeltoanswer summary which repeat as a score of redundancy.
cloze-stylequestions usinggeneratedsummaries. For a comprehensive explanation of each metric,
Questions are generated by masking named enti- pleaserefertothecorrespondingpaper.
tiesinsourcedocumentsassociatedwithevaluated Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
|     |     |     |     |     |     |     | 3.2 SummarizationModels |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- |
summaries.ThemetricreportsboththeF1overlap
scoreandQA-modelconfidence. Webroadlycategorizethemodelsincludedinthis
|             |           |          |         |             |                 |       | study into | extractive |     | and     | abstractive | approaches. |           |
| ----------- | --------- | -------- | ------- | ----------- | --------------- | ----- | ---------- | ---------- | --- | ------- | ----------- | ----------- | --------- |
| BLANC       | (Vasilyev |          | et al., | 2020)       | is a reference- |       |            |            |     |         |             |             |           |
|             |           |          |         |             |                 |       | For each   | model,     | we  | provide | a model     |             | code (M*) |
| less metric | that      | measures | the     | performance |                 | gains |            |            |     |         |             |             |           |
ofapre-trainedlanguagemodelgivenaccesstoa as well as a descriptive model name, which will
allowforeasymatchingwiththereleaseddata.
| document | summary | while |     | carrying | out language |     |     |     |     |     |     |     |     |
| -------- | ------- | ----- | --- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
understandingtasksonthesourcedocument’stext.
ExtractiveMethods
| SUPERT         | (Gao       | et al.,  | 2020)    | is a               | reference-less |     |              |                |           |       |         |            |            |
| -------------- | ---------- | -------- | -------- | ------------------ | -------------- | --- | ------------ | -------------- | --------- | ----- | ------- | ---------- | ---------- |
|                |            |          |          |                    |                |     | M1 -         | NEUSUM         |           | (Zhou | et al., | 2018)      | jointly    |
| metric,        | originally | designed |          | for multi-document |                |     |              |                |           |       |         |            |            |
|                |            |          |          |                    |                |     | scores and   | selects        | sentences |       | by      | first      | building a |
| summarization, |            | which    | measures |                    | the semantic   |     |              |                |           |       |         |            |            |
|                |            |          |          |                    |                |     | hierarchical | representation |           |       | of      | a document | and        |
similarityofmodeloutputswithpseudo-reference
|     |     |     |     |     |     |     | considering | the | partially |     | outputted | summary | at  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --------- | --- | --------- | ------- | --- |
summariescreatedbyextractingsalientsentences
eachtimestep.
| from the | source | documents, |     | using | soft | token |      |           |     |       |     |            |        |
| -------- | ------ | ---------- | --- | ----- | ---- | ----- | ---- | --------- | --- | ----- | --- | ---------- | ------ |
|          |        |            |     |       |      |       | M2 - | BanditSum |     | (Dong | et  | al., 2018) | treats |
alignmenttechniques.
|      |           |     |         |       |      |         | extractive | summarization |     |     | as a contextual |     | bandit |
| ---- | --------- | --- | ------- | ----- | ---- | ------- | ---------- | ------------- | --- | --- | --------------- | --- | ------ |
| BLEU | (Papineni |     | et al., | 2002) | is a | corpus- |            |               |     |     |                 |     |        |
problemwherethedocumentisthecontextandthe
| level precision-focused |     |     | metric | that | calculates |     |          |              |     |            |     |        |         |
| ----------------------- | --- | --- | ------ | ---- | ---------- | --- | -------- | ------------ | --- | ---------- | --- | ------ | ------- |
|                         |     |     |        |      |            |     | sequence | of sentences |     | to include |     | in the | summary |
n-gramoverlapbetweenacandidateandreference
istheaction.
| utterance | and | includes | a brevity | penalty. |     | It is the |      |        |       |     |        |         |         |
| --------- | --- | -------- | --------- | -------- | --- | --------- | ---- | ------ | ----- | --- | ------ | ------- | ------- |
|           |     |          |           |          |     |           | M3 - | LATENT | Zhang |     | et al. | (2018b) | propose |
primaryevaluationmetricformachinetranslation.
|      |            |       |     |            |            |     | a latent   | variable | extractive |           | model | which      | views |
| ---- | ---------- | ----- | --- | ---------- | ---------- | --- | ---------- | -------- | ---------- | --------- | ----- | ---------- | ----- |
| CHRF | (Popovic´, | 2015) |     | calculates | character- |     |            |          |            |           |       |            |       |
|      |            |       |     |            |            |     | rele-vance | labels   | of         | sentences | in    | a document | as    |
basedn-gramoverlapbetweenmodeloutputsand
binarylatentvariables.
referencedocuments.
|          |     |           |         |          |           |       | M4         | - REFRESH  |           | Narayan       |            | et al. | (2018)     |
| -------- | --- | --------- | ------- | -------- | --------- | ----- | ---------- | ---------- | --------- | ------------- | ---------- | ------ | ---------- |
| METEOR   |     | (Lavie    | and     | Agarwal, |           | 2007) |            |            |           |               |            |        |            |
|          |     |           |         |          |           |       | propose    | using      | REINFORCE |               | (Williams, |        | 1992)      |
| computes | an  | alignment | between |          | candidate | and   |            |            |           |               |            |        |            |
|          |     |           |         |          |           |       | to extract | summaries, |           | approximating |            |        | the search |
reference sentences by mapping unigrams in the spaceduringtrainingbylimiting to combinations
generated summary to 0 or 1 unigrams in the ofindividuallyhigh-scoringsentences.
| reference,   | based    | on  | stemming, | synonyms, |        | and |             |        |       |     |         |                |         |
| ------------ | -------- | --- | --------- | --------- | ------ | --- | ----------- | ------ | ----- | --- | ------- | -------------- | ------- |
|              |          |     |           |           |        |     | M5          | - RNES | Wu    | and | Hu      | (2018)         | propose |
| paraphrastic | matches. |     | Precision | and       | recall | are |             |        |       |     |         |                |         |
|              |          |     |           |           |        |     | a coherence |        | model | to  | capture | cross-sentence |         |
computedandreportedasaharmonicmean. coherence,combining output from the coherence
CIDEr (Vedantam et al., 2015) computes model and ROUGE scores as a reward in a
| {1–4}-gram | co-occurrences |     |     | between | the | candi- |     |     |     |     |     |     |     |
| ---------- | -------------- | --- | --- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
REINFORCEframework.
dateandreferencetexts,down-weightingcommon M6-JECS(XuandDurrett,2019)firstextracts
n-gramsandcalculatingcosinesimilaritybetween
|     |     |     |     |     |     |     | sentences | from | a   | document |     | and then | scores |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---- | --- | -------- | --- | -------- | ------ |
then-gramsofthecandidateandreferencetexts.
|     |     |     |     |     |     |     | possible | constituency-based |     |     | compressed |     | units to |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------ | --- | --- | ---------- | --- | -------- |
Data Statistics:
|     |     | Grusky |     | et al. | (2018) | define | producethefinalcompressedsummary. |     |     |     |     |     |     |
| --- | --- | ------ | --- | ------ | ------ | ------ | --------------------------------- | --- | --- | --- | --- | --- | --- |
three measures of the extractiveness of a dataset. M7 - STRASS (Bouscarrat et al., 2019)
Extractivefragmentcoverageisthepercentageof extracts a summary by selecting the sentences
words in the summary that are from the source with the closest embeddings to the document
article, measuringtheextentto whicha summary embedding,learningatransformationtomaximize
is a derivative of a text. Density is defined as the the similarity between the summary and the
averagelengthoftheextractivefragmenttowhich groundtruthreference.
394

AbstractiveMethods M17 - T5 Raffel et al. (2019) perform a sys-
M8-PointerGeneratorSeeetal.(2017)propose tematic study of transfer learning techniques and
|     |     |     |     |     |     |     | apply their | insights | to  | a set | of tasks | all | framed |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ----- | -------- | --- | ------ |
avariationofencoder-decodermodels,thePointer
|     |     |     |     |     |     |     | as text-input |     | to text-output |     | generation |     | tasks, |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | -------------- | --- | ---------- | --- | ------ |
GeneratorNetwork,wherethedecodercanchoose
includingsummarization.
| to generate | a   | word | from the | vocabulary |     | or copy |     |     |     |     |     |     |     |
| ----------- | --- | ---- | -------- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
a word from the input. A coverage mechanism is M18 - NeuralTD Bo¨hm et al. (2019) learn
|               |     |            |            |     |           |     | a reward | function | from | 2,500 | human | judgments |     |
| ------------- | --- | ---------- | ---------- | --- | --------- | --- | -------- | -------- | ---- | ----- | ----- | --------- | --- |
| also proposed |     | to prevent | repeatedly |     | attending | to  |          |          |      |       |       |           |     |
thatisusedinareinforcementlearningsetting.
thesamepartofthesourcedocument.
|     |               |     |      |     |        |        | M19 | - BertSum-abs |     | Liu | and | Lapata | (2019) |
| --- | ------------- | --- | ---- | --- | ------ | ------ | --- | ------------- | --- | --- | --- | ------ | ------ |
| M9  | - Fast-abs-rl |     | Chen | and | Bansal | (2018) |     |               |     |     |     |        |        |
propose a model which first extracts salient sen- introduce a novel document-level encoderon top Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
|             |      |         |         |            |          |             | of BERT   | (Devlin | et            | al., 2019), | over | which          | they |
| ----------- | ---- | ------- | ------- | ---------- | -------- | ----------- | --------- | ------- | ------------- | ----------- | ---- | -------------- | ---- |
| tences with | a    | Pointer | Network | and        | rewrites | these       |           |         |               |             |      |                |      |
|             |      |         |         |            |          |             | introduce | both    | an extractive |             | and  | an abstractive |      |
| sentences   | with | a       | Pointer | Generator  |          | Network.    |           |         |               |             |      |                |      |
| In addition | to   | maximum |         | likelihood |          | training, a | model.    |         |               |             |      |                |      |
ROUGE-L rewardis usedto update the extractor M20 - GPT-2 Ziegler et al. (2019) build off
ofGPT-2(Radfordetal.,2019)andfine-tunethe
viaREINFORCE(Williams,1992).
|     |             |     |          |     |     |            | model | by using | human | labels | of  | which | of four |
| --- | ----------- | --- | -------- | --- | --- | ---------- | ----- | -------- | ----- | ------ | --- | ----- | ------- |
| M10 | - Bottom-Up |     | Gehrmann |     | et  | al. (2018) |       |          |       |        |     |       |         |
sampledsummariesisthebesttodirectfine-tuning
| introduce | a bottom–up |     | approach |     | whereby | a con- |     |     |     |     |     |     |     |
| --------- | ----------- | --- | -------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
tent selection model restricts the copy attention inareinforcementlearningframework.
|              |     |              |     |         |     |           | M21     | - UniLM    | Dong | et    | al. (2019) | introduce |     |
| ------------ | --- | ------------ | --- | ------- | --- | --------- | ------- | ---------- | ---- | ----- | ---------- | --------- | --- |
| distribution | of  | a pretrained |     | Pointer |     | Generator |         |            |      |       |            |           |     |
|              |     |              |     |         |     |           | a model | pretrained | on   | three | language   | modeling  |     |
Networkduringinference.
tasks:unidirectional,bidirectional,andsequence-
| M11 | - Improve-abs |     | Krys´cin´ski |     | et  | al. (2018) |     |     |     |     |     |     |     |
| --- | ------------- | --- | ------------ | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
extend the model of Paulus et al. (2017) by to-sequence prediction. It is thus applicable to
naturallanguageunderstandingtasksandgenera-
| augmenting | the | decoder | with | an  | external | LSTM |     |     |     |     |     |     |     |
| ---------- | --- | ------- | ---- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- |
tiontaskssuchasabstractivesummarization.
| language | model | and | add | a novelty |     | RL-based |     |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
objectiveduringtraining. M22 - BART Lewis et al. (2019) introduce a
M12 - Unified-ext-abs Hsu et al. (2018) pro- denoisingautoencoderforpretrainingsequenceto
sequencetaskswhichisapplicabletobothnatural
posetousetheprobabilityoutputofanextractive
languageunderstandingandgenerationtasks.
modelassentence-levelattentiontomodifyword-
level attention scores of an abstractive model, M23-PegasusZhangetal.(2019a)introducea
introducing an inconsistency loss to encourage model pretrained with a novel objective function
|     |     |     |     |     |     |     | designed | for summarization |     |     | by which | important |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------------- | --- | --- | -------- | --------- | --- |
consistencybetweenthesetwolevelsofattention.
|     |     |     |     |     |     |     | sentences | are | removed | from | an input | document |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | ---- | -------- | -------- | --- |
M13-ROUGESalPasunuruandBansal(2018)
propose a keyphrase-based salience reward as andthengeneratedfromtheremainingsentences.
| well asanentailment-based |                     |     |         | rewardin       |             | addition to |             |     |     |     |     |     |     |
| ------------------------- | ------------------- | --- | ------- | -------------- | ----------- | ----------- | ----------- | --- | --- | --- | --- | --- | --- |
| usinga                    | ROUGE-basedrewardin |     |         |                | a REINFORCE |             | 4 Resources |     |     |     |     |     |     |
| setting,                  | optimizing          |     | rewards | simultaneously |             | in          |             |     |     |     |     |     |     |
alternatemini-batches. We now describe the resources collected and
M14-Multi-task(Ent+QG)Guoetal.(2018) releasedtogetherwiththismanuscript.
| propose | question |     | generation |     | and | entailment |     |     |     |     |     |     |     |
| ------- | -------- | --- | ---------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
4.1 ModelOutputs
| generation | as  | auxiliary |     | tasks | in a | multi-task |     |     |     |     |     |     |     |
| ---------- | --- | --------- | --- | ----- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
frameworkalongwithacorrespondingmulti-task
|     |     |     |     |     |     |     | The model | output | collection |     | contains | summaries |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------ | ---------- | --- | -------- | --------- | --- |
architecture. associated with 23 recent papers on neural text
M15 - Closed book decoderJiang and Bansal summarization described in Section 3.2. We
(2018) build upon a Pointer Generator Network obtained a total of 44 model outputs, as many
| by adding | copy-less |     | and | attention-less |     | decoder |        |         |            |     |        |      |        |
| --------- | --------- | --- | --- | -------------- | --- | ------- | ------ | ------- | ---------- | --- | ------ | ---- | ------ |
|           |           |     |     |                |     |         | papers | include | variations |     | of the | main | model. |
during training time to force the encoder to be All models were trained on the CNN/DailyMail
moreselectiveinencodingsalientcontent. news corpus and the collected summaries were
M16 - SENECA Sharma et al. (2019) propose generated using the test split of the dataset with-
to use entity-aware content selection module and outconstraintslimitingtheoutputlength.Outputs
an abstractive generation module to generate the weresolicitedfromtheauthorsofpaperstoensure
finalsummary. comparability between results presented in this
395

paper with those in the original works. They are quality question (Dang, 2005) of structure and
sharedpubliclywiththeconsentoftheauthors. coherence whereby ‘‘the summary should be
Model outputs were transformedinto a unified well-structuredandwell-organized.Thesummary
format and are shared with IDs of the origi- should not just be a heap of related information,
nal CNN/DailyMail examples so that generated but should build from sentence to sentence to a
summaries can be matched with corresponding coherentbodyofinformationaboutatopic.’’
| source | articles. | Pairing | model | outputs | with orig- |             |     |       |         |           |     |         |     |
| ------ | --------- | ------- | ----- | ------- | ---------- | ----------- | --- | ----- | ------- | --------- | --- | ------- | --- |
|        |           |         |       |         |            | Consistency |     | - the | factual | alignment |     | between |     |
inal articles was done using a heuristic approach thesummaryandthesummarizedsource.Afactu-
that relied on aligning reference summaries. The allyconsistentsummarycontainsonlystatements
| pairing | process | revealed | that | 38 examples | in the |          |          |     |            |           |     |       |                                                                                                                                     |
| ------- | ------- | -------- | ---- | ----------- | ------ | -------- | -------- | --- | ---------- | --------- | --- | ----- | ----------------------------------------------------------------------------------------------------------------------------------- |
|         |         |          |      |             |        | that are | entailed | by  | the source | document. |     | Anno- | Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026 |
CNN/DailyMailtestsplitcontainedduplicateref- tatorswerealsoaskedtopenalizesummariesthat
erencesummariespreventingthoseexamplestobe containedhallucinatedfacts.
correctlyaligned.However,thisprobleminvolves
|           |             |               |               |     |            | Fluency | -     | the quality | of      | individual | sentences.  |     |     |
| --------- | ----------- | ------------- | ------------- | --- | ---------- | ------- | ----- | ----------- | ------- | ---------- | ----------- | --- | --- |
| only 0.3% | of          | the available | data          | and | should not |         |       |             |         |            |             |     |     |
|           |             |               |               |     |            | Drawing | again | from        | the DUC | quality    | guidelines, |     |     |
| have a    | significant | impact        | on downstream |     | results.   |         |       |             |         |            |             |     |     |
sentencesinthesummary‘‘shouldhavenoformat-
IDs of duplicate examples are provided together ting problems, capitalization errors or obviously
withthedata.
ungrammaticalsentences(e.g.,fragments,missing
components)thatmakethetextdifficulttoread.’’
4.2 EvaluationToolkit
|                |         |           |          |            |           | Relevance |         | - selection |         | of important |        | content |     |
| -------------- | ------- | --------- | -------- | ---------- | --------- | --------- | ------- | ----------- | ------- | ------------ | ------ | ------- | --- |
| The evaluation |         | toolkit   | contains | 14         | automatic |           |         |             |         |              |        |         |     |
|                |         |           |          |            |           | from the  | source. | The         | summary |              | should | include |     |
| evaluation     | metrics | described |          | in Section | 3.1 con-  |           |         |             |         |              |        |         |     |
onlyimportantinformationfromthesourcedocu-
| solidated | into | a Python | package. | The | package |     |     |     |     |     |     |     |     |
| --------- | ---- | -------- | -------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
ment.Annotatorswereinstructedtopenalizesum-
providesahigh-level,easy-to-useinterfaceunify-
|     |     |     |     |     |     | maries | that | contained | redundancies |     | and | excess |     |
| --- | --- | --- | --- | --- | --- | ------ | ---- | --------- | ------------ | --- | --- | ------ | --- |
ingalloftheunderlyingmetrics.Foreachmetric,
information.
| we implement |     | both evaluate |     | example | and |     |     |     |     |     |     |     |     |
| ------------ | --- | ------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
evaluate batch functions that return the The data collection interface provided judges
|                      |            |             |        |                   |         | with the            | source  | article          | and       | associated | summaries    |          |     |
| -------------------- | ---------- | ----------- | ------ | ----------------- | ------- | ------------------- | ------- | ---------------- | --------- | ---------- | ------------ | -------- | --- |
| metric’s             | score      | on example- |        | and corpus-levels |         |                     |         |                  |           |            |              |          |     |
|                      |            |             |        |                   |         | grouped             | in sets | of               | 5. Each   | group      | of summaries |          |     |
| accordingly.Function |            | inputs      | and    | outputs           | arealso |                     |         |                  |           |            |              |          |     |
|                      |            |             |        |                   |         | contained           | the     | referencesummary |           |            | associated   | with     |     |
| unified              | across     | all metrics | to     | streamline        | multi-  |                     |         |                  |           |            |              |          |     |
|                      |            |             |        |                   |         | the source          | article | to               | establish | a          | common       | point    |     |
| metric               | evaluation | and         | result | processing.       | The     |                     |         |                  |           |            |              |          |     |
|                      |            |             |        |                   |         | of referencebetween |         |                  | groups.   | Summary    |              | grouping |     |
toolkitcomeswithastandardconfigurationresem-
|                 |           |                      |                        |     |             | and order       | within | groups   |       | were randomized |      | for       |     |
| --------------- | --------- | -------------------- | ---------------------- | --- | ----------- | --------------- | ------ | -------- | ----- | --------------- | ---- | --------- | --- |
| bling the       | most      | popular              | settings               | for | each of the |                 |        |          |       |                 |      |           |     |
|                 |           |                      |                        |     |             | each annotator. |        | Judges   | were  | asked           | to   | rate the  |     |
| metrics         | to enable | easy, out-of-the-box |                        |     | use. How-   |                 |        |          |       |                 |      |           |     |
|                 |           |                      |                        |     |             | summaries       | on     | a Likert | scale | from            | 1 to | 5 (higher |     |
| ever,eachmetric |           | canbe                | furtherconfiguredusing |     |             |                 |        |          |       |                 |      |           |     |
better)alongthefourmentioneddimensions.
externalginconfigurationfiles.Wealsoprovide
|     |     |     |     |     |     | Crowd-sourced |     | annotators |     | were | hired | through |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ---------- | --- | ---- | ----- | ------- | --- |
acommand-linetooltoevaluateasummarization
modelwithseveralmetricsinparallel. theAmazonMechanicalTurkplatform.Thehiring
criteriaweresettoaminimumof10000approved
| 4.3 HumanAnnotations |     |     |     |     |     | HITsandanapprovalrateof97%orhigher.Geo- |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
The collection of human annotations contains graphicconstraintsforworkersweresettoUnited
summary evaluations of 16 recent neural sum- States, United Kingdom, and Australia to ensure
|            |        |           |      |               |     | that summaries |     | were | evaluated | by  | native | English |     |
| ---------- | ------ | --------- | ---- | ------------- | --- | -------------- | --- | ---- | --------- | --- | ------ | ------- | --- |
| marization | models | solicited | from | crowd-sourced |     |                |     |      |           |     |        |         |     |
and expert judges. Annotations were collected speakers. Compensation was carefully calculated
for 100 articles randomly picked from the toensureanaveragewageof12USDperhour.
CNN/DailyMail test set. To ensure high qual- Gillick and Liu (2010) showed that summary
ity of annotations, each summary was scored by judgments obtained through non-experts may
5 crowd-sourced and 3 expert workers, amount- differ greatly from expert annotations and could
ing to 12800 summary-level annotations. Model exhibit worse inter-annotator agreement. As a
outputs were evaluated along the following four result, in addition to the hired crowd-sourced
dimensions,asinKrys´cin´skietal.(2019): workers,we enlisted three expertannotators who
Coherence - the collective quality of all sen- have written papers on summarization either for
tences. We align this dimension with the DUC academic conferences (2) or as part of a senior
396

thesis (1). The expert annotators were asked to scored axes, where the overall quality of a sum-
evaluatethesamesetofsummariesunderthesame mary biased scores of the individual dimensions.
instructions as the hired crowd-sourced workers. The histograms also show that while the second
For expert judgments, we proceeded with two round of expertannotations lowered the standard
rounds of annotation to correct any obvious mis- deviation of scores and substantially increased
takesaswellastoconfirmjudgmentsandensurea inter-annotator agreement, relevance and coher-
higherqualityofannotations.Inthesecondround, ence remained the most disagreed on dimensions
annotators were asked to check all examples for between experts. This could be attributed to the
which their score of a dimension differed from subjectivenatureofrelevanceandcoherenceasan
anotherannotatorbymorethan2pointsandwhere evaluationdimensions(Krys´cin´skietal.,2020).
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
the other annotators were within 1 point of each Toassessthesimilarityofannotationsbetween
thecrowd-sourcedandexpertannotators,weaver-
other.Incaseswhereascoredifferedbymorethan
2 points for which such a pattern did not exist, aged the assigned scores per example within the
all annotators examined the annotation. When respective annotator groups and computed Pear-
re-evaluating examples, judges were allowed to son’scorrelationcoefficient.Thestatisticreturned
|            |          |     |          |        |            |     | a value | close to | 0, indicating |     | no correlation |     |
| ---------- | -------- | --- | -------- | ------ | ---------- | --- | ------- | -------- | ------------- | --- | -------------- | --- |
| see scores | assigned |     | by other | expert | annotators | in  |         |          |               |     |                |     |
thefirstroundofannotations.Whilesuchasetting betweenexpertandcrowd-sourcedjudges.
could undermine the wisdom of the crowd and We also manually inspected the human anno-
|           |             |     |        |         |             |     | tations | and present | examples |     | of  | annotated |
| --------- | ----------- | --- | ------ | ------- | ----------- | --- | ------- | ----------- | -------- | --- | --- | --------- |
| shift the | re-assigned |     | scores | towards | the average |     |         |             |          |     |     |           |
judgment from the first round, we encouraged summaries, both generated and reference, as
experts to remain critical and discuss contested well as the differences in human judgments in
|          |            |            |           |     |                |     | Table 1a.                | The first | row | shows | a well  | written, |
| -------- | ---------- | ---------- | --------- | --- | -------------- | --- | ------------------------ | --------- | --- | ----- | ------- | -------- |
| examples | when       | necessary. |           | For | completeness,  |     |                          |           |     |       |         |          |
|          |            |            |           |     |                |     | comprehensivesummary.The |           |     | high  | quality | of the   |
| the data | collection | user       | interface |     | and additional |     |                          |           |     |       |         |          |
details regarding the data collection process are summary is reflected by top scores assigned by
expertannotators,whilebeingratedasaverageby
presentedintheAppendix.
crowd-sourcedworkers.Thesecondrowshowsa
5 Metric Re-evaluation summarywithambiguouspronounusageandfac-
tualinconsistencies.Theerrorsresultinadecrease
5.1 HumanAnnotations in coherence, consistency, and relevance scores
Considering the concerns raised in previous in the expert annotations, but do not see a corre-
work (Gillick and Liu, 2010) about the quality sponding decrease in crowd-worker annotations.
Thethirdrowpresentsafactuallycorrectsummary
| differences | between |     | crowd-sourced |     | and | expert |     |     |     |     |     |     |
| ----------- | ------- | --- | ------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
annotations we study this issue using the human that contains token and phrase repetitions. The
annotationscollectedaspartofthiswork. errorswerecaughtbytheexpertannotatorsresult-
To evaluate the inter-annotator agreement ing in a low fluency score, while crowd-sourced
of collected crowd-sourced and expert anno- annotators incorrectly classified them as issues
tations we computed the Krippendorff’s alpha with factual consistency. These examples again
coefficient (Krippendorff, 2011). We found the illustrate the disparities in the understanding of
|                 |     |          |       |     |          |     | evaluated | dimensions | between | judges | and | under- |
| --------------- | --- | -------- | ----- | --- | -------- | --- | --------- | ---------- | ------- | ------ | --- | ------ |
| inter-annotator |     | interval | kappa | to  | be below | an  |           |            |         |        |     |        |
acceptable range—0.4920 and 0.4132 for the scoreourobservationaboveabouttheuniformity
crowd-sourced workers and the first round of ofcrowd-sourcedannotations;thecrowd-sourced
expert annotations, respectively. However, the annotations tend to be similar across quality
second round of expert annotations improved the dimensions even when distinctions exist, which
inter-annotator agreement, achieving a kappa arecapturedintheexpertannotations.
|             |     |          |            |         |            |     | Results      | presented         | in this | section      | highlight | the   |
| ----------- | --- | -------- | ---------- | ------- | ---------- | --- | ------------ | ----------------- | ------- | ------------ | --------- | ----- |
| coefficient | of  | 0.7127.  | For        | further | insights,  |     |              |                   |         |              |           |       |
|             |     |          |            |         |            |     | difficulties | of crowd-sourcing |         | high-quality |           | anno- |
| we computed |     | standard | deviations |         | of annota- |     |              |                   |         |              |           |       |
tor scores within the respective groups and tationsandthenecessityforprotocolsforimprov-
presenthistograms of those statistics in Figure 1. inghumanevaluationintextsummarization.
| Plots of     | crowd-sourced                     |     | annotations |     | show | strong |                      |     |     |     |     |     |
| ------------ | --------------------------------- | --- | ----------- | --- | ---- | ------ | -------------------- | --- | --- | --- | --- | --- |
|              |                                   |     |             |     |      |        | 5.2 AutomaticMetrics |     |     |     |     |     |
| similarities | acrossallevaluateddimensions.Such |     |             |     |      |        |                      |     |     |     |     |     |
an effect could be caused by an insufficient dis- Many automatic metrics have been proposed for
tinction made by the annotators between the 4 evaluating both summarization and other text
397

Expert Crowd-worker
GeneratedSummaries
scores(avg.) scores(avg.)
thequeen’sguardwasleftred-facedafterheslippedonahe Coh:5.0 Coh:3.4
manholecoverlosthisfootingandslidsideways,knockinghis Con:5.0 Con:3.8
bearskinontheside.theembarrassedsoldierquicklyscrambled Flu:5.0 Flu:3.4
tohisfeetashiscolleaguesmarchedpastasifnothinghad Rel:5.0 Rel:3.8
happened.touristdavidmeadwellrecordedtheunscheduled
manouevreoutsidebuckinghampalaceonthursdayafternoon.
holidaymakerdavidmeadwellrecordedtheunscheduled Coh:2.7 Coh:3.2
manouevreoutsidebuckinghampalace.helosthisfootingand Con:2.0 Con:3.4
slidsideways,knockingbearskinonthesideofthebox.queen’s Flu:4.7 Flu:3.4
guardwasleftred-facedafterheslippedonmanholecover. Rel:3.7 Rel:4.0
theentireincidentwascaughtonamanholecover.theembarrassed
soldierquicklyscrambledtohisfeetashiscolleaguesmarchedpast.
buckinghampalaceguardslippedonmanholecoverinfront Coh:3.3 Coh:3.0
ofhundredsofhorrifiedtourists.thequeen’sguardwasleft Con:5.0 Con:3.2
red-facedafterheslippedonamanholecover.helosthisfooting Flu:1.7 Flu:2.8
anddroppedhisrifleonthesideoftheboxanddroppinghisrifle. Rel:4.3 Rel:3.2
theincidentwascaughtoncameracameracamera.theguardis
thoughttohaveslippedbecauseofmetalshuttersnailedtothe
solesofhisboots.
(a)Generatedsummaryexamplesillustratecommonproblemsfoundinmodeloutputs,suchasambiguous
pronouns,incorrectreferences,andrepetitivecontent.
Expert Crowd-worker
ReferenceSummaries
scores(avg.) scores(avg.)
riverplateadmitthey‘dream’ofmanchesterunitedstriker Coh:3.0 Coh:3.0
radamelfalcao.thecolombiainternationalspenteightyears Con:2.0 Con:3.6
withtheargentineclub.falcaohasmanagedjustfourgoalsin Flu:5.0 Flu:3.0
19premierleagueappearances.read:falcaostill‘hasfaith’ Rel:2.3 Rel:4.4
thathecouldcontinueatmanutdnextseason.clickherefor
thelatestmanchesterunitednews.
theincidentoccurredonapril7northofpolandinthebaltic Coh:2.0 Coh:4.0
sea.u.s.saysplanewasininternationalairspace.russiasays Con:1.7 Con:3.4
ithadtransponderturnedoffandwasflyingtowardrussia Flu:3.0 Flu:4.2
Rel:2.3 Rel:3.6
(b)ReferencesummarieshighlightissuesfoundintheCNN/DailyMaildataset,suchasclick-baitsand
referencestootherarticlesaswellasunreferenceddatesandlowcoherencecausedbyconcatenating
bullet-pointsummaries.
Table 1: Example summaries with the corresponding averaged expert and crowd-sourced annotations
for coherence, consistency, fluency, and relevance. Expert annotations better differentiate coherence,
consistency,andfluencyamongtheexampleswhencomparedtothecrowd-sourcedannotations.
generation models. However, the field lacks a judgmentscalculatedonasystem-levelfollowing
comprehensivestudythatwouldofferaconsistent Louis and Nenkova (2013). The statistics were
side-by-sidecomparisonoftheirperformance.We computed using the available expert annotations
addressthisissuewiththefollowingexperiments. toavoidpossiblequalityproblemsassociatedwith
In Table 2 we show Kendall’s tau rank cor- crowd-sourcedratings,ashighlightedintheprevi-
relations between automatic metrics and human oussubsection.Automaticmetricswerecomputed
398
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026

Figure 1: Histogram of standard deviations of inter-annotator scores between: crowd-sourced
annotations,firstroundexpertannotations,andsecondroundexpertannotations,respectively.
Figure2:PairwiseKendall’staucorrelationsforallautomaticevaluationmetrics.
inamulti-referencesetting,usingtheoriginalref- majority of metrics rely on hard or soft subse-
erence summary included in the CNN/DailyMail quencealignments,whichdonotmeasurewellthe
datasetand10additionalsummariescomingfrom interdependence between consecutive sentences.
Krys´cin´ski et al. (2020), and the length of model Low and moderate correlation scores were also
outputs was not constrained. We report correla- found for the relevance dimension. As discussed
tions without differentiating between abstractive intheprevioussubsection,suchtrendscouldresult
and extractive models, as most metrics did not from the inherent subjectiveness of the dimen-
exhibit large differences in correlation when sion and the difficulty of collecting consistent
reportedseparately. human annotations. Model correlations increase
Correlation results show several trends. We considerably across the consistency and fluency
find that most metrics have the lowest correla- dimensions.Althoughunexpected,thestrongcor-
tion within the coherence dimension, where the relationwithconsistencycouldbeattributedtothe
correlation strength can be classified as weak or lowabstractivenessofmostneuralmodels,which
moderate. This finding follows intuition as the could increase the effectiveness of metrics using
399
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026

Metric Coherence Consistency Fluency Relevance strong correlation between all metrics that com-
| ROUGE-1 |     | 0.2500 | 0.5294 | 0.5240 | 0.4118 |                  |           |                |     |           |            |         |
| ------- | --- | ------ | ------ | ------ | ------ | ---------------- | --------- | -------------- | --- | --------- | ---------- | ------- |
|         |     |        |        |        |        | pute, implicitly |           | or explicitly, |     | the       | lexical    | overlap |
| ROUGE-2 |     | 0.1618 | 0.5882 | 0.4797 | 0.2941 |                  |           |                |     |           |            |         |
|         |     |        |        |        |        | between          | generated |                | and | reference | summaries. |         |
| ROUGE-3 |     | 0.2206 | 0.7059 | 0.5092 | 0.3529 |                  |           |                |     |           |            |         |
ROUGE-4 0.3088 0.5882 0.5535 0.4118 Metricsmeasuringthen-gramnoveltyandrepet-
| ROUGE-L   |     | 0.0735 | 0.1471 | 0.2583 | 0.2353 |                   |      |        |          |        |             |           |
| --------- | --- | ------ | ------ | ------ | ------ | ----------------- | ---- | ------ | -------- | ------ | ----------- | --------- |
|           |     |        |        |        |        | itiveness         | show | a weak | negative |        | correlation | with      |
| ROUGE-su* |     | 0.1912 | 0.2941 | 0.4354 | 0.3235 |                   |      |        |          |        |             |           |
|           |     |        |        |        |        | all ROUGE-related |      |        | metrics. | Length | as          | a feature |
| ROUGE-w   |     | 0.0000 | 0.3971 | 0.3764 | 0.1618 |                   |      |        |          |        |             |           |
ROUGE-we-1 0.2647 0.4559 0.5092 0.4265 isweaklycorrelatedwithmostmetricsapartfrom
| ROUGE-we-2 | −0.0147 |        | 0.5000 | 0.3026 | 0.1176 | S3       |     |             |     |       |       |         |
| ---------- | ------- | ------ | ------ | ------ | ------ | -------- | --- | ----------- | --- | ----- | ----- | ------- |
|            |         |        |        |        |        | , BLANC, |     | and SuPERT, |     | which | might | suggest |
| ROUGE-we-3 |         | 0.0294 | 0.3676 | 0.3026 | 0.1912 |          |     |             |     |       |       |         |
S3-pyr −0.0294 0.5147 0.3173 0.1324 the mentioned metrics favor longer summaries.
| S3-resp | −0.0147 |     |     |     |     | Worth | noting | is also | the | weak | correlation | of  |
| ------- | ------- | --- | --- | --- | --- | ----- | ------ | ------- | --- | ---- | ----------- | --- |
0.5000 0.3321 0.1471 Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
−0.1912
BertScore-p 0.0588 0.0074 0.1618 reference-lessSummaQA,BLANC,andSuPERT
| BertScore-r |     | 0.1471 | 0.6618 | 0.4945 | 0.3088 |     |     |     |     |     |     |     |
| ----------- | --- | ------ | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
metricswithmostotherevaluatedmetrics.
| BertScore-f |     | 0.2059 | 0.0441 | 0.2435 | 0.4265 |     |     |     |     |     |     |     |
| ----------- | --- | ------ | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
−0.0294
MoverScore 0.1912 0.2583 0.2941 Results presented in this section highlight the
SMS 0.1618 0.5588 0.3616 0.2353 evaluation dimensions that are not reliably cov-
| SummaQAˆ |     | 0.1176 | 0.6029 | 0.4059 | 0.2206 |     |     |     |     |     |     |     |
| -------- | --- | ------ | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
BLANCˆ 0.0735 0.5588 0.3616 0.2647 ered by currently available metrics and pave the
| SUPERTˆ |     | 0.1029 | 0.5882 | 0.4207 | 0.2353 |     |     |     |     |     |     |     |
| ------- | --- | ------ | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
wayforfutureworkinmodelevaluation.
| BLEU          |         | 0.1176 | 0.0735  | 0.3321  | 0.2206 |         |               |       |          |     |       |        |
| ------------- | ------- | ------ | ------- | ------- | ------ | ------- | ------------- | ----- | -------- | --- | ----- | ------ |
| CHRF          |         | 0.3971 | 0.5294  | 0.4649  | 0.5882 |         |               |       |          |     |       |        |
| CIDEr         |         | 0.1176 | −0.1912 | −0.0221 | 0.1912 | 6 Model | Re-evaluation |       |          |     |       |        |
| METEOR        |         | 0.2353 | 0.6324  | 0.6126  | 0.4265 |         |               |       |          |     |       |        |
| Lengthˆ       | −0.0294 |        | 0.4265  | 0.2583  | 0.1618 |         |               |       |          |     |       |        |
|               |         |        |         |         |        | We now  | turn          | to an | analysis | of  | model | scores |
| Novelunigramˆ |         | 0.1471 | −0.2206 | −0.1402 | 0.1029 |         |               |       |          |     |       |        |
Novelbi-gramˆ 0.0294 −0.5441 −0.3469 −0.1029 across human evaluations and automatic metrics.
Noveltri-gramˆ 0.0294 −0.5735 −0.3469 −0.1324 The evaluated models were released between
| Repeatedunigramˆ | −0.3824 |     | 0.1029  | −0.0664 | −0.3676 |          |       |           |     |           |            |     |
| ---------------- | ------- | --- | ------- | ------- | ------- | -------- | ----- | --------- | --- | --------- | ---------- | --- |
|                  |         |     |         |         |         | 2017 and | 2019, | represent |     | different | approaches |     |
| Repeatedbi-gramˆ | −0.3824 |     | −0.0147 | −0.2435 | −0.4559 |          |       |           |     |           |            |     |
Repeatedtri-gramˆ −0.2206 0.1471 −0.0221 −0.2647 to summarization: abstractive, extractive, and
Stats-coverageˆ −0.1324 0.3529 0.1550 −0.0294 hybrid,andtheirarchitecturesreflectthetrendsin
| Stats-compressionˆ |           | 0.1176          | −0.4265 | −0.2288      | −0.0147 |                    |       |                   |               |              |            |          |
| ------------------ | --------- | --------------- | ------- | ------------ | ------- | ------------------ | ----- | ----------------- | ------------- | ------------ | ---------- | -------- |
|                    |           |                 |         |              |         | summarization      |       | research.Although |               |              | in many    | cases    |
| Stats-densityˆ     |           | 0.1618          | 0.6471  | 0.3911       | 0.2941  |                    |       |                   |               |              |            |          |
|                    |           |                 |         |              |         | weobtainedmultiple |       |                   | variantsofthe |              | samemodel, |          |
| Table 2:           | Kendall’s | tau correlation |         | coefficients | of      |                    |       |                   |               |              |            |          |
|                    |           |                 |         |              |         | in the             | study | we focus          | on            | the versions |            | with the |
expert annotations computed on a system-level highestROUGE-Lscores.
| along    | four quality | dimensions   |       | with      | automatic  |         |             |          |             |     |                 |       |
| -------- | ------------ | ------------ | ----- | --------- | ---------- | ------- | ----------- | -------- | ----------- | --- | --------------- | ----- |
|          |              |              |       |           |            | Table   | 3 contains  |          | the results |     | of human        | eval- |
| metrics  | using        | 11 reference |       | summaries | per        |         |             |          |             |     |                 |       |
|          |              |              |       |           |            | uation  | across      | the four | dimensions  |     | described       | in    |
| example. | ˆ denotes    | metrics      | which | use       | the source |         |             |          |             |     |                 |       |
|          |              |              |       |           |            | Section | 4.3. Scores |          | for ground  |     | truth summaries |       |
document. The five most-correlated metrics in areincluded as a point of reference.We find that
eachcolumnarebolded.
pretrainedmodelssuchasPegasus,BART,andT5
|     |     |     |     |     |     | consistently | performed |     | best | on most | dimensions. |     |
| --- | --- | --- | --- | --- | --- | ------------ | --------- | --- | ---- | ------- | ----------- | --- |
Notably,thementionedmodelsscoredhigheston
higher-order n-gram overlap, such as ROUGE-3 consistency and fluency while obtaining lower
orExtractiveDensity.Referringbacktotheprevi- scores for relevance and coherence. Scores for
oussubsection,bothofthementioneddimensions
|     |     |     |     |     |     | extractive | models | highlight |     | the | known | short- |
| --- | --- | --- | --- | --- | --- | ---------- | ------ | --------- | --- | --- | ----- | ------ |
achievedhigh inter-annotatoragreementbetween comings of such approaches, which are lack of
expert judges which could also positively affect coherenceofsummariesandissueswithselecting
the correlation scores. Additionally, the results relevant content. Abstractive model ratings show
show a substantially higher correlation between an increasing trend with respect to the date of
allevaluateddimensionsandROUGEscorescom- publication. This is a promising result as it sug-
higher-ordern-grams
puted for in comparison to geststhatthequalityofmodelsisimprovingwith
| ROUGE-L, | which | corroborates |     | with findings | of  |             |        |     |      |          |      |           |
| -------- | ----- | ------------ | --- | ------------- | --- | ----------- | ------ | --- | ---- | -------- | ---- | --------- |
|          |       |              |     |               |     | time. Worth | noting | is  | also | the fact | that | reference |
Rankeletal.(2013). summaries did not score well on consistency,
Toexaminethedependenciesbetweendifferent coherence, and relevance. Upon examination of
metrics, we computed Kendall’s tau rank corre- theannotations,wefoundthatthereferencesum-
lation coefficients, pairwise, between all metrics. maries often contained extraneous information,
Results are presented as a correlation matrix such as hyperlinks and click-bait descriptions of
in Figure 2. Following intuition, we observe a otherarticles.Asthisinformationwasnotpresent
400

|     | Method                 |     |     |     | Coherence |     | Consistency | Fluency |     | Relevance |     |     |
| --- | ---------------------- | --- | --- | --- | --------- | --- | ----------- | ------- | --- | --------- | --- | --- |
|     | CNN/DMReferenceSummary |     |     |     | 3.26      |     | 4.47        | 4.79    |     | 3.77      |     |     |
ExtractiveModels
|     | M0-LEAD-3    |     |     |     | 4.16 |     | 4.98 | 4.94 |     | 4.14 |     |     |
| --- | ------------ | --- | --- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | --- |
|     | M1-NEUSUM    |     |     |     | 3.22 |     | 4.98 | 4.90 |     | 3.82 |     |     |
|     | M2-BanditSum |     |     |     | 3.28 |     | 4.99 | 4.83 |     | 3.81 |     |     |
|     | M5-RNES      |     |     |     | 3.71 |     | 4.97 | 4.81 |     | 4.06 |     |     |
AbstractiveModels
|     | M8-PointerGenerator |     |     |     | 3.29 |     | 4.65 | 4.79 |     | 3.55 |     |     |
| --- | ------------------- | --- | --- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | --- |
|     | M9-Fast-abs-rl      |     |     |     | 2.38 |     | 4.67 | 4.50 |     | 3.52 |     |     |
|     | M10-Bottom-Up       |     |     |     | 2.73 |     | 4.25 | 4.42 |     | 3.38 |     |     |
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
|     | M11-Improve-abs     |     |     |     | 2.28 |     | 3.27 | 3.65 |     | 3.15 |     |     |
| --- | ------------------- | --- | --- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | --- |
|     | M12-Unified-ext-abs |     |     |     | 3.60 |     | 4.96 | 4.85 |     | 3.85 |     |     |
|     | M13-ROUGESal        |     |     |     | 3.44 |     | 4.82 | 4.86 |     | 3.83 |     |     |
M14-Multi-task(Ent+QG)
|     |                       |     |     |     | 3.20 |     | 4.90 | 4.74 |     | 3.63 |     |     |
| --- | --------------------- | --- | --- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | --- |
|     | M15-Closedbookdecoder |     |     |     | 3.35 |     | 4.95 | 4.80 |     | 3.67 |     |     |
|     | M17-T5                |     |     |     | 4.00 |     | 4.93 | 4.93 |     | 4.23 |     |     |
M20-GPT-2(zeroshot)1
|     |                         |     |     |     | 3.63 |     | 3.40 | 3.97 |     | 3.30 |     |     |
| --- | ----------------------- | --- | --- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | --- |
|     | M22-BART                |     |     |     | 4.18 |     | 4.94 | 4.90 |     | 4.25 |     |     |
|     | M23-Pegasus(C4)         |     |     |     | 4.16 |     | 4.91 | 4.88 |     | 4.26 |     |     |
|     | M23-Pegasus(dynamicmix) |     |     |     | 4.09 |     | 4.85 | 4.79 |     | 4.27 |     |     |
Table 3: Human ratings of summaries along four evaluation dimensions,
averagedoverthreeexpertannotators,brokendownbyextractiveandabstractive
models. The M* codes follow the notation described in Section 3.2. The three
highest-ratedmodelsineachcolumnareinbold.
in the source documents nor relevant for the Presented results provide a comprehensive
summaries, the annotators interpreted it as hal- perspective on the current state of the field and
lucinations and assigned lower consistency and highlightdirectionsforfuturemodelingwork.
| relevance            | scores. | Additionally,             |     | many    | reference |     |     |     |     |     |     |     |
| -------------------- | ------- | ------------------------- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| summaries            | in      | the CNN/DailyMail         |     | dataset | were      |     |     |     |     |     |     |     |
| constructedbynaively |         | concatenatingbullet-point |     |         |           |     |     |     |     |     |     |     |
7 Conclusions
| summaries | into | contiguous | sequences. |     | Such pro- |     |     |     |     |     |     |     |
| --------- | ---- | ---------- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
cessingstepsnegativelyaffectedthecoherenceof
| examples.Similar |     | trendsin | humanstudiesofref- |     |     |     |            |           |     |       |              |     |
| ---------------- | --- | -------- | ------------------ | --- | --- | --- | ---------- | --------- | --- | ----- | ------------ | --- |
|                  |     |          |                    |     |     | We  | introduced | SummEval, |     | a set | of resources |     |
erencesummarieswerereportedbyStiennonetal. forsummarizationmodelandevaluationresearch
(2020). Examples of noisy reference summaries that include: a collection of summaries generated
are shown in Table 1b. Table 4 shows scores by recent summarization models on the
| formodeloutputsacrossall |     |     | automatic |     | evaluation |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
CNN/DailyMaildataset,anextensibleandunified
metrics. Parameters of metrics used in this study toolkit for summarization model evaluation, and
can be found in the evaluation toolkit repository a diverse collection of human annotations of
| listed inSection1.Theresultsalign |     |     |     | with | insights |       |         |           |     |          |              |     |
| --------------------------------- | --- | --- | --- | ---- | -------- | ----- | ------- | --------- | --- | -------- | ------------ | --- |
|                                   |     |     |     |      |          | model | outputs | collected |     | from the | crowd-source |     |
coming from the human evaluation of models. and expert annotators. Using the accumulated
Wefoundthatformostmetrics,thehighestscores resources we re-evaluated a broad selection of
were assigned to large models pretrained on vast current models and evaluation metrics in a
quantitiesofdata.However,severalmetrics,such
|     |     |     |     |     |     | consistent |     | and comprehensive |     | manner. |     | We hope |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ----------------- | --- | ------- | --- | ------- |
S3
as , SummaQA, SMS, CHRF, and METEOR that this work will prove to be a valuable
tended to favor extractive models, assigning the resourceforfutureresearchontextsummarization
highestscorestotheiroutputs.
|     |     |     |     |     |     | evaluation   |     | and models. |         | We also  | encourage | the |
| --- | --- | --- | --- | --- | --- | ------------ | --- | ----------- | ------- | -------- | --------- | --- |
|     |     |     |     |     |     | research     |     | community   | to      | join our | efforts   | by  |
|     |     |     |     |     |     | contributing |     | model       | outputs | and      | extending | the |
1Thezero-shotmodelwasusedforevaluation. evaluationtoolkitwithnewmetrics.
401

Method ROUGE-1/2/3/4/L/su*/w ROUGE-WE-(1/2/3) S3(pyr/resp) BertScore MoverScore SummaQA SMS BLANC SUPERT
ExtractiveModels
M0-LEAD-3 0.3994/0.1746/0.0990/0.0647/0.3606/0.1377/0.2072 0.4049/0.2260/0.2172 0.5395/0.6328 0.3742 0.1679 0.1652 0.1050 0.0480 0.7259
M1-NEUSUM 0.4130/0.1893/0.1109/0.0742/0.3768/0.1495/0.2156 0.4186/0.2402/0.2310 0.5562/0.6509 0.3955 0.1839 0.1700 0.1062 0.1087 0.7010
M2-BanditSum 0.4137/0.1868/0.1086/0.0721/0.3759/0.1513/0.2139 0.4195/0.2385/0.2300 0.5339/0.6306 0.3938 0.1815 0.1324 0.1058 0.0909 0.7018
M3-LATENT 0.4136/0.1867/0.1085/0.0721/0.3757/0.1512/0.2138 0.4194/0.2384/0.2299 0.5337/0.6305 0.3936 0.1814 0.1645 0.1058 0.0910 0.7020
M4-REFRESH 0.3972/0.1807/0.1042/0.0690/0.3621/0.1340/0.2129 0.4023/0.2318/0.2238 0.6395/0.7124 0.3903 0.1720 0.1944 0.1088 0.1406 0.7526
M5-RNES 0.4088/0.1878/0.1102/0.0736/0.3719/0.1446/0.2163 0.4153/0.2395/0.2317 0.6082/0.6894 0.3997 0.1802 0.1794 0.1107 0.1232 0.7434
M6-JECS 0.4144/0.1846/0.1063/0.0699/0.3760/0.1485/0.2135 0.4200/0.2371/0.2283 0.5337/0.6284 0.3925 0.1805 0.1644 0.1048 0.1044 0.6946
M7-STRASS 0.3377/0.1237/0.0650/0.0416/0.2790/0.1052/0.1559 0.3477/0.1757/0.1656 0.3632/0.4939 0.3090 0.1079 0.1367 0.1023 0.1042 0.6566
AbstractiveModels
M8-PointerGenerator 0.3921/0.1723/0.1003/0.0674/0.3599/0.1435/0.1999 0.3990/0.2226/0.2128 0.4328/0.5561 0.3763 0.1643 0.1398 0.0974 0.0704 0.6501
M9-Fast-abs-rl 0.4057/0.1774/0.0975/0.0616/0.3806/0.1439/0.2112 0.4123/0.2302/0.2184 0.4818/0.5865 0.3918 0.1748 0.1431 0.0847 0.0855 0.6125
M10-Bottom-Up 0.4124/0.1870/0.1064/0.0695/0.3815/0.1543/0.2084 0.4192/0.2400/0.2313 0.4450/0.5655 0.3964 0.1830 0.1408 0.0925 0.0570 0.6092
M11-Improve-abs 0.3985/0.1720/0.0927/0.0567/0.3730/0.1431/0.2073 0.4045/0.2300/0.2228 0.4899/0.5897 0.3826 0.1652 0.1341 0.0816 0.0777 0.5972
M12-Unified-ext-abs 0.4038/0.1790/0.1039/0.0695/0.3675/0.1484/0.2074 0.4097/0.2299/0.2204 0.4936/0.5995 0.3832 0.1739 0.1530 0.1038 0.0962 0.6826
M13-ROUGESal 0.4016/0.1797/0.1053/0.0709/0.3679/0.1497/0.2058 0.4078/0.2294/0.2190 0.4643/0.5799 0.3837 0.1722 0.1475 0.1009 0.0882 0.6570
M14-Multi-task(Ent+QG) 0.3952/0.1758/0.1037/0.0705/0.3625/0.1476/0.2007 0.4015/0.2253/0.2149 0.4246/0.5513 0.3759 0.1670 0.1360 0.0982 0.0648 0.6380
M15-Closedbookdecoder 0.3976/0.1760/0.1031/0.0696/0.3636/0.1472/0.2033 0.4039/0.2263/0.2160 0.4591/0.5757 0.3783 0.1699 0.1456 0.1009 0.0896 0.6612
M16-SENECA 0.4151/0.1836/0.1052/0.0681/0.3806/0.1520/0.2112 0.4211/0.2369/0.2282 0.4735/0.5836 0.3907 0.1811 0.1404 0.1005 0.0692 0.6519
M17-T5 0.4479/0.2205/0.1336/0.0920/0.4172/0.1879/0.2291 0.4543/0.2723/0.2631 0.5168/0.6294 0.4450 0.2376 0.1437 0.1046 0.0773 0.6094
M18-NeuralTD 0.4004/0.1762/0.1000/0.0650/0.3723/0.1452/0.2085 0.4063/0.2277/0.2187 0.4946/0.5975 0.3949 0.1697 0.1440 0.0916 0.0859 0.6290
M19-BertSum-abs 0.4163/0.1944/0.1156/0.0785/0.3554/0.1625/0.1979 0.4230/0.2454/0.2351 0.4664/0.5855 0.3855 0.1894 0.1385 0.1071 0.0815 0.6116
M20-GPT-2(supervised) 0.3981/0.1758/0.0993/0.0649/0.3674/0.1470/0.2006 0.4048/0.2268/0.2170 0.4069/0.5373 0.3915 0.1750 0.1299 0.0930 0.0705 0.6053
M21-UniLM 0.4306/0.2044/0.1218/0.0824/0.4013/0.1714/0.2228 0.4369/0.2567/0.2483 0.5143/0.6210 0.4122 0.2112 0.1455 0.0957 0.0841 0.6100
M22-BART 0.4416/0.2128/0.1285/0.0880/0.4100/0.1818/0.2266 0.4472/0.2646/0.2556 0.5116/0.6215 0.4264 0.2259 0.1457 0.1037 0.0822 0.6184
M23-Pegasus(dynamicmix) 0.4407/0.2155/0.1307/0.0901/0.4101/0.1825/0.2260 0.4471/0.2668/0.2575 0.5099/0.6233 0.4369 0.2283 0.1422 0.1040 0.0797 0.6046
M23-Pegasus(hugenews) 0.4408/0.2147/0.1295/0.0889/0.4103/0.1821/0.2273 0.4473/0.2663/0.2568 0.5295/0.6372 0.4377 0.2286 0.1497 0.1049 0.0845 0.6148
(a)Modelscoresfromsummarization-specificevaluationmetrics.
Method BLEU CHRF CIDEr METEOR Length Stats(cov/comp/den) Repeated(1/2/3)
ExtractiveModels
M0-LEAD-3 11.4270 0.3892 0.2125 0.2141 87.4475 0.9825/9.6262 /57.8001 0.2086/0.0310/0.0310
M1-textbfNEUSUM 12.7784 0.3946 0.2832 0.2183 84.4075 0.9819/9.8047 /32.8574 0.2325/0.0531/0.0531
M2-BanditSum 12.9761 0.3897 0.3305 0.2124 78.5279 0.9836/10.2810/40.4265 0.2384/0.0573/0.0573
M3-LATENT 12.9725 0.3897 0.3305 0.2123 78.5279 0.9834/10.2809/40.4095 0.2384/0.0573/0.0573
M4-REFRESH 10.6568 0.4526 0.0677 0.2395 114.5684 0.9850/7.1059 /53.1928 0.2127/0.0289/0.0289
M5-RNES 11.2203 0.4062 0.1559 0.2300 99.9199 0.9938/7.9032 /67.7089 0.2451/0.0540/0.0540
M6-JECS 12.5659 0.4310 0.3090 0.2122 79.7797 0.9874/10.1111/26.6943 0.2041/0.0327/0.0327
M7-STRASS 7.8330 0.3330 0.2945 0.1607 76.4859 0.9969/12.7835/59.9498 0.1864/0.0343/0.0343
AbstractiveModels
M8-PointerGenerator 13.8247 0.3567 0.5065 0.1860 63.5211 0.9957/13.1940/26.0880 0.2015/0.0375/0.0375
M9-Fast-abs-rl 12.9812 0.3778 0.4329 0.2014 70.8600 0.9860/11.0141/ 9.9859 0.2157/0.0370/0.0370
M10-Bottom-Up 15.1293 0.3523 0.6176 0.1887 56.5715 0.9811/14.7771 /12.6181 0.1856/0.0211/0.0211
M11-Improve-abs 11.9816 0.3715 0.3356 0.2005 75.9512 0.9674/10.6043/8.9755 0.2499/0.0542/0.0542
M12-Unified-ext-abs 12.8457 0.3786 0.3851 0.2017 74.4663 0.9868/10.7510/33.1106 0.2177/0.0493/0.0493
M13-ROUGESal 13.8882 0.3668 0.4746 0.1936 66.5575 0.9853/13.0369/25.2893 0.2102/0.0458/0.0458
M14-Multi-task(Ent+QG) 14.5276 0.3539 0.5749 0.1831 60.0294 0.9853/14.1828/22.2296 0.1985/0.0411/0.0411
M15-Closedbookdecoder 13.4158 0.3675 0.4648 0.1925 68.2858 0.9866/12.0588/27.3686 0.2074/0.0444/0.0444
M16-SENECA 13.7676 0.3660 0.5233 0.1966 64.9710 0.9880/12.3610/16.7640 0.2146/0.0303/0.0303
M17-T5 19.3891 0.3833 0.7763 0.2140 59.5288 0.9775/14.2002/12.9565 0.1810/0.0209/0.0209
M18-NeuralTD 12.9241 0.3783 0.3543 0.2038 74.4033 0.9830/10.7768/12.4443 0.2645/0.0901/0.0901
M19-BertSum-abs 14.9525 0.3649 0.6240 0.1876 60.8893 0.9517/13.9197/12.3254 0.1697/0.0156/0.0156
M20-GPT-2(supervised) 13.9364 0.3678 0.5787 0.1759 51.8352 0.9791/15.9839/15.4999 0.1875/0.0362/0.0362
M21-UniLM 15.5736 0.4230 0.5294 0.2084 67.1960 0.9685/11.5672/11.7908 0.1722/0.0180/0.0180
M22-BART 17.1005 0.4271 0.7573 0.2105 62.2989 0.9771/12.8811/15.2999 0.1627/0.0127/0.0127
M23-Pegasus(dynamicmix) 18.6517 0.4261 0.7280 0.2131 64.1348 0.9438/13.7208/11.6003 0.1855/0.0355/0.0081
M23-Pegasus(hugenews) 17.8102 0.3912 0.6595 0.2189 66.7559 0.9814/12.9473/14.9850 0.1883/0.0251/0.0251
(b)Modelscoresfromothertextgenerationevaluationmetrics.
Table 4: Model scores from automatic evaluation metrics available in the evaluation toolkit. The five
highestscoresforeachmetric(andlowestforLengthandRepeated-1/2/3)arebolded.
8 Acknowledgments Processing and the 9th International Joint
Conference on Natural Language Processing
We thank all authors for sharing model outputs
(EMNLP-IJCNLP), pages 3110–3120, Hong
andTonyWongforassistancewithannotations.
Kong, China. Association for Computational
Linguistics. DOI: https://doi.org/10
References .18653/v1/D19-1307
DzmitryBahdanau,KyunghyunCho,andYoshua
Le´o Bouscarrat, Antoine Bonnefoy, Thomas
Bengio. 2014. Neural machine translation by
Peel, and Ce´cile Pereira. 2019. STRASS: jointly learning to align and translate. arXiv
A light and effective method for extractive
preprintarXiv:1409.0473.
summarization basedon sentenceembeddings.
Florian Bo¨hm, Yang Gao, Christian M. Meyer, In Proceedings of the 57th Annual Meeting
Ori Shapira, Ido Dagan, and Iryna Gurevych. of the Association for Computational
2019. Better rewards yield better summaries: Linguistics: Student Research Workshop,
Learning to summarise without references. pages243–252,Florence,Italy.Associationfor
In Proceedings of the 2019 Conference on Computational Linguistics. DOI: https://
Empirical Methods in Natural Language doi.org/10.18653/v1/P19-2034
402
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026

Arun Chaganty, Stephen Mussmann, and Percy of the Eleventh International Conference on
Liang. 2018. The price of debiasing automatic Language Resources and Evaluation (LREC
metrics in natural language evaluation. In 2018), Miyazaki, Japan. European Language
Proceedingsofthe 56th AnnualMeeting ofthe ResourcesAssociation(ELRA).
| Association |              | for Computational |             |             | Linguistics |             |          |            |                 |     |         |       |
| ----------- | ------------ | ----------------- | ----------- | ----------- | ----------- | ----------- | -------- | ---------- | --------------- | --- | ------- | ----- |
|             |              |                   |             |             |             | Daniel      | Deutsch  | and        |                 | Dan | Roth.   | 2020. |
| (Volume     | 1:           | Long              | Papers),    | pages       | 643–653,    |             |          |            |                 |     |         |       |
|             |              |                   |             |             |             | SacreROUGE: |          | An         | Open-Source     |     | Library | for   |
| Melbourne,  | Australia.   |                   | Association |             | forCompu-   |             |          |            |                 |     |         |       |
|             |              |                   |             |             |             | Using       | and      | Developing | Summarization   |     |         | Eval- |
| tational    | Linguistics. |                   | DOI:        | https://doi |             |             |          |            |                 |     |         |       |
|             |              |                   |             |             |             | uation      | Metrics. | DOI:       | https://doi.org |     |         |       |
.org/10.18653/v1/P18-1060
/10.18653/v1/2020.nlposs-1.17
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
| Yen-Chun | Chen | and | Mohit | Bansal. | 2018. |     |     |     |     |     |     |     |
| -------- | ---- | --- | ----- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
JacobDevlin,Ming-WeiChang,KentonLee,and
Fast abstractive summarization with reinforce- Kristina Toutanova. 2019. BERT: Pre-training
selected sentence rewriting. In Proceedings of ofdeepbidirectionaltransformersforlanguage
| the 56th | Annual | Meeting |     | of the | Association |                |     |     |             |     |     |          |
| -------- | ------ | ------- | --- | ------ | ----------- | -------------- | --- | --- | ----------- | --- | --- | -------- |
|          |        |         |     |        |             | understanding. |     | In  | Proceedings |     | of  | the 2019 |
forComputationalLinguistics(Volume1:Long Conference of the North American Chapter of
Papers),pages675–686,Melbourne,Australia. theAssociationfor Computational Linguistics:
| Association |                             | for Computational |     |     | Linguistics. |              |          |                |               |             |            |     |
| ----------- | --------------------------- | ----------------- | --- | --- | ------------ | ------------ | -------- | -------------- | ------------- | ----------- | ---------- | --- |
|             |                             |                   |     |     |              | Human        | Language |                | Technologies, |             | Volume     | 1   |
| DOI:        | https://doi.org/10.18653/v1 |                   |     |     |              |              |          |                |               |             |            |     |
|             |                             |                   |     |     |              | (Long        | and      | Short Papers), |               | pages       | 4171–4186, |     |
| /P18-1063   |                             |                   |     |     |              | Minneapolis, |          | Minnesota.     |               | Association |            | for |
ComputationalLinguistics.
| Elizabeth | Clark, | Asli | Celikyilmaz, |     | and Noah A. |     |     |     |     |     |     |     |
| --------- | ------ | ---- | ------------ | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Smith. 2019. Sentence mover’s similarity: Li Dong, Nan Yang, Wenhui Wang, Furu
Automatic evaluation for multi-sentence Wei, Xiaodong Liu, Yu Wang, Jianfeng Gao,
|        |                |     |     |     |             | Ming | Zhou, | and | Hsiao-Wuen |     | Hon. | 2019. |
| ------ | -------------- | --- | --- | --- | ----------- | ---- | ----- | --- | ---------- | --- | ---- | ----- |
| texts. | In Proceedings |     | of  | the | 57th Annual |      |       |     |            |     |      |       |
Meeting of the Association for Computational Unifiedlanguagemodelpre-trainingfornatural
Linguistics, pages 2748–2760, Florence, Italy. language understanding and generation. In
|             |                             |                   |     |     |              | Advances                  | in  | Neural | Information |     | Processing |     |
| ----------- | --------------------------- | ----------------- | --- | --- | ------------ | ------------------------- | --- | ------ | ----------- | --- | ---------- | --- |
| Association |                             | for Computational |     |     | Linguistics. |                           |     |        |             |     |            |     |
| DOI:        | https://doi.org/10.18653/v1 |                   |     |     |              | Systems,pages13042–13054. |     |        |             |     |            |     |
/P19-1264
|             |     |       |           |     |              | Yue Dong, | Yikang | Shen, | Eric   | Crawford, |     | Herke   |
| ----------- | --- | ----- | --------- | --- | ------------ | --------- | ------ | ----- | ------ | --------- | --- | ------- |
|             |     |       |           |     |              | van       | Hoof,  | and   | Jackie | Chi       | Kit | Cheung. |
| Arman Cohan | and | Nazli | Goharian. |     | 2016. Revis- |           |        |       |        |           |     |         |
iting summarization evaluation for scientific 2018. BanditSum: Extractive summarization
|                |                |            |             |        |              | as a       | contextual | bandit.  |     | In          | Proceedings | of      |
| -------------- | -------------- | ---------- | ----------- | ------ | ------------ | ---------- | ---------- | -------- | --- | ----------- | ----------- | ------- |
| articles.      | In Proceedings |            |             | of the | Tenth Inter- |            |            |          |     |             |             |         |
|                |                |            |             |        |              | the 2018   | Conference |          | on  | Empirical   |             | Methods |
| national       | Conference     |            | on Language |        | Resources    |            |            |          |     |             |             |         |
|                |                |            |             |        |              | in Natural |            | Language |     | Processing, |             | pages   |
| and Evaluation |                | (LREC’16), |             | pages  | 806–813,     |            |            |          |     |             |             |         |
Portorozˇ, Slovenia. European Language 3739–3748, Brussels, Belgium. Associa-
|     |     |     |     |     |     | tion | for Computational |     |     | Linguistics. |     | DOI: |
| --- | --- | --- | --- | --- | --- | ---- | ----------------- | --- | --- | ------------ | --- | ---- |
ResourcesAssociation(ELRA).
https://doi.org/10.18653/v1/D18
Hoa Trang Dang. 2005. Overview of DUC 2005. -1409,PMID:30577265
| InProceedingsofthe |     |     | documentunderstanding |     |     |              |     |        |     |      |       |       |
| ------------------ | --- | --- | --------------------- | --- | --- | ------------ | --- | ------ | --- | ---- | ----- | ----- |
|                    |     |     |                       |     |     | Esin Durmus, |     | He He, | and | Mona | Diab. | 2020. |
conference,volume2005,pages1–12.
|           |      |     |          |     |            | FEQA:     | A   | question         | answering |     | evaluation |     |
| --------- | ---- | --- | -------- | --- | ---------- | --------- | --- | ---------------- | --------- | --- | ---------- | --- |
|           |      |     |          |     |            | framework |     | for faithfulness |           |     | assessment | in  |
| Hoa Trang | Dang | and | Karolina |     | Owczarzak. |           |     |                  |           |     |            |     |
2008. Overview of the TAC 2008 update abstractive summarization. In Proceedings
summarizationtask.InTAC. of the 58th Annual Meeting of the Asso-
|     |     |     |     |     |     | ciation | for | Computational |     |     | Linguistics, |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------------- | --- | --- | ------------ | --- |
Hoa Trang Dang and Karolina Owczarzak.2009. pages 5055–5070, Online. Association for
| Overview | of  | the | TAC 2009 | summarization |     |               |     |              |     |      |          |     |
| -------- | --- | --- | -------- | ------------- | --- | ------------- | --- | ------------ | --- | ---- | -------- | --- |
|          |     |     |          |               |     | Computational |     | Linguistics. |     | DOI: | https:// |     |
track. In Proceedings of the Text Analysis doi.org/10.18653/v1/2020.acl-
| Conference. |     |     |     |     |     | main.454 |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
Franck Dernoncourt, Mohammad Ghassemi, Kavita Ganesan. 2015. Rouge 2.0: Updated
and Walter Chang. 2018. A repository of and improved measures for evaluation of
corpora for summarization. In Proceedings summarizationtasks.
403

Yang Gao, Wei Zhao, and Steffen Eger. Annual Meeting of the Association for
2020. SUPERT: towards new frontiers in Computational Linguistics (Volume 1: Long
unsupervised evaluation metrics for multi- Papers), pages 687–697, Melbourne, Aus-
document summarization. In Proceedings of tralia. Association for Computational Linguis-
the 58th Annual Meeting of the Association tics. DOI: https://doi.org/10.18653
for Computational Linguistics, ACL 2020, /v1/P18-1064,PMCID:PMC6428206
| Online,     | July | 5-10,             | 2020, | pages | 1347–1354.   |     |          |        |                 |     |                 |         |
| ----------- | ---- | ----------------- | ----- | ----- | ------------ | --- | -------- | ------ | --------------- | --- | --------------- | ------- |
|             |      |                   |       |       |              |     | Hardy    | Hardy, | Shashi Narayan, |     | and             | Andreas |
| Association |      | for Computational |       |       | Linguistics. |     |          |        |                 |     |                 |         |
|             |      |                   |       |       |              |     | Vlachos. | 2019.  | HighRES:        |     | Highlight-based |         |
DOI: https://doi.org/10.18653/v1
/2020.acl-main.124 reference-less evaluation of summarization.
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
|     |     |     |     |     |     |     | In Proceedings |     | of the | 57th | Annual | Meet- |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | ---- | ------ | ----- |
Sebastian Gehrmann, Yuntian Deng, and ing of the Association for Computational
Alexander Rush. 2018. Bottom-up abstractive Linguistics, pages 3381–3392, Florence,
summarization. In Proceedings of the 2018 Italy. Association for Computational Linguis-
Conference on Empirical Methods in Natu- tics. DOI: https://doi.org/10.18653
| ral Language |          | Processing, |             | pages | 4098–4109,   |     | /v1/P19-1330 |     |     |     |     |     |
| ------------ | -------- | ----------- | ----------- | ----- | ------------ | --- | ------------ | --- | --- | --- | --- | --- |
| Brussels,    | Belgium. |             | Association |       | for Computa- |     |              |     |     |     |     |     |
tionalLinguistics.DOI:https://doi.org Karl Moritz Hermann, Tomas Kocisky, Edward
|     |     |     |     |     |     |     | Grefenstette, |     | Lasse | Espeholt, | Will | Kay, |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----- | --------- | ---- | ---- |
/10.18653/v1/D18-1443
|     |     |     |     |     |     |     | Mustafa | Suleyman, | and | Phil | Blunsom. | 2015. |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | ---- | -------- | ----- |
Dan Gillick and Yang Liu. 2010. Non- Teaching machines to read and comprehend.
expert evaluation of summarization systems In Advancesin NeuralInformation Processing
is risky. In Proceedings of the NAACL HLT Systems,pages1693–1701.
| 2010 Workshop |      | on   | Creating |     | Speech     | and |          |      |           |     |                |     |
| ------------- | ---- | ---- | -------- | --- | ---------- | --- | -------- | ---- | --------- | --- | -------------- | --- |
|               |      |      |          |     |            |     | Wan-Ting | Hsu, | Chieh-Kai |     | Lin, Ming-Ying |     |
| Language      | Data | with | Amazon’s |     | Mechanical |     |          |      |           |     |                |     |
Turk,pages148–151,LosAngeles.Association Lee, Kerui Min, Jing Tang, and Min Sun.
forComputationalLinguistics. 2018. A unified model for extractive and
|     |     |     |     |     |     |     | abstractive | summarization |     | using | inconsistency |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | --- | ----- | ------------- | --- |
Yvette Graham. 2015. Re-evaluating automatic loss. In Proceedings of the 56th Annual
summarization with BLEU and 192 shades Meeting of the Association for Computa-
of ROUGE. In Proceedings of the 2015 Con- tional Linguistics (Volume 1: Long Papers),
ference on Empirical Methods in Natural pages 132–141, Melbourne, Australia. Associ-
LanguageProcessing,pages128–137,Lisbon, ationforComputationalLinguistics.
| Portugal. | Association |     | for | Computational |     | Lin- |     |     |     |     |     |     |
| --------- | ----------- | --- | --- | ------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
guistics. DOI: https://doi.org/10 Yichen Jiang and Mohit Bansal. 2018.
|     |     |     |     |     |     |     | Closed-book |     | training | to improve |     | summa- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------- | ---------- | --- | ------ |
.18653/v1/D15-1013,PMID:24802104
|     |     |     |     |     |     |     | rization | encoder | memory. |     | In Proceedings |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ------- | --- | -------------- | --- |
Max Grusky, Mor Naaman, and Yoav Artzi. of the 2018 Conference on Empirical
2018. Newsroom: A dataset of 1.3 million Methods in Natural Language Process-
summaries with diverse extractive strategies. ing, pages 4067–4077, Brussels, Belgium.
In Proceedings of the 2018 Conference of the Association for Computational Linguistics.
NorthAmericanChapteroftheAssociationfor DOI: https://doi.org/10.18653/v1
| Computational |          | Linguistics: |     | Human    | Language   |          | /D18-1440     |     |          |          |     |         |
| ------------- | -------- | ------------ | --- | -------- | ---------- | -------- | ------------- | --- | -------- | -------- | --- | ------- |
| Technologies, |          | Volume       |     | 1 (Long  |            | Papers), |               |     |          |          |     |         |
|               |          |              |     |          |            |          | Chris Kedzie, |     | Kathleen | McKeown, |     | and Hal |
| pages         | 708–719, | New          |     | Orleans, | Louisiana. |          |               |     |          |          |     |         |
Association for Computational Linguistics. Daume´ III. 2018. Content selection in deep
Pro-
DOI: https://doi.org/10.18653/v1 learning models of summarization. In
|     |     |     |     |     |     |     | ceedings | of the | 2018 Conference |     | on  | Empirical |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | --------------- | --- | --- | --------- |
/N18-1065
|     |     |     |     |     |     |     | Methods | in  | Natural | Language | Processing, |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | -------- | ----------- | --- |
Han Guo, Ramakanth Pasunuru, and Mohit pages 1818–1828, Brussels, Belgium. Asso-
Bansal. 2018. Soft layer-specific multi-task ciation for Computational Linguistics. DOI:
summarization with entailment and ques- https://doi.org/10.18653/v1/D18
| tion generation. |     | In  | Proceedings |     | of  | the 56th | -1208 |     |     |     |     |     |
| ---------------- | --- | --- | ----------- | --- | --- | -------- | ----- | --- | --- | --- | --- | --- |
404

Klaus Krippendorff. 2011. Computing krip- 2019.BART:Denoisingsequence-to-sequence
pendorff’s alpha-reliability. Retrieved from pre-training for natural language generation,
https://repository.upenn.edu/asc translation,andcomprehension.arXivpreprint
| papers/43. |     |     |     |     |     | arXiv:1910.13461. |     |     | DOI: https://doi.org |     |     |     |
| ---------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | -------------------- | --- | --- | --- |
/10.18653/v1/2020.acl-main.703
Krys´cin´ski,
| Wojciech |     | Nitish | Shirish |     | Keskar, |     |     |     |     |     |     |     |
| -------- | --- | ------ | ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Bryan McCann, Caiming Xiong, and Richard Chin-Yew Lin. 2004a. Looking for a few good
Socher. 2019. Neural text summarization: A metrics: Automatic summarization evaluation-
critical evaluation. In Proceedings of the 2019 howmanysamplesareenough?InNTCIR.
| Conference | on  | Empirical | Methods |     | in Nat- |          |      |        |        |     |             |                                                                                                                                     |
| ---------- | --- | --------- | ------- | --- | ------- | -------- | ---- | ------ | ------ | --- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
|            |     |           |         |     |         | Chin-Yew | Lin. | 2004b. | ROUGE: | A   | package for | Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026 |
uralLanguageProcessingandthe9thInterna-
|              |            |     |            |     |          | automatic |     | evaluation | of summaries. |     | In Text |     |
| ------------ | ---------- | --- | ---------- | --- | -------- | --------- | --- | ---------- | ------------- | --- | ------- | --- |
| tional Joint | Conference |     | on Natural |     | Language |           |     |            |               |     |         |     |
Processing(EMNLP-IJCNLP),pages540–551, Summarization Branches Out, pages 74–81,
Hong Kong, China. Association for Computa- Barcelona, Spain. Association for Computa-
tionalLinguistics.
tionalLinguistics.DOI:https://doi.org
/10.18653/v1/2020.emnlp-main.750
|     |     |     |     |     |     | Feifan | Liu | and Yang | Liu. | 2008. | Correla- |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | -------- | ---- | ----- | -------- | --- |
Wojciech Krys´cin´ski, Bryan McCann, Caiming tion between ROUGE and human evaluation
|            |         |         |       |            |     | of extractive |     | meeting | summaries. |     | In Pro- |     |
| ---------- | ------- | ------- | ----- | ---------- | --- | ------------- | --- | ------- | ---------- | --- | ------- | --- |
| Xiong, and | Richard | Socher. | 2020. | Evaluating |     |               |     |         |            |     |         |     |
the factual consistency of abstractive text ceedings of ACL-08: HLT, Short Papers,
summarization. In Proceedings of the pages 201–204, Columbus, Ohio. Association
forComputationalLinguistics.
| 2020 Conference  |          | on           | Empirical  | Methods     | in  |                |     |             |                 |      |            |     |
| ---------------- | -------- | ------------ | ---------- | ----------- | --- | -------------- | --- | ----------- | --------------- | ---- | ---------- | --- |
| Natural          | Language |              | Processing | (EMNLP),    |     |                |     |             |                 |      |            |     |
|                  |          |              |            |             |     | Yang           | Liu | and Mirella | Lapata.         |      | 2019. Text |     |
| pages 9332–9346, |          | Online.      |            | Association | for |                |     |             |                 |      |            |     |
|                  |          |              |            |             |     | summarization  |     |             | with pretrained |      | encoders.  |     |
| Computational    |          | Linguistics. | DOI:       | https://    |     |                |     |             |                 |      |            |     |
|                  |          |              |            |             |     | In Proceedings |     |             | of the          | 2019 | Conference |     |
doi.org/10.18653/v1/D18-1207
|     |     |     |     |     |     | on  | Empirical | Methods |     | in Natural | Lang- |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------- | --- | ---------- | ----- | --- |
Wojciech Krys´cin´ski, Romain Paulus, Caiming uage Processing and the 9th International
|                 |             |         |                |       |         | Joint   | Conference      |     | on Natural | Language | Pro-       |     |
| --------------- | ----------- | ------- | -------------- | ----- | ------- | ------- | --------------- | --- | ---------- | -------- | ---------- | --- |
| Xiong,          | and Richard | Socher. |                | 2018. | Improv- |         |                 |     |            |          |            |     |
|                 |             |         |                |       |         | cessing | (EMNLP-IJCNLP), |     |            | pages    | 3730–3740, |     |
| ing abstraction |             | in text | summarization. |       | In Pro- |         |                 |     |            |          |            |     |
ceedings of the 2018 Conference on Empirical Hong Kong, China. Association for Computa-
Methods in Natural Language Processing, tionalLinguistics.DOI:https://doi.org
/10.18653/v1/D19-1387
| pages 1808–1817, |     | Brussels, |     | Belgium. | Asso- |     |     |     |     |     |     |     |
| ---------------- | --- | --------- | --- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
ciationforComputationalLinguistics.
|     |     |     |     |     |     | Annie | Louis | and | Ani Nenkova. |     | 2013. Auto- |     |
| --- | --- | --- | --- | --- | --- | ----- | ----- | --- | ------------ | --- | ----------- | --- |
Matt Kusner, Yu Sun, Nicholas Kolkin, matically assessing machine summary content
|            |             |     |       |      |      | without | a   | gold standard. |     | Computational | Lin- |     |
| ---------- | ----------- | --- | ----- | ---- | ---- | ------- | --- | -------------- | --- | ------------- | ---- | --- |
| and Kilian | Weinberger. |     | 2015. | From | word |         |     |                |     |               |      |     |
embeddings to document distances. In Inter- guistics,39(2):267–300.DOI:https://doi
national Conference on Machine Learning, .org/10.1162/COLI a 00123
pages957–966.
|     |     |     |     |     |     | Joshua | Maynez, | Shashi | Narayan, | Bernd | Bohnet, |     |
| --- | --- | --- | --- | --- | --- | ------ | ------- | ------ | -------- | ----- | ------- | --- |
Alon Lavie and Abhaya Agarwal. 2007. and Ryan T. McDonald. 2020. On faithfulness
METEOR: An automatic metric for MT and factuality in abstractive summariza-
|            |      |             |     |             |      | tion. | In  | Proceedings | of  | the | 58th Annual |     |
| ---------- | ---- | ----------- | --- | ----------- | ---- | ----- | --- | ----------- | --- | --- | ----------- | --- |
| evaluation | with | high levels | of  | correlation | with |       |     |             |     |     |             |     |
humanjudgments.InProceedingsoftheSecond Meeting of the Association for Compu-
Workshop on Statistical Machine Translation, tational Linguistics, ACL 2020, Online,
pages228–231,Prague,CzechRepublic.Asso- July 5-10, 2020, pages 1906–1919. Associ-
ciation for Computational Linguistics. DOI: ation for Computational Linguistics. DOI:
https://doi.org/10.3115/1626355 https://doi.org/10.18653/v1/2020
.1626389 .acl-main.173
Mike Lewis, Yinhan Liu, Naman Goyal, Marjan Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg
Ghazvininejad,AbdelrahmanMohamed,Omer S. Corrado, and Jeff Dean. 2013. Distributed
Levy,VeselinStoyanov,andLukeZettlemoyer. representations of words and phrases and
405

their compositionality. In C. J. C. Burges, Ramakanth Pasunuru and Mohit Bansal. 2018.
L. Bottou, M. Welling, Z. Ghahramani, Multi-reward reinforced summarization with
and K. Q. Weinberger, editors, Advances in saliency and entailment. In Proceedings of
Neural Information Processing Systems 26, the 2018 Conference of the North American
pages3111–3119.CurranAssociates,Inc. Chapter of the Association for Computational
|     |     |     |     |     |     |     | Linguistics: |     | Human | Language |     | Technologies, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----- | -------- | --- | ------------- | --- |
RameshNallapati,BowenZhou,CaglarGulcehre, Volume 2 (Short Papers), pages 646–653,
Bing Xiang et al. 2016. Abstractive text New Orleans, Louisiana. Association for
summarization using sequence-to-sequence Computational Linguistics. DOI: https://
rnns and beyond. arXiv preprint arXiv: doi.org/10.18653/v1/N18-2102
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
| 1602.06023. |     | DOI: | https://doi.org/10 |     |     |     |                |     |         |     |        |             |     |
| ----------- | --- | ---- | ------------------ | --- | --- | --- | -------------- | --- | ------- | --- | ------ | ----------- | --- |
|             |     |      |                    |     |     |     | Romain Paulus, |     | Caiming |     | Xiong, | and Richard |     |
.18653/v1/K16-1028
|     |     |     |     |     |     |     | Socher. | 2017. | A   | deep | reinforced |     | model |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----- | --- | ---- | ---------- | --- | ----- |
Shashi Narayan, Shay B. Cohen, and Mirella for abstractive summarization. arXiv preprint
arXiv:1705.04304.
Lapata.2018.Rankingsentencesforextractive
| summarization |     | with   | reinforcementlearning. |            |     | In     |                 |         |       |          |             |               |         |
| ------------- | --- | ------ | ---------------------- | ---------- | --- | ------ | --------------- | ------- | ----- | -------- | ----------- | ------------- | ------- |
|               |     |        |                        |            |     |        | Maxime Peyrard. |         | 2019. | Studying |             | summarization |         |
| Proceedings   |     | of the | 2018                   | Conference |     | of the |                 |         |       |          |             |               |         |
|               |     |        |                        |            |     |        | evaluation      | metrics |       | in the   | appropriate |               | scoring |
NorthAmericanChapteroftheAssociationfor
|                                  |            |                   |     |          |              |          | range.              | In Proceedings           |     |                          | of the | 57th         | Annual |
| -------------------------------- | ---------- | ----------------- | --- | -------- | ------------ | -------- | ------------------- | ------------------------ | --- | ------------------------ | ------ | ------------ | ------ |
| Computational                    |            | Linguistics:      |     | Human    | Language     |          |                     |                          |     |                          |        |              |        |
|                                  |            |                   |     |          |              |          | Meeting             | of                       | the | Association              |        | for Computa- |        |
| Technologies,                    |            | Volume            |     | 1 (Long  |              | Papers), |                     |                          |     |                          |        |              |        |
|                                  |            |                   |     |          |              |          | tional Linguistics, |                          |     | pages5093–5100,Florence, |        |              |        |
| pages                            | 1747–1759, |                   | New | Orleans, | Louisiana.   |          |                     |                          |     |                          |        |              |        |
|                                  |            |                   |     |          |              |          | Italy. Association  |                          |     | for Computational        |        | Linguis-     |        |
| Association                      |            | for Computational |     |          | Linguistics. |          |                     |                          |     |                          |        |              |        |
|                                  |            |                   |     |          |              |          | DOI:                | https://doi.org/10.18653 |     |                          |        |              |        |
| DOI: https://doi.org/10.18653/v1 |            |                   |     |          |              |          | tics.               |                          |     |                          |        |              |        |
/v1/P19-1502
/N18-1158
|            |               |            |            |          |             |       | Maxime    | Peyrard, | Teresa |          | Botschen, | and       | Iryna  |
| ---------- | ------------- | ---------- | ---------- | -------- | ----------- | ----- | --------- | -------- | ------ | -------- | --------- | --------- | ------ |
| Jun-Ping   | Ng            | and        | Viktoria   | Abrecht. |             | 2015. |           |          |        |          |           |           |        |
|            |               |            |            |          |             |       | Gurevych. | 2017.    |        | Learning | to        | score     | system |
| Better     | summarization |            | evaluation |          | with        | word  |           |          |        |          |           |           |        |
|            |               |            |            |          |             |       | summaries |          | for    | better   | content   | selection |        |
| embeddings |               | for ROUGE. |            | In       | Proceedings |       |           |          |        |          |           |           |        |
evaluation.InProceedingsoftheWorkshopon
| of the | 2015 | Conference |     |     | on Empirical |     |     |     |     |     |     |     |     |
| ------ | ---- | ---------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
NewFrontiersinSummarization,pages74–84,
| Methods          | in  | Natural | Language |           | Processing, |          |               |     |              |     |             |          |     |
| ---------------- | --- | ------- | -------- | --------- | ----------- | -------- | ------------- | --- | ------------ | --- | ----------- | -------- | --- |
|                  |     |         |          |           |             |          | Copenhagen,   |     | Denmark.     |     | Association |          | for |
| pages 1925–1930, |     |         | Lisbon,  | Portugal. |             | Associa- |               |     |              |     |             |          |     |
|                  |     |         |          |           |             |          | Computational |     | Linguistics. |     | DOI:        | https:// |     |
tionforComputationalLinguistics.
doi.org/10.18653/W17-4510
KarolinaOwczarzak,PeterA.Rankel,HoaTrang
|            |             |              |         |           |               |         | Maja Popovic´. |               | 2015.        | chrF:       | character   |              | n-gram |
| ---------- | ----------- | ------------ | ------- | --------- | ------------- | ------- | -------------- | ------------- | ------------ | ----------- | ----------- | ------------ | ------ |
| Dang, and  | John        | M.           | Conroy. | 2012.     | Assessing     |         |                |               |              |             |             |              |        |
|            |             |              |         |           |               |         | F-score        | for automatic |              | MT          | evaluation. | In           | Pro-   |
| the effect | of          | inconsistent |         | assessors |               | on sum- |                |               |              |             |             |              |        |
|            |             |              |         |           |               |         | ceedings       | of            | the Tenth    | Workshop    |             | on Statisti- |        |
| marization | evaluation. |              | In      | The       | 50th          | Annual  |                |               |              |             |             |              |        |
|            |             |              |         |           |               |         | cal Machine    |               | Translation, |             | pages       | 392–395,     |        |
| Meeting    | of the      | Association  |         | for       | Computational |         |                |               |              |             |             |              |        |
|            |             |              |         |           |               |         | Lisbon,        | Portugal.     |              | Association |             | for Computa- |        |
Linguistics, Proceedings of the Conference, tionalLinguistics.DOI:https://doi.org
July8–14,2012,JejuIsland,Korea-Volume2:
/10.18653/v1/W15-3049
ShortPapers,pages359–362.TheAssociation
forComputerLinguistics. Alec Radford, Jeffrey Wu, Rewon Child, David
Luan,DarioAmodei,andIlyaSutskever.2019.
| Kishore Papineni, |     | Salim | Roukos, |     | Todd | Ward, |          |        |     |                  |     |           |     |
| ----------------- | --- | ----- | ------- | --- | ---- | ----- | -------- | ------ | --- | ---------------- | --- | --------- | --- |
|                   |     |       |         |     |      |       | Language | models |     | are unsupervised |     | multitask |     |
and Wei-Jing Zhu. 2002. BLEU: A method learners.OpenAIBlog,1(8):9.
| for automatic |     | evaluation |     | of machine |     | trans- |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | --- | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
lation. In Proceedings of the 40th Annual Colin Raffel, Noam Shazeer, Adam Roberts,
Meeting of the Association for Computational Katherine Lee, Sharan Narang, Michael
Linguistics, pages 311–318, Philadelphia, Matena, YanqiZhou, WeiLi, and PeterJ. Liu.
Pennsylvania, USA. Association for Com- 2019. Exploring the limits of transfer learning
putational Linguistics. DOI: https:// with a unified text-to-text transformer. arXiv
| doi.org/10.3115/1073083.1073135 |     |     |     |     |     |     | e-prints. |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
406

Peter A. Rankel, John M. Conroy, Hoa Trang pages 3280–3291, Hong Kong, China.
Dang, and Ani Nenkova. 2013. A decade Association for Computational Linguistics.
of automatic content evaluation of news DOI: https://doi.org/10.18653/v1
summaries: Reassessing the state of the art. /D19-1323, PMID: 31698456, PMCID:
| In Proceedings  |     | of the            | 51st Annual | Meeting     | of  | PMC6855099 |     |     |     |     |     |
| --------------- | --- | ----------------- | ----------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- |
| the Association |     | for Computational |             | Linguistics |     |            |     |     |     |     |     |
(Volume 2: Short Papers), pages 131–136, NisanStiennon,LongOuyang,JeffWu,DanielM.
|     |     |     |     |     |     | Ziegler, | Ryan | Lowe, | Chelsea |     | Voss, Alec |
| --- | --- | --- | --- | --- | --- | -------- | ---- | ----- | ------- | --- | ---------- |
Sofia,Bulgaria.AssociationforComputational
|     |     |     |     |     |     | Radford, | Dario | Amodei, |     | and Paul | Christiano. |
| --- | --- | --- | --- | --- | --- | -------- | ----- | ------- | --- | -------- | ----------- |
Linguistics.
|     |     |     |     |     |     | 2020. | Learning | to  | summarize | from | human |
| --- | --- | --- | --- | --- | --- | ----- | -------- | --- | --------- | ---- | ----- |
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
| Evan Sandhaus. | 2008. |     | The New | York | Times |     |     |     |     |     |     |
| -------------- | ----- | --- | ------- | ---- | ----- | --- | --- | --- | --- | --- | --- |
feedback.CoRR,abs/2009.01325.
| annotatedcorpus.Linguistic |     |     |     | Data Consortium, |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Philadelphia,6(12):e26752. Ilya Sutskever, Oriol Vinyals, and Quoc V. Le.
|     |     |     |     |     |     | 2014. | Sequence | to  | sequence | learning | with |
| --- | --- | --- | --- | --- | --- | ----- | -------- | --- | -------- | -------- | ---- |
Thomas Scialom, Sylvain Lamprier, Benjamin neural networks. In Advances in Neural Infor-
| Piwowarski, | and | Jacopo |     | Staiano. | 2019. |     |     |     |     |     |     |
| ----------- | --- | ------ | --- | -------- | ----- | --- | --- | --- | --- | --- | --- |
mationprocessingSystems,pages3104–3112.
| Answers | unite! | unsupervised |     | metrics | for rein- |     |     |     |     |     |     |
| ------- | ------ | ------------ | --- | ------- | --------- | --- | --- | --- | --- | --- | --- |
forced summarization models. In Proceed- Oleg V. Vasilyev, Vedant Dharnidharka, and
ings of the 2019 Conference on Empirical John Bohannon. 2020. Fill in the BLANC:
Methods in Natural Language Processing human-free quality estimation of document
and the 9th International Joint Conference summaries. CoRR, abs/2002.09836. DOI:
https://doi.org/10.18653/v1/2020
| on Natural | Language |            | Processing |      | (EMNLP- |               |     |     |     |     |     |
| ---------- | -------- | ---------- | ---------- | ---- | ------- | ------------- | --- | --- | --- | --- | --- |
| IJCNLP),   | pages    | 3246–3256, |            | Hong | Kong,   | .eval4nlp-1.2 |     |     |     |     |     |
China.AssociationforComputationalLinguis-
|              |                          |     |     |     |     | Ashish Vaswani,                         |         | Noam | Shazeer, | Niki        | Parmar, |
| ------------ | ------------------------ | --- | --- | --- | --- | --------------------------------------- | ------- | ---- | -------- | ----------- | ------- |
| tics. DOI:   | https://doi.org/10.18653 |     |     |     |     |                                         |         |      |          |             |         |
| /v1/D19-1320 |                          |     |     |     |     | JakobUszkoreit,LlionJones,AidanN.Gomez, |         |      |          |             |         |
|              |                          |     |     |     |     | Łukasz                                  | Kaiser, | and  | Illia    | Polosukhin. | 2017.   |
Abigail See, Peter J. Liu, and Christopher D. Attention is all you need. In Advances
Manning. 2017. Get to the point: Summariza- in Neural Information Processing Systems,
| tion with | pointer-generator |      | networks. |         | In Pro- | pages5998–6008. |     |     |     |     |     |
| --------- | ----------------- | ---- | --------- | ------- | ------- | --------------- | --- | --- | --- | --- | --- |
| ceedings  | of the            | 55th | Annual    | Meeting | of      |                 |     |     |     |     |     |
the Association for Computational Linguistics RamakrishnaVedantam,C.LawrenceZitnick,and
|         |         |          |       |            |     | Devi Parikh. |     | 2015. | CIDEr: | Consensus-based |     |
| ------- | ------- | -------- | ----- | ---------- | --- | ------------ | --- | ----- | ------ | --------------- | --- |
| (Volume | 1: Long | Papers), | pages | 1073–1083, |     |              |     |       |        |                 |     |
imagedescriptionevaluation.InProceedingsof
| Vancouver,Canada.Association |     |     |     | forComputa- |     |     |     |     |     |     |     |
| ---------------------------- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
tionalLinguistics. the IEEE Conference on Computer Vision and
|     |     |     |     |     |     | Pattern | Recognition, |     | pages | 4566–4575. | DOI: |
| --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | ----- | ---------- | ---- |
Elaheh ShafieiBavani, Mohammad Ebrahimi, https://doi.org/10.1109/CVPR.2015
| Raymond           | Wong, | and     | Fang | Chen.      | 2018. | .7299087 |     |     |     |     |     |
| ----------------- | ----- | ------- | ---- | ---------- | ----- | -------- | --- | --- | --- | --- | --- |
| A graph-theoretic |       | summary |      | evaluation | for   |          |     |     |     |     |     |
ROUGE. In Proceedings of the 2018 Con- Oriol Vinyals, Meire Fortunato, and Navdeep
ferenceon Empirical Methods in Natural Lan- Jaitly. 2015. Pointer networks. In Advances
|              |             |                    |          |               |           | in Neural       | Information |     |      | Processing | Systems,    |
| ------------ | ----------- | ------------------ | -------- | ------------- | --------- | --------------- | ----------- | --- | ---- | ---------- | ----------- |
| guage        | Processing, | pages              | 762–767, |               | Brussels, |                 |             |     |      |            |             |
| Belgium.     | Association |                    | for      | Computational |           | pages2692–2700. |             |     |      |            |             |
| Linguistics. | DOI:        | https://doi.org/10 |          |               |           |                 |             |     |      |            |             |
|              |             |                    |          |               |           | Alex Wang,      | Kyunghyun   |     | Cho, | and        | Mike Lewis. |
.18653/v1/D18-1085
|     |     |     |     |     |     | 2020. | Asking | and | answering | questions | to  |
| --- | --- | --- | --- | --- | --- | ----- | ------ | --- | --------- | --------- | --- |
Eva Sharma, Luyang Huang, Zhe Hu, and evaluate the factual consistency of summaries.
Lu Wang. 2019. An entity-driven framework In Proceedings of the 58th Annual Meet-
for abstractive summarization. In Proceedings ing of the Association for Computational
of the 2019 Conference on Empirical Methods Linguistics, pages 5008–5020, Online. Asso-
in Natural Language Processing and the ciation for Computational Linguistics. DOI:
9th International Joint Conference on Natural https://doi.org/10.18653/v1/2020
Language Processing (EMNLP-IJCNLP), .acl-main.450,PMCID:PMC7367613
407

Ronald J. Williams. 1992. Simple statistical guistics, pages 5059–5069, Florence, Italy.
gradient-followingalgorithmsforconnectionist Association for Computational Linguistics.
reinforcement learning. Machine Learning, DOI: https://doi.org/10.18653/v1
8(3-4):229–256. DOI: https://doi.org /P19-1499, PMID: 31638247, PMCID:
| /10.1007/BF00992696 |     |             |     |         |       |          | PMC6854546 |           |        |          |     |         |      |
| ------------------- | --- | ----------- | --- | ------- | ----- | -------- | ---------- | --------- | ------ | -------- | --- | ------- | ---- |
| Yuxiang             | Wu  | and Baotian |     | Hu.     | 2018. | Learning |            |           |        |          |     |         |      |
|                     |     |             |     |         |       |          | Wei Zhao,  |           | Maxime | Peyrard, | Fei | Liu,    | Yang |
| to extract          |     | coherent    |     | summary |       | via deep |            |           |        |          |     |         |      |
|                     |     |             |     |         |       |          | Gao,       | Christian | M.     | Meyer,   | and | Steffen |      |
reinforcementlearning.InThirty-SecondAAAI
|     |     |     |     |     |     |     | Eger. | 2019. | MoverScore: |     | Text | generation |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ----------- | --- | ---- | ---------- | --- |
ConferenceonArtificialIntelligence.
|     |     |     |     |     |     |     | evaluating |     | with contextualized |     |     | embeddings |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------------- | --- | --- | ---------- | --- |
Downloaded from http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf by guest on 03 August 2026
|          |            |     |      |               |     |       | and    | earth | mover | distance. | In  | EMNLP- |       |
| -------- | ---------- | --- | ---- | ------------- | --- | ----- | ------ | ----- | ----- | --------- | --- | ------ | ----- |
| Jiacheng | Xu         | and | Greg | Durrett.      |     | 2019. |        |       |       |           |     |        |       |
|          |            |     |      |               |     |       | IJCNLP | 2019, | pages | 563–578,  |     | Hong   | Kong, |
| Neural   | extractive |     | text | summarization |     | with  |        |       |       |           |     |        |       |
China.AssociationforComputationalLinguis-
EMNLP-IJCNLP
| syntactic | compression. |            |     | In   |       |        |       |      |                          |     |     |     |     |
| --------- | ------------ | ---------- | --- | ---- | ----- | ------ | ----- | ---- | ------------------------ | --- | --- | --- | --- |
|           |              |            |     |      |       |        | tics. | DOI: | https://doi.org/10.18653 |     |     |     |     |
| 2019,     | pages        | 3292–3303, |     | Hong | Kong, | China. |       |      |                          |     |     |     |     |
/v1/D19-1053
AssociationforComputationalLinguistics.
|          |        |        |     |      |     |          | Liang | Zhou, | Chin-Yew | Lin, | Dragos |     | Stefan |
| -------- | ------ | ------ | --- | ---- | --- | -------- | ----- | ----- | -------- | ---- | ------ | --- | ------ |
| Fangfang | Zhang, | Jin-ge |     | Yao, | and | Rui Yan. |       |       |          |      |        |     |        |
2018a. On the abstractiveness of neural Munteanu, and Eduard Hovy. 2006. ParaEval:
documentsummarization.InProceedingsofthe Using paraphrases to evaluate summaries
|      |            |     |     |           |         |     |                |     | Proceedings |     | of  | the Human |     |
| ---- | ---------- | --- | --- | --------- | ------- | --- | -------------- | --- | ----------- | --- | --- | --------- | --- |
| 2018 | Conference |     | on  | Empirical | Methods | in  | automatically. |     | In          |     |     |           |     |
NaturalLanguageProcessing,pages785–790, Language Technology Conference of the
Brussels, Belgium. Association for Compu- NAACL, Main Conference, pages 447–454,
tational Linguistics. DOI: https://doi New York City, USA. Association for
.org/10.18653/v1/D18-1089 Computational Linguistics. DOI: https://
doi.org/10.3115/1220835.1220892
| Jingqing  | Zhang, | Yao  | Zhao,  | Mohammad |              | Saleh, |        |       |           |      |      |         |     |
| --------- | ------ | ---- | ------ | -------- | ------------ | ------ | ------ | ----- | --------- | ---- | ---- | ------- | --- |
| and Peter | J.     | Liu. | 2019a. | Pegasus: | Pre-training |        |        |       |           |      |      |         |     |
|           |        |      |        |          |              |        | Qingyu | Zhou, | Nan Yang, | Furu | Wei, | Shaohan |     |
with extracted gap-sentences for abstractive Huang, Ming Zhou, and Tiejun Zhao. 2018.
| summarization. |     | arXiv |     | preprint | arXiv:1912. |     |        |          |               |     |     |     |         |
| -------------- | --- | ----- | --- | -------- | ----------- | --- | ------ | -------- | ------------- | --- | --- | --- | ------- |
|                |     |       |     |          |             |     | Neural | document | summarization |     |     | by  | jointly |
08777.
|            |                |            |     |                 |        |       | learning | to          | score                    | and select    | sentences. |          | In   |
| ---------- | -------------- | ---------- | --- | --------------- | ------ | ----- | -------- | ----------- | ------------------------ | ------------- | ---------- | -------- | ---- |
|            |                |            |     |                 |        |       | ACL      | 2018,       | pages 654–663,           |               | Melbourne, |          | Aus- |
| Tianyi     | Zhang,         | Varsha     |     | Kishore,        | Felix  | Wu,   |          |             |                          |               |            |          |      |
|            |                |            |     |                 |        |       | tralia.  | Association | for                      | Computational |            | Linguis- |      |
| Kilian     | Q. Weinberger, |            |     | and Yoav        | Artzi. | 2020. |          |             |                          |               |            |          |      |
|            |                |            |     |                 |        |       | tics.    | DOI:        | https://doi.org/10.18653 |               |            |          |      |
| Bertscore: |                | Evaluating |     | text generation |        | with  |          |             |                          |               |            |          |      |
/v1/P18-1061
| BERT. | In International |     |     | Conference |     | on Learn- |     |     |     |     |     |     |     |
| ----- | ---------------- | --- | --- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
ingRepresentations.
|     |     |     |     |     |     |     | Daniel | M. Ziegler, | Nisan | Stiennon, |     | Jeffrey | Wu, |
| --- | --- | --- | --- | --- | --- | --- | ------ | ----------- | ----- | --------- | --- | ------- | --- |
Xingxing Zhang, Mirella Lapata, Furu Wei, and Tom B. Brown, Alec Radford, Dario Amodei,
Ming Zhou. 2018b. Neural latent extractive Paul Christiano, and Geoffrey Irving. 2019.
| document |     | summarization. |     | In  | Proceedings |     |             |     |          |        |      |       |     |
| -------- | --- | -------------- | --- | --- | ----------- | --- | ----------- | --- | -------- | ------ | ---- | ----- | --- |
|          |     |                |     |     |             |     | Fine-tuning |     | language | models | from | human |     |
of the 2018 Conference on Empirical preferences.arXivpreprintarXiv:1909.08593.
| Methods                         | in       | Natural       |           | Language     | Processing, |         |            |     |     |     |     |     |     |
| ------------------------------- | -------- | ------------- | --------- | ------------ | ----------- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
| pages                           | 779–784, |               | Brussels, | Belgium.     |             | Associ- |            |     |     |     |     |     |     |
| ation                           | for      | Computational |           | Linguistics. |             | DOI:    |            |     |     |     |     |     |     |
| https://doi.org/10.18653/v1/D18 |          |               |           |              |             |         | 9 Appendix |     |     |     |     |     |     |
-1088
Data Collection
|     |     |     |     |     |     |     |     |     | The | data | collection | interface |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---------- | --------- | --- |
Xingxing Zhang, Furu Wei, and Ming usedby both crowd-sourceand expertannotators
Zhou. 2019b. HIBERT: Document level ispresentedinFigure3.Intheannotationprocess,
pre-training of hierarchical bidirectional judges were first asked to carefully read the con-
transformers for document summarization. In tentofthesourcearticleandnextproceedtoeval-
Proceedings of the 57th Annual Meeting uating the associated summaries along four axes:
of the Association for Computational Lin- relevance,consistency,fluency,andcoherence.
408

Figure3:Exampleofthedatacollectioninterfaceusedbycrowd-sourceandexpertannotators.
409
Downloaded
from
http://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl_a_00373/1923949/tacl_a_00373.pdf
by
guest
on
03
August
2026