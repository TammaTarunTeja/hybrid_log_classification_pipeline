from process_with_regex import regex_classifier
from process_with_llm import llm_classifier
from process_with_bert import bert_classifier 
import csv
import pandas as pd
def hybrid_classify_log_message(log_message,source):
    label = regex_classifier(log_message)
    if label == 'Unknown':
        label = bert_classifier(log_message)
        if label == 'Unknown':
            if source == 'legacy':
                label = llm_classifier(log_message, is_legacy=True)
                return label
            else:
                label = llm_classifier(log_message, is_legacy=False)
                return label
        return label
    return label

def create_classified_csv(csv_file, output_csv):
    df = pd.read_csv(csv_file)
    df['Predicted Label'] = df.apply(lambda row: hybrid_classify_log_message(row['log_message'], row['source']), axis=1)
    df.to_csv(output_csv, index=False)


