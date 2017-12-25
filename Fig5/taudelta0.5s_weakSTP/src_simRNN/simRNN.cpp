
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include "csvio.hpp"
#include "int2str.hpp"
#include "ratehebb_neuron.hpp"

void save_weights(std::vector<ratehebb_neuron> &excneuron, std::vector<std::vector<std::vector<double> > > &from_neuron, const char *str)
{
    std::string stamp=str;
    std::string name;
    std::vector<double> temp_vec(4);
    //std::vector<std::vector<double> > param;
    writeCSV<double> writer;
    writer.set_delimiter(',');
    
    //EE
    //param.clear();
    name="WEE_"+stamp+".csv";
    writer.open(name.c_str());
    for(unsigned int i=0; i<excneuron.size(); ++i)
        for(unsigned int j=0; j<excneuron[i].wEsom.size(); ++j)
        {
            temp_vec[0]=from_neuron[0][i][j]; temp_vec[1]=i;
            temp_vec[2]=excneuron[i].wEsom[j];
            temp_vec[3]=excneuron[i].wEsomNMDA[j];
            writer.write1D(temp_vec);
            //param.push_back(temp_vec);
        }
    writer.close();
    //savetxt<double>(name.c_str(), param, ',');    
}

int main(int argc, char *argv[])
{
    if(argc!=3)
    {
        fprintf(stderr, "Usage: %s [N of excneuron] [sampling pitch [ms]]\n", argv[0]);
        exit(-1);
    }
    
    //simulation settings
    int NE=atoi(argv[1]);
    double samp_pitch=atof(argv[2]); //[ms]
    double plot_pitch=10.0; //[ms]
    double plot_pitch_weight=0.1*1000.0; //[ms]
    
    double inh_global=1.0;
    double tau_inh=10.0;//ms
    double Iinh=0.0;
    
    /********** read & create networks **********/
    //exc neuron
    std::vector<ratehebb_neuron> excneuron(NE);
    for(int i=0; i<NE; ++i)
    {
        excneuron[i].init(samp_pitch);
        //excneuron[i].setIBparam();
    }
    
    //synapses
    std::vector<double> temp_vec;
    std::vector<std::vector<double> > param;
    std::vector<std::vector<std::vector<double> > > from_neuron(1);
    //E<-E
    param=loadtxt<double>("WEEinit.csv");
    from_neuron[0].resize(NE);
    for(unsigned int i=0; i<param.size(); ++i)
    {
        temp_vec=param[i]; //to, from, wAMPA, wNMDA
        if(temp_vec[0]!=temp_vec[1])
            excneuron[temp_vec[1]].add_wEsom(temp_vec[2], temp_vec[3], &excneuron[temp_vec[0]]);
        //else
        //    excneuron[temp_vec[1]].add_wEsom(0.0, 0.0, NULL);
        from_neuron[0][temp_vec[1]].push_back(temp_vec[0]);
    }

    //update weight sum
    for(int i=0; i<NE; ++i)
        excneuron[i].update_weightsum();
    
    //open output file
    writeCSV<double> f_spikeE("spikeE.csv"); f_spikeE.set_delimiter(',');
    writeCSV<double> f_xSTD("xSTD.csv"); f_xSTD.set_delimiter(',');
    writeCSV<double> f_output("output.csv"); f_output.set_delimiter(',');

    //output weightbias
    writeCSV<double> f_wbias("wbias.csv"); f_wbias.set_delimiter(',');
    double bias_plus, bias_minus;
    
    /********** simulate & save **********/
    readCSVstdin<double> read_input;
    std::vector<double> input;
    double time_ms=0.0;
    std::cerr << "simulation start." << std::endl;
    for(int t=1; ; ++t) //t<sim_len+1
    {
        time_ms=samp_pitch*(double)t;
        if(t%(int)(1.0/samp_pitch*1000.0)==0)
            std::cerr << time_ms/1000.0 << "s" << std::endl;
        if(!isfinite(excneuron[0].output))
        {
            std::cerr << "output invalid. " << time_ms << std::endl;
            exit(-1);
        }

        //read input
        input=read_input.read1D();
        if((signed int)input.size()!=NE)
            break;

        //inh feedback
        Iinh+=samp_pitch*(-Iinh)/tau_inh;
        for(int to=0; to<NE; ++to)
            Iinh+=samp_pitch*inh_global*excneuron[to].output;

        //set external inputs
        for(int to=0; to<NE; ++to)
            excneuron[to].set_som_input_bias(input[to]-Iinh);

        //update variables
        for(int to=0; to<NE; ++to)
            excneuron[to].update_variables();

        //update rates
        for(int to=0; to<NE; ++to)
            excneuron[to].update_output();
        
        //save results
        if(t%(int)(plot_pitch/samp_pitch)==0)
        {
            temp_vec.resize(NE+1);
            temp_vec[0]=time_ms;
            for(int i=0; i<NE; ++i)
                temp_vec[i+1]=excneuron[i].spike;
            f_spikeE.write1D(temp_vec);

            temp_vec.resize(NE+1);
            temp_vec[0]=time_ms;
            for(int i=0; i<NE; ++i)
                temp_vec[i+1]=excneuron[i].xSTD;
            f_xSTD.write1D(temp_vec);

            temp_vec.resize(NE+1);
            temp_vec[0]=time_ms;
            for(int i=0; i<NE; ++i)
                temp_vec[i+1]=excneuron[i].output;
            f_output.write1D(temp_vec);
        }
        if(t==1 || t%(int)(plot_pitch_weight/samp_pitch)==0)
        {
            temp_vec.resize(3);
            temp_vec[0]=time_ms;
            //cell 100
            bias_plus=0.0; bias_minus=0.0;
            for(unsigned int to=0; to<excneuron.size(); ++to)
                for(unsigned int from=0; from<excneuron[to].wEsom.size(); ++from)
                    if(from_neuron[0][to][from]==100)
                    {
                        if(to>100)
                            bias_plus+=excneuron[to].wEsom[from];
                        else
                            bias_minus+=excneuron[to].wEsom[from];
                        break;
                    }
            temp_vec[1]=bias_minus-bias_plus;
            //cell 400
            bias_plus=0.0; bias_minus=0.0;
            for(unsigned int to=0; to<excneuron.size(); ++to)
                for(unsigned int from=0; from<excneuron[to].wEsom.size(); ++from)
                    if(from_neuron[0][to][from]==400)
                    {
                        if(to>400)
                            bias_plus+=excneuron[to].wEsom[from];
                        else
                            bias_minus+=excneuron[to].wEsom[from];
                        break;
                    }
            temp_vec[2]=bias_minus-bias_plus;
            f_wbias.write1D(temp_vec);
        }
    }
    //save weights
    save_weights(excneuron, from_neuron, "end");

    std::cerr << "simulation end." << std::endl;
    return 0;
}
