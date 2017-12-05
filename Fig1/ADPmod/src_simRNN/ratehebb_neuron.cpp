#include "ratehebb_neuron.hpp"

double ratehebb_neuron::fIcurve(double I)
{
    if(I>fI_thr)
        return fI_slope*(I-fI_thr);
    else
        return 0.0;
}
ratehebb_neuron::ratehebb_neuron()
{}
ratehebb_neuron::ratehebb_neuron(double samp_pitch_set)
{ init(samp_pitch_set); }
void ratehebb_neuron::init(double samp_pitch_set)
{
    //set paremeters
    samp_pitch=samp_pitch_set;
    tauAMPA=10.0;
    tauDelta=1.0*1000.0;
    wmin=0.0;

    fI_slope=0.0025; //kHz
    fI_thr=0.5;

    etaEsom=4.0;

    tauSTD=500.0;
    tauSTP=200.0;
    U_STP=0.6;

    STPsw=1;
    if(STPsw)
    {
        xSTD=1.0;
        xSTP=U_STP;
    }
    else
    {
        xSTD=1.0;
        xSTP=1.0;
    }
    
    //initialize variables
    current=0.0;
    IAMPA=0.0;
    output=0.0;
    spike=0.0;
    som_input_bias=0.0;
    wEsom.clear(); DeltawEsom.clear(); wEsom_from.clear();
    //ADP
    spikeADP=0.0;
    tauADP=80.0;//ms
}
int ratehebb_neuron::add_wEsom(double w_init, double wNMDA_init, ratehebb_neuron *from_neuron)
{
    wEsom.push_back(w_init);
    wEsomNMDA.push_back(wNMDA_init);
    wEsom_from.push_back(from_neuron);
    DeltawEsom.push_back(0.0);
    return wEsom.size()-1;
}
void ratehebb_neuron::set_som_input_bias(double val)
{ som_input_bias=val; }
void ratehebb_neuron::update_wEsom(int num)
{
    if(wEsom_from[num]!=NULL)
    {
        wEsom[num]+=samp_pitch*DeltawEsom[num];
        DeltawEsom[num]+=samp_pitch*(-DeltawEsom[num])/tauDelta;
        DeltawEsom[num]+=samp_pitch*etaEsom/tauDelta*spikeADP*(wEsom_from[num]->spike);
        
        if(wEsom[num]<wmin)
            wEsom[num]=wmin;
    }
}
void ratehebb_neuron::update_weights()
{
    for(unsigned int i=0; i<wEsom.size(); ++i)
        update_wEsom(i);
}
void ratehebb_neuron::update_Isom()
{
    double input_sum=0.0;
    for(unsigned int i=0; i<wEsom.size(); ++i)
        if(wEsom_from[i]!=NULL && wEsom_from[i]->output)
            input_sum+=wEsom[i]*(wEsom_from[i]->output);
    IAMPA+=samp_pitch*(-IAMPA/tauAMPA+input_sum);
    
    current=IAMPA+som_input_bias;
}
void ratehebb_neuron::update_output()
{
    //spike (rate)
    spike=fIcurve(current);
    spikeADP+=(-spikeADP+spike)/tauADP;
    //update output
    output=spike*xSTD*xSTP;
}
void ratehebb_neuron::update_STP()
{
    if(STPsw)
    {
        xSTD+=samp_pitch*((1.0-xSTD)/tauSTD-xSTD*xSTP*spike);
        xSTP+=samp_pitch*((U_STP-xSTP)/tauSTP+U_STP*(1.0-xSTP)*spike);
    }
}
void ratehebb_neuron::update_variables() //after changing inputs
{
    update_weights();
    update_STP();
    update_Isom();
}
