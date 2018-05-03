
CC = g++ -Wall -O3

simRNN: simRNN.o ratehebb_neuron.o
	$(CC) -o ../$@ $^

simRNN.o: simRNN.cpp ratehebb_neuron.hpp csvio.hpp int2str.hpp
	$(CC) -o $@ -c $<

ratehebb_neuron.o: ratehebb_neuron.cpp ratehebb_neuron.hpp
	$(CC) -o $@ -c $<
