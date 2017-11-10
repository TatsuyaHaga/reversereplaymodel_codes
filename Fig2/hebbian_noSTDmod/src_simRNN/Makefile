
CC = g++ -Wall -O3

simRNN: simRNN.o Izhikevich_neuron.o
	$(CC) -o ../$@ $^

simRNN.o: simRNN.cpp Izhikevich_neuron.hpp csvio.hpp int2str.hpp
	$(CC) -o $@ -c $<

Izhikevich_neuron.o: Izhikevich_neuron.cpp Izhikevich_neuron.hpp
	$(CC) -o $@ -c $<
