import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import readline

def load_dataset(filename):
    # Load the the predicted and actual types of the inputs in the test datasets

    # Parameters:
    #       filename (Any -> str): the name of the file to load from

    # Returns:
    #       actual(NDArray): the list of the actual type of each input
    #       predicted (NDArray): the list of the predicted type of each input

    f = open(f'{filename}_cm.txt', 'r')
    results = f.read().split('\n~~~~~~\n')
    actual_results = results[0].split('\n~~~~~\n')[1].split(', ')[:-1]
    predicted_results = results[1].split('\n~~~~~\n')[1].split(', ')[:-1]

    actual = np.array(actual_results)
    predicted = np.array(predicted_results)

    return actual, predicted

def compute_cm(filename):
    # Create the confusion matrix

    # Paramters:
    #       filename (Any -> str): the name of the file to load data from

    # Returns:
    #       None
    
    if filename == '2_1':
        title = "Anomaly Zero-shot"
    if filename == '3_1':
        title = "Signature Zero-shot"
    if filename == "anomaly":
        title = "Anomaly Few-shot"
    if filename == "signature":
        title = "Signature Few-shot"
    actual, predicted = load_dataset(filename)
    cm = confusion_matrix(actual, predicted)

    sns.heatmap(cm, annot = True, fmt = 'g', xticklabels = ['Not Prompt Injection', 'Prompt Injection'], yticklabels = ['Not Prompt Injection', 'Prompt Injection'])
    plt.ylabel('Actual', fontsize = 13)
    plt.title(title, fontsize = 17, pad = 20)
    plt.gca().xaxis.set_label_position('top')
    plt.xlabel('Prediction', fontsize = 13)
    plt.gca().xaxis.tick_top()
    plt.gca().figure.subplots_adjust(bottom = 0.2)

    plt.show()

    return

compute_cm('2_1')
compute_cm('3_1')
compute_cm('anomaly')
compute_cm('signature')