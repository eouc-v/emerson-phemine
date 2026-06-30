"""
Trains a model with pheML_develop's train_model() function
Uses data saved by the main pipeline 
Mostly just for testing custom models in the pheML code
(Without re-running the entire pipeline each time testing is needed)
"""

from pheML_develop import train_model
from pathlib import Path
import sys,argparse

def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--train_folder',default='results/enrichment_test_0310') #where X_train & y_train are stored. normally the standard test output
    parser.add_argument('--model_type',default='LR') #type of model (RF, CART, etc.). defaults to linear regression
    #parser.add_argument('--','')
    
    args = parser.parse_args()
    
    return_args()
    
def main():
    #get args from command line
    args = process_args()
    train_path = args.train_folder
    model_type = args.model_type

    X = pd.read_csv(train_path / "X_train.csv")
    y = pd.read_csv(train_path / "y_train.csv")
    print(X)
    print(y)
    #final_model = train_model()