
#ifndef RATEHEBB_NEURON_HPP

#define RATEHEBB_NEURON_HPP

#include <vector>
#include <stdlib.h>
#include <math.h>

class ratehebb_neuron
{
public:
    //parameters
    double samp_pitch; //simulation
    double fI_slope, fI_thr; //f-I curve
    double tauAMPA;
    double etaEsom, tauDelta; //plasticity
    double wmin; //hard boundary for weights
    double wsum; //sum of weights
    //variables
    double output;
    double current;
    double spike;
    double som_input_bias;
    double IAMPA;
    std::vector<double> wEsom, DeltawEsom, wEsomNMDA;
    std::vector<ratehebb_neuron*> wEsom_from;
    //STP
    int STPsw;
    double tauSTD, tauSTP, U_STP;
    double xSTD, xSTP;
    //external functions
    double fIcurve(double I);
    ratehebb_neuron();
    ratehebb_neuron(double samp_pitch_set);
    void init(double samp_pitch_set);
    int add_wEsom(double w_init, double wNMDA_init, ratehebb_neuron *from_neuron);
    void set_som_input_bias(double val);
    void update_weightsum();
    void update_wEsom(int num);
    void update_weights();
    void update_Isom();
    void update_output();
    void update_STP();
    void update_variables();
};

#endif
