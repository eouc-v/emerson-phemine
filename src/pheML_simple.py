"""
Trains a model with pheML_develop's train_model() function
Uses data saved by the main pipeline 
Mostly just for testing custom models in the pheML code
(Without re-running the entire pipeline each time testing is needed)
"""

from pheML_develop import train_model
from plotting import plot_CM

from pathlib import Path
import sys,argparse

import pandas as pd

def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--train_folder',default='results/enrichment_test_0310') #where X_train & y_train are stored. normally the standard test output
    parser.add_argument('--model_type',default='LR') #type of model (RF, CART, etc.). defaults to linear regression
    parser.add_argument('--name',default='0311') #prefix to use when saving files to avoid name conflicts
    
    args = parser.parse_args()
    
    return args
    
def main():
    #get args from command line
    args = process_args()
    train_path = Path(args.train_folder)
    model_type = args.model_type
    prefix = args.name
    #import training data
    X_train = pd.read_csv(train_path / "X_train.csv")
    y_train = pd.read_csv(train_path / "y_train.csv")
    #import testing data
    X_test = pd.read_csv(train_path / "X_test.csv")
    y_test = pd.read_csv(train_path / "y_test.csv")
    #train the model
    model = train_model(X_train,y_train,model_type)
    #plot a confusion matrix for the model using a function from plotting.py (which also saves it)
    precision = plot_CM(model,X_test,y_test,train_path,'Trait',prefix)
    
    
if __name__ == '__main__':
    main()
