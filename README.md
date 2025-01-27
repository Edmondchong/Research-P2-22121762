# Research-P2-22121762
This Github repository is for 22121762 Research Project P2


All files are renamed accordingly:
-> o = overlapping, no = non-overlapping, c = combined, LT = long-tail.

-> LLM-o-train = training set for LLM (text-based), where o stands for overlapping_set.

-> ML-c-test = testing set for ML (one-hot encoded), where c stands for combined_set.

-> Files are saved this way to clearly differentiate them and avoid confusion.




Notes:
Since fine-tuning ClinicalT5 is super time-consuming and performs worse than other LLMs especially standalone ClinicalT5, PubMedBERT is added as the extra LLM to match the three ML models and three LLMs (3ML vs 3LLM). However, the best performance is still achieved by BioClinicalBERT most of the time, followed by BioBERT in some cases.

->PubMedBERT outperforms ClinicalT5 in both performance and time-efficiency.

->PubMedBERT aligns better with BioBERT and BioClinicalBERT, allowing for a more direct comparison in disease classification.

->However, ClinicalT5 is still retained in the folders.

