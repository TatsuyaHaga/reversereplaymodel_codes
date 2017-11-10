#include "Izhikevich_neuron.hpp"

double Izhikevich_neuron::NMDAfunc(double V)
{
    double temp=(V+80.0)/60.0;
    return temp*temp/(1.0+temp*temp);
}
Izhikevich_neuron::Izhikevich_neuron()
{}
Izhikevich_neuron::Izhikevich_neuron(double samp_pitch_set, int STDPtype_set, int STDPmod_sw_set)
{ init(samp_pitch_set, STDPtype_set, STDPmod_sw_set); }
void Izhikevich_neuron::init(double samp_pitch_set, int STDPtype_set, int STDPmod_sw_set)
{
    //set paremeters
    samp_pitch=samp_pitch_set;
    STDPtype=STDPtype_set;
    STDPmod_sw=STDPmod_sw_set;
    
    tauAMPA=5.0;
    tauNMDA=150.0;
    tauDelta=1.0*1000.0;
    wmin=0.0;

    a=0.02;
    b=0.2;
    c=-65.0;
    d=8.0;

    if(STDPmod_sw)
        eta=0.05;
    else
        eta=0.01;
    if(STDPtype!=1 && STDPtype!=2 && STDPtype!=3)
        eta=0.0;
    Aplus=1.0;
    Aminus=0.5;
    tauplus=20.0; //ms
    tauminus=40.0; //ms
    spiketime_max=500.0; //ms

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
    voltage=c; ref=b*c;
    gAMPA=0.0; gNMDA=0.0;
    output=0.0; output_nodelay=0.0;
    spike=0;
    som_input_bias=0.0;
    wE.clear(); DeltawE.clear(); wE_from.clear(); wENMDA.clear();
    spiketime_hist.clear(); output_hist.clear();

    delay_len=(int)(2.0/samp_pitch);
    if(delay_len<=0)
        delay_len=1;
    output_delay.resize(delay_len);
    for(int i=0; i<delay_len; ++i)
        output_delay[i]=0.0;
}
void Izhikevich_neuron::setRSparam()
{ a=0.02; b=0.2; c=-65.0; d=8.0; }
void Izhikevich_neuron::setIBparam()
{ a=0.02; b=0.2; c=-55.0; d=4.0; }
void Izhikevich_neuron::setFSparam()
{ a=0.1; b=0.2; c=-65.0; d=2.0; }
int Izhikevich_neuron::add_wE(double w_init, double wNMDA_init, Izhikevich_neuron *from_neuron)
{
    wE.push_back(w_init);
    wENMDA.push_back(wNMDA_init);
    wE_from.push_back(from_neuron);
    DeltawE.push_back(0.0);
    return wE.size()-1;
}
void Izhikevich_neuron::set_som_input_bias(double val)
{ som_input_bias=val; }
double Izhikevich_neuron::STDPplus(double tau)
{ return Aplus*exp(-tau/tauplus); }
double Izhikevich_neuron::STDPminus(double tau)
{ return -Aminus*exp(-tau/tauminus); }
double Izhikevich_neuron::STDPsym(double tau)
{ return STDPplus(tau)+STDPminus(tau); }
void Izhikevich_neuron::update_wE(int num)
{
    double tmp;
    if(wE_from[num]!=NULL)
    {
        wE[num]+=samp_pitch*DeltawE[num];
        DeltawE[num]+=samp_pitch*(-DeltawE[num])/tauDelta;
        
        if(wE_from[num]->output_nodelay) //post->pre
        {
            for(unsigned int i=0; i<spiketime_hist.size(); ++i)
            {
                switch(STDPtype)
                {
                case 1: //Hebbian
                    tmp=STDPminus(spiketime_hist[i]); break;
                case 2: //anti-Hebbian
                    tmp=STDPplus(spiketime_hist[i]); break;
                case 3: //symmetric
                    tmp=STDPsym(spiketime_hist[i]); break;
                default:
                    tmp=0.0; break;
                }
                if(STDPmod_sw)
                    DeltawE[num]+=eta/tauDelta*(wE_from[num]->output_nodelay)*tmp;
                else
                    DeltawE[num]+=eta/tauDelta*tmp;
            }
        }
        
        if(spike) //pre->post
        {
            for(unsigned int i=0; i<(wE_from[num]->spiketime_hist).size(); ++i)
            {
                tmp=0.0;
                switch(STDPtype)
                {
                case 1: //Hebbian
                    tmp=STDPplus(wE_from[num]->spiketime_hist[i]); break;
                case 2: //anti-Hebbian
                    tmp=STDPminus(wE_from[num]->spiketime_hist[i]); break;
                case 3: //symmetric
                    tmp=STDPsym(wE_from[num]->spiketime_hist[i]); break;
                default:
                    tmp=0.0; break;
                }
                if(STDPmod_sw)
                    DeltawE[num]+=eta/tauDelta*(wE_from[num]->output_hist[i])*tmp;
                else
                    DeltawE[num]+=eta/tauDelta*tmp;
            }
        }
        
        if(wE[num]<wmin)
            wE[num]=wmin;
    }
}
void Izhikevich_neuron::update_weights()
{
    for(unsigned int i=0; i<wE.size(); ++i)
        update_wE(i);
}
void Izhikevich_neuron::update_Isom()
{
    voltage+=samp_pitch*(0.04*voltage*voltage+5.0*voltage+140.0-ref+gAMPA*(0.0-voltage)+NMDAfunc(voltage)*gNMDA*(0.0-voltage)+som_input_bias);
    ref+=samp_pitch*(a*(b*voltage-ref));

    double input_sum=0.0;
    for(unsigned int i=0; i<wE.size(); ++i)
        if(wE_from[i]!=NULL && wE_from[i]->output)
            input_sum+=wE[i]*wE_from[i]->output/samp_pitch;
    gAMPA+=samp_pitch*(-gAMPA/tauAMPA+input_sum);
    
    //NMDA
    input_sum=0.0;
    for(unsigned int i=0; i<wENMDA.size(); ++i)
        if(wE_from[i]!=NULL && wE_from[i]->output)
            input_sum+=wENMDA[i]*(wE_from[i]->output)/samp_pitch;
    gNMDA+=samp_pitch*(-gNMDA/tauNMDA+input_sum);
}
void Izhikevich_neuron::update_output()
{
    //spike
    if(voltage>=30.0)
    { spike=1; voltage=c; ref+=d; }
    else
    { spike=0; }
    //update output
    output_nodelay=spike*xSTD*xSTP;
    output=output_delay[0];
    for(int i=1; i<delay_len; ++i)
        output_delay[i-1]=output_delay[i];
    output_delay.back()=output_nodelay;

    //spike history for STDP
    if(spike)
    { spiketime_hist.push_back(0.0); output_hist.push_back(output_nodelay); }
    std::vector<double>::iterator it_t=spiketime_hist.begin();
    std::vector<double>::iterator it_o=output_hist.begin();
    while(it_t!=spiketime_hist.end())
    {
        if((*it_t)<spiketime_max)
        {
            (*it_t)+=samp_pitch;
            ++it_t; ++it_o;
        }
        else
        {
            it_t=spiketime_hist.erase(it_t);
            it_o=output_hist.erase(it_o);
        }
    }
}
void Izhikevich_neuron::update_STP()
{
    if(STPsw)
    {
        xSTD+=samp_pitch*((1.0-xSTD)/tauSTD)-xSTD*xSTP*spike;
        xSTP+=samp_pitch*((U_STP-xSTP)/tauSTP)+U_STP*(1.0-xSTP)*spike;
    }
}
void Izhikevich_neuron::update_variables() //after changing inputs
{
    update_weights();
    update_STP();
    update_Isom();
}
