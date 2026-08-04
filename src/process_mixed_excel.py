"""
This program is designed to parse an excel file containing GRIDs (labeled Patient ID) and diagnoses (labeled diagnosis) for any number of patients
It also takes a file containing excluded controls and a file containing cases that have certain lab readings that automatically classify them as a case
It processes them into two files: 

    A list of all cases, or patients in the file with 'yes' in the diagnosis column represented by their GRIDs
    Also included are patients who have passes the ttg-iga cutoff point
    This is used to separate cases and controls in find_matched_controls.py
    
    A list of patients who cannot become controls for various reasons
    This will be passed to find_matched_controls.py as well and used to exclude all controls listed in it
    Unknown patients are excluded because the model is a binary classifier and cannot handle multiclass problems
    PMH patients have previously been diagnosed, but the reasoning behind this diagnosis is unclear/suspect, so a clear classification is impossible
"""
import pandas as pd
import argparse
from pathlib import Path

def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--diagnosis-path')
    #parser.add_argument('--cutoff-path')
    parser.add_argument('--control-exclusion-path')
    parser.add_argument('--output-path',default='./')
    parser.add_argument('--case-output',default='celiac_cases_manual_review.txt')
    parser.add_argument('--exclusion-output',default='celiac_control_exclusion_grids.txt')
    
    args = parser.parse_args()
    
    return args

def main():
    args = process_args()
    #extract output paths and make them complete w/ pathlib
    output_path = Path(args.output_path)
    case_path = output_path / args.case_output
    exclusion_path = output_path / args.exclusion_output
    #load diagnosis/grid table and rename columns for consistency/readability
    diagnosis_df = pd.read_excel(args.diagnosis_path)
    diagnosis_df = diagnosis_df.rename( columns={'Patient ID':'grid','Diagnosis':'diagnosis'} )
    #extract all the patients where the diagnosis is 'Yes', or any case variation of it
    cases_df = diagnosis_df[ ( diagnosis_df['diagnosis'] == 'Yes' ) ]
    #remove all columns other than the one containing patient GRIDs
    cases_df = cases_df['grid'].str.strip()
    #load control exclusion and fuzzy cases (deprecated)
    ###cutoff_df = pd.read_csv(args.cutoff_path)
    primary_exclusion_df = pd.read_csv(args.control_exclusion_path,header=None)
    #add label to primary exclusion since it doesn't come with one
    primary_exclusion_df =  primary_exclusion_df.rename(columns={0:'grid'},errors='raise')
    #get all grids where the diagnosis is not Yes or No, making an exclusion df of any non-binary (:D) results
    exclusion_df = diagnosis_df[ ~diagnosis_df['diagnosis'].isin(['Yes','No']) ]
    #cut all columns other than grid (and strip spaces) from the exclusion df so it can then be combined with the prior exclusion list
    exclusion_df = exclusion_df['grid']
    exclusion_df = pd.concat([exclusion_df,primary_exclusion_df])
    exclusion_df["grid"] = exclusion_df["grid"].str.strip()
    print("exclusion dataframe:")
    print(exclusion_df)
    print("cases dataframe:")
    print(cases_df)
    #export results to csv
    #cases_df.to_csv(case_path,index=False)
    #exclusion_df.to_csv(exclusion_path,index=False)
    
if __name__ == '__main__':
	main()    
    
   
    

