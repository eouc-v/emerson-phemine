"""
This program is designed to parse an excel file containing GRIDs (labeled Patient ID) and diagnoses (labeled diagnosis) for any number of patients
It processes it into two files: 

    A list of all cases, or patients in the file with 'yes' in the diagnosis column represented by their GRIDs
    This is used to separate cases and controls in find_matched_controls.py
    
    A list of both cases and controls, removing any patients with a diagnosis of 'unknown','PMH', or any other unexpected input
    This will be passes to find_matched_controls.py as well and used to remove all patients not listed in this sheet
    Unknown patients are excluded because the model is a binary classifier and cannot handle multiclass problems
    PMH patients have previously been diagnosed, but the reasoning behind this diagnosis is unclear/suspect, so a clear classification is impossible
"""
import pandas as pd
import argparse
from pathlib import Path

def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--diagnosis-path')
    parser.add_argument('--output-path',default='./')
    parser.add_argument('--case-output',default='celiac_cases_manual_review.txt')
    parser.add_argument('--all-output',default='subset_inclusion_grids.txt')
    
    args = parser.parse_args()
    
    return args

def main():
    args = process_args()
    #extract output paths and make them complete w/ pathlib
    output_path = Path(args.output_path)
    case_path = output_path / args.case_output
    subset_path = output_path / args.all_output
    #load diagnosis/grid table and rename columns for consistency/readability
    diagnosis_df = pd.read_excel(args.diagnosis_path)
    diagnosis_df = diagnosis_df.rename( columns={'Patient ID':'grid','Diagnosis':'diagnosis'} )
    print(diagnosis_df)
    #extract all the patients where the diagnosis is 'Yes', or any case variation of it
    cases_df = diagnosis_df[ ( diagnosis_df['diagnosis'] == 'Yes' ) ]
    print(cases_df)
    #remove all columns other than the one containing patient GRIDs
    cases_df = cases_df['grid']
    print(cases_df)
    #get all grids where the diagnosis is either a Yes or No, ignoring any non-binary (:D) results
    subset_df = diagnosis_df[ diagnosis_df['diagnosis'].isin(['Yes','No']) ]
    print(subset_df)
    subset_df = subset_df['grid']
    print(subset_df)
    #EXPORT STATEMENT GOES HERE
    
if __name__ == '__main__':
	main()    
    
