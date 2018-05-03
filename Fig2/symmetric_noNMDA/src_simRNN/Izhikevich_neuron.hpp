
#ifndef IZHIKEVICH_NEURON_HPP

#define IZHIKEVICH_NEURON_HPP

#include <vector>
#include <stdlib.h>
#include <math.h>

class Izhikevich_neuron
{
public:
    //parameters
    double samp_pitch; //simulation
    double a, b, c, d; //Izhikevich
    double tauAMPA, tauNMDA;
    double eta, tauDelta; //plasticity
    double Aplus, Aminus, tauplus, tauminus; //STDP
    double wmin; //hard boundary for weights
    int STDPtype, STDPmod_sw;
    //variables
    double output, output_nodelay;
    double voltage;
    int spike;
    double som_input_bias;
    double gAMPA, gNMDA;
    double ref; //Izhikevich
    std::vector<double> wE, DeltawE, wENMDA;
    std::vector<Izhikevich_neuron*> wE_from;
    //spike history
    double spiketime_max;
    std::vector<double> spiketime_hist;
    std::vector<double> output_hist;
    //delay
    int delay_len;
    std::vector<double> output_delay;
    //STP
    int STPsw;
    double tauSTD, tauSTP, U_STP;
    double xSTD, xSTP;
    //external functions
    double NMDAfunc(double V);
    Izhikevich_neuron();
    Izhikevich_neuron(double samp_pitch_set, int STDPtype_set, int STDPmod_sw_set); //STDPtype 1:Hebbian 2:anti-Hebbian, 3:symmetric
    void init(double samp_pitch_set, int STDPtype_set, int STDPmod_sw_set);
    void setRSparam();
    void setIBparam();
    void setFSparam();
    int add_wE(double w_init, double wNMDA_init, Izhikevich_neuron *from_neuron);
    void set_som_input_bias(double val);
    double STDPplus(double tau);
    double STDPminus(double tau);
    double STDPsym(double tau);
    void update_wE(int num);
    void update_weights();
    void update_Isom();
    void update_output();
    void update_STP();
    void update_variables();
};

#endif
