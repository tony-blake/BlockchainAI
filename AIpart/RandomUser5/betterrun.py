import numpy
import lstm
import time
import matplotlib.pyplot as plt

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
     
    plt.show()
    

#Main Run Thread
if __name__=='__main__':
	global_start_time = time.time()
	epochs  = 10
	seq_len = 50

	print('> Loading data... ')

	X_train, y_train, X_test, y_test = lstm.load_data('siraj.csv', seq_len, False)

	print('> Data Loaded. Compiling...')

	model = lstm.build_model([1, 50, 100, 1])

	model.fit(
	    X_train,
	    y_train,
	    batch_size=32,
	    nb_epoch=epochs,
	    validation_split=0.05)

	predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
	#predictedfull = lstm.predict_sequence_full(model, X_test, seq_len)
	#predictedpoint = lstm.predict_point_by_point(model, X_test)        

	print('Training duration (s) : ', time.time() - global_start_time)
	#plot_results_multiple(predictions, y_test, 50)

numpy.savetxt("betterPreditions2.csv", predictions, delimiter=",")
#numpy.savetxt("betterPredictedfull.csv", predictedfull, delimiter=",")
#numpy.savetxt("betterPredictedpoint2.csv", predictedpoint, delimiter=",")
#numpy.savetxt("X_train.csv", X_train, delimiter=",")
#numpy.savetxt("X_test.csv", X_test, delimiter=",")
#numpy.savetxt("y_train.csv", y_train, delimiter=",")
#numpy.savetxt("y_test.csv", y_test, delimiter=",")
#import pandas as pd 
#df = pd.DataFrame(y_test)
#df.to_csv("ytest.csv", header=None)