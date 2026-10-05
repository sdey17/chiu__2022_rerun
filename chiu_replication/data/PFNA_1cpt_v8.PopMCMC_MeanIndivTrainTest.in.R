#-------------------------------------------------------------------------------
# Simulation file.
# Notes: 
#   SD of 1e-6 is used when a sampled parameter is "fixed"
#   For steady state calculations, t=1e-6 is used because MCSim requires at 
#     least one t > 0.  Additionally, GM of C_0 is set to 1e-30 and its GSD
#     set to 1.01 in order to avoid underflow/infinities.
#   
#-------------------------------------------------------------------------------
MCMC ("PFNA_1cpt_v8.pop_MCMC_Train.out","",  # name of output and restart file
      "",                     # name of data file
      20000,0,                 # iterations, print predictions flag, 40000,0
      10,20000 ,                 # printing frequency, iters to print 20, 40000
      10101010);              # random seed (default)

M_ln_DWI_BW_d = -4.3955;
SD_ln_DWI_BW_d = 0.888;
SD_ln_Cbgd_sc = 1;
SD_ln_C_0_sc = 1;

Level { # priors on population parameters
  
    # Population Mean Parameters
  Distrib (M_ln_k, Normal, -1.80181, 0.4055); # Elimination rate (1/yr) 
  Distrib (M_ln_Vd, Normal, -1.77196,  0.2624); # Distribution volume (L/kg) 
 
 
# Population SD or Variance Parameters
#  Distrib (V_ln_k, InvGamma, 9, 0.75); # Elimination rate (1/yr)
  Distrib (V_ln_k, LogNormal, 0.2000, 1.275); # Elimination rate (1/yr) from PFOA posterior
  Distrib (SD_ln_Vd, HalfNormal, 0.17); # Distribution volume (L/kg) from PFOA posterior.  

  
  # Error GSDs
  Distrib (GSD_Cserum, LogUniform, 1.1, 10.0);
  Distrib (GSD_M_Cbgd_Css, LogUniform, 1.1, 10.0)


  Level { # Studies 
    
    Distrib (M_ln_Cbgd_sc, Normal, -0.22314, 0.4055); # Background serum concentration (ug/L)
    # Centered on log(0.8) = -0.22314 to account for a RSC of 20% for drinking water
    # at background
    Distrib (M_ln_C_0_sc, Normal, 0, 0.4055); # Initial serum concentration (ug/L)
    
    
    Level { # Decatur
      Distrib (DWC_belowMRL, Uniform, 0, 0.02);
      
      Level { # All Decatur have the same DWC below MRL
        
      Level { # Decatur Training 9 M 9 F individual data
        Distrib (ln_Cbgd, Normal, 0, 1);
        Distrib (ln_C_0, Normal, 0, 1);
        Distrib (ln_DWI_BW_d, Normal, 0, 1);
        Distrib (ln_k, Normal, 0, 1);
        Distrib (ln_Vd, Normal, 0, 1);
  	  
        Likelihood (Cserum, LogNormal, Prediction(Cserum), GSD_Cserum);
  
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFNA_Decatur_indiv_M_train.in 
        Simulation { # 22
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.9,1.1);
        }
  
        Simulation { # 43
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.1,0.9);
        }
  
        Simulation { # 15
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 2.1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.1,0.7);
        }
  
        Simulation { # 47
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.9,0.5);
        }
  
        Simulation { # 56
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 3.5;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.5,0.9);
        }
  
        Simulation { # 14
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.2,0.6);
        }
  
        Simulation { # 42
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 2.7;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.7,0.8);
        }
  
        Simulation { # 8
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.7;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.7,0.5);
        }
  
        Simulation { # 30
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.1,0.6);
        }
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFNA_Decatur_indiv_F_train.in 
        Simulation { # 50
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.6;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.6,1);
        }
  
        Simulation { # 12
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2,1.1);
        }
  
        Simulation { # 64
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1,0.4);
        }
  
        Simulation { # 33
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.7;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.7,0.4);
        }
  
        Simulation { # 9
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 3.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.9,1.2);
        }
  
        Simulation { # 31
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 2.4;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.4,3.6);
        }
  
        Simulation { # 46
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.2,0.6);
        }
  
        Simulation { # 67
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 2.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.9,0.9);
        }
  
        Simulation { # 37
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.2,0.4);
        }
  
   
      } 
  ## End Decatur training
    
    Level { # Decatur TEST SET - has individual data with only the first concentrations
        Distrib (ln_Cbgd, Normal, 0, 1);
        Distrib (ln_C_0, Normal, 0, 1);
        Distrib (ln_DWI_BW_d, Normal, 0, 1);
        Distrib (ln_k, Normal, 0, 1);
        Distrib (ln_Vd, Normal, 0, 1);

  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFNA_Decatur_indiv_M_test.in 
        Simulation { # 5
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.5;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.5,0.4);
        }
  
        Simulation { # 10
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 3.3;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.3,1);
        }
  
        Simulation { # 13
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.8;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.8,0.6);
        }
  
        Simulation { # 25
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.6;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.6,0.7);
        }
  
        Simulation { # 32
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 4.3;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 4.3,1.4);
        }
  
        Simulation { # 40
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.7;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.7,1.4);
        }
  
        Simulation { # 44
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 1.3;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.3,0.4);
        }
  
        Simulation { # 51
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 3;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3,1);
        }
  
        Simulation { # 59
          # Cbgd
          Cbgd_in_gm = 0.63;
          Cbgd_in_gsd = 1.93;
          # C_0
          C_0_in_gm = 3.1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.1,1.3);
        }
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFNA_Decatur_indiv_F_test.in 
        Simulation { # 6
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.5;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.5,1.2);
        }
  
        Simulation { # 24
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 3.1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.1,1.9);
        }
  
        Simulation { # 29
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.9,0.8);
        }
  
        Simulation { # 39
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1,1.1);
        }
  
        Simulation { # 41
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.2,0.4);
        }
  
        Simulation { # 45
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 2.5;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.5,0.9);
        }
  
        Simulation { # 48
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.2;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.2,0.4);
        }
  
        Simulation { # 55
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 2.3;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.3,0.7);
        }
  
        Simulation { # 57
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.5;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.5,0.5);
        }
  
        Simulation { # 61
          # Cbgd
          Cbgd_in_gm = 0.53;
          Cbgd_in_gsd = 2.18;
          # C_0
          C_0_in_gm = 1.9;
          C_0_in_gsd = 1.2;
          # Time-varying drinking water concentration
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 1.9,1.1);
        }
  
   
      } ## End Decatur Test
      } # Decatur all one value below MRL
    }	## End Decatur 
  
    Level { # Paulsboro, NJ Population data -- TRAIN
      # Intervention 2.2 years prior to serum data
      
      Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);
      
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm =  0.58;# NHANES 2015-2016 12+
        Cbgd_in_gsd = 2.07;# NHANES 2015-2016 12+
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.072;
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.2); 
        Data (M_Cbgd_Css, 5.71);
      }
    }
    Level { # Horsham, PA Population data -- TRAIN
      # Intervention 2.0 years prior to serum data
      
      Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);
      Distrib (DWC_belowMRL, Uniform, 0, 0.02);
      
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm =  0.58;# NHANES 2015-2016 12+
        Cbgd_in_gsd = 2.07;# NHANES 2015-2016 12+
        
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 0.925); 
      }
    }
    
	

	Level { # Test Warminster, PA Population data
	  # Intervention 2.0 years prior to serum data
	  
	    Distrib (DWC_belowMRL, Uniform, 0, 0.02);
	  
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm =  0.58;# NHANES 2015-2016 12+
        Cbgd_in_gsd = 2.07;# NHANES 2015-2016 12+
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 1.060); # used earliest concentration
      }
    }
 
  }
}
End.
