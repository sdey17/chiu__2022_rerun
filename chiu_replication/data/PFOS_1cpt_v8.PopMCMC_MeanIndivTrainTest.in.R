#-------------------------------------------------------------------------------
# Simulation file.
# Notes: 
#   SD of 1e-6 is used when a sampled parameter is "fixed"
#   For steady state calculations, t=1e-6 is used because MCSim requires at 
#     least one t > 0.  Additionally, GM of C_0 is set to 1e-30 and its GSD
#     set to 1.01 in order to avoid underflow/infinities.
#   
#-------------------------------------------------------------------------------
MCMC ("PFOS_1cpt_v8.PopMCMC_MeanIndivTest.out","",  # name of output and restart file
      "",                     # name of data file
      20000,0,                 # iterations (increased due to large rhat), print predictions flag, 
      10,20000,                 # printing frequency, iters to print
      10101010);              # random seed (default)

M_ln_DWI_BW_d = -4.3955;
SD_ln_DWI_BW_d = 0.888;
SD_ln_Cbgd_sc = 1;
SD_ln_C_0_sc = 1;

Level { # priors on population parameters
  
  # Population Mean Parameters
  Distrib (M_ln_k, Normal, -1.8971, 0.4055); # Elimination rate (1/yr) # From 'haf life' in PFOS_INputs_11_1_19.xlsx, without value from Zhang et al. 2013 for over 50 population; SD left as for PFOA as could not find enough additional estimates to adapt
  Distrib (M_ln_Vd, Normal, -1.46968,  0.2624); # Distribution volume (L/kg) . 2.3 From 'Selected' Source in source_PBK_simplify.xlsx (possibly Thomson?) SD left as for PFOA as could not find enough additional estimates to adapt
  
  # Population SD or Variance Parameters
#  Distrib (V_ln_k, InvGamma, 9, 0.75); # Elimination rate (1/yr)
  Distrib (V_ln_k, LogNormal, 0.2024, 1.261);  # Elimination rate (1/yr) #from PFOA as could not find enough additional estimates to adapt
  Distrib (SD_ln_Vd, HalfNormal, 0.17);  # Distribution volume (L/kg)  

  
  # Error GSDs
  Distrib (GSD_Cserum, LogUniform, 1.1, 10.0);
  Distrib (GSD_Cbgd_Css, LogUniform, 1.1, 10.0);
  Distrib (GSD_M_Cbgd_Css, LogUniform, 1.1, 10.0)

  Level { # Studies 
    
    Distrib (M_ln_Cbgd_sc, Normal, -0.22314, 0.4055); # Background serum concentration (ug/L)
    # Centered on log(0.8) = -0.22314 to account for a RSC of 20% for drinking water
    # at background
    Distrib (M_ln_C_0_sc, Normal, 0, 0.4055); # Initial serum concentration (ug/L)
    
    Level { # Decatur Training 9 M 9 F individual data
      Distrib (ln_Cbgd, Normal, 0, 1);
      Distrib (ln_C_0, Normal, 0, 1);
      Distrib (ln_DWI_BW_d, Normal, 0, 1);
      Distrib (ln_k, Normal, 0, 1);
      Distrib (ln_Vd, Normal, 0, 1);
	  
      Likelihood (Cserum_t, LogNormal, Prediction(Cserum_t), GSD_Cserum);


## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
## data/individual/simfiles/PFOS_Decatur_indiv_M_train.in 
      Simulation { # 22
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 82.4;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 82.4,70.3);
      }

      Simulation { # 44
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 32.6;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 32.6,14.2);
      }

      Simulation { # 15
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 236;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 236,75.4);
      }

      Simulation { # 47
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 61;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 61,12.8);
      }

      Simulation { # 56
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 182;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 182,43.9);
      }

      Simulation { # 14
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 25.3;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 25.3,18.8);
      }

      Simulation { # 42
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 113;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 113,24);
      }

      Simulation { # 8
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 78.2;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 78.2,26.4);
      }

      Simulation { # 30
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 54.4;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 54.4,26.5);
      }

## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
## data/individual/simfiles/PFOS_Decatur_indiv_F_train.in 
      Simulation { # 55
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 81.2;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 81.2,31.5);
      }

      Simulation { # 12
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 70.7;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 70.7,50.2);
      }

      Simulation { # 64
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 13.7;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 13.7,12.8);
      }

      Simulation { # 37
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 42;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 42,28.1);
      }

      Simulation { # 9
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 98;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 98,35.1);
      }

      Simulation { # 31
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 56.9;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 56.9,45.9);
      }

      Simulation { # 48
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 32.5;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 32.5,13.3);
      }

      Simulation { # 67
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 60.5;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 60.5,27.6);
      }

      Simulation { # 39
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 43.8;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 43.8,34.7);
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
## data/individual/simfiles/PFOS_Decatur_indiv_M_test.in 
      Simulation { # 5
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 64.1;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 64.1,15);
      }

      Simulation { # 10
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 89.6;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 89.6,24.7);
      }

      Simulation { # 13
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 74.7;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 74.7,39.8);
      }

      Simulation { # 25
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 68.4;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 68.4,30);
      }

      Simulation { # 32
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 72.9;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 72.9,32.2);
      }

      Simulation { # 40
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 78.1;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 78.1,45.4);
      }

      Simulation { # 43
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 24.1;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 24.1,15.4);
      }

      Simulation { # 51
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 60.9;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 60.9,22);
      }

      Simulation { # 59
        # Cbgd
        Cbgd_in_gm = 6.16;
        Cbgd_in_gsd = 2.18;
        # C_0
        C_0_in_gm = 137;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 137,70.7);
      }

## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
## data/individual/simfiles/PFOS_Decatur_indiv_F_test.in 
      Simulation { # 6
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 26.6;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 26.6,15.2);
      }

      Simulation { # 24
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 120;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 120,61.7);
      }

      Simulation { # 29
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 60.9;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 60.9,22.5);
      }

      Simulation { # 41
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 41.1;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 41.1,12.4);
      }

      Simulation { # 45
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 39.2;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 39.2,12.8);
      }

      Simulation { # 46
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 18.1;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 18.1,13.4);
      }

      Simulation { # 50
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 19.4;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 19.4,16.8);
      }

      Simulation { # 57
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 21.5;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 21.5,11.8);
      }

      Simulation { # 61
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 53.8;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 53.8,30.6);
      }

      Simulation { # 33
        # Cbgd
        Cbgd_in_gm = 3.67;
        Cbgd_in_gsd = 2.39;
        # C_0
        C_0_in_gm = 16;
        C_0_in_gsd = 1.2;
        # Time-varying drinking water concentration
        DWC_t = NDoses(10,
        0.11,0.0375,0.13,0.075,0.0375,0.13,0.04,0.08,0.08,0.028,
        0,1.287,2.653,2.998,3.34,3.68,4.027,5.054,5.405,6.171
        );
        # Individual data
        Print(Cserum_t, 0,5.802);
        Data(Cserum_t, 16,6.7);
      }

 
    } 
	## End Decatur 
  
  Level { # Minnesota Training SET - has individual data with only the first concentrations
      Distrib (ln_Cbgd, Normal, 0, 1);
      Distrib (ln_C_0, Normal, 0, 1);
      Distrib (ln_DWI_BW_d, Normal, 0, 1);
      Distrib (ln_k, Normal, 0, 1);
      Distrib (ln_Vd, Normal, 0, 1);

      Likelihood (Cbgd_Css, LogNormal, Prediction(Cbgd_Css), GSD_Cbgd_Css);
    # CL: changed to "Prediction(Cbgd_CSS)"; not sure if has dif GSD param; check MODEL

## data/PFOS_INputs_11_1_19.xlsx
## data/individual/simfiles/PFOS_MDPH_indiv_train.in
      Simulation { # 45
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.19;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 13);
      }

      Simulation { # 49
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.19;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 75
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.6;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 45);
      }

      Simulation { # 40
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 55);
      }

      Simulation { # 90
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.2;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 58);
      }

      Simulation { # 64
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.45;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 43
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 150);
      }

      Simulation { # 55
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 12);
      }

      Simulation { # 27
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.14;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 58);
      }

      Simulation { # 62
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.45;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 21);
      }

      Simulation { # 9
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 19);
      }

      Simulation { # 11
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 25);
      }

      Simulation { # 29
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.17;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 4);
      }

      Simulation { # 46
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.19;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 32);
      }

      Simulation { # 84
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 58);
      }

      Simulation { # 2
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 8.5);
      }

      Simulation { # 17
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.082;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 5.5);
      }

      Simulation { # 14
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.04;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 58);
      }

      Simulation { # 77
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.6;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 97
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.24;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 145);
      }

      Simulation { # 69
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.5;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 77);
      }

      Simulation { # 39
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 91
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.2;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 90);
      }

      Simulation { # 6
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 14);
      }

      Simulation { # 66
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.47;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 21);
      }

      Simulation { # 93
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.8;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 35);
      }

      Simulation { # 36
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 28);
      }

      Simulation { # 26
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.14;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 7);
      }

      Simulation { # 54
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.25;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 150);
      }

      Simulation { # 81
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 76
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.6;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 50);
      }

      Simulation { # 42
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 70);
      }

      Simulation { # 22
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.13;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 21);
      }

      Simulation { # 50
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.195;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 19);
      }

      Simulation { # 48
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.19;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 40);
      }

      Simulation { # 87
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.72;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 70);
      }

      Simulation { # 80
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 45);
      }

      Simulation { # 10
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 22);
      }

      Simulation { # 28
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.15;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 29);
      }

      Simulation { # 20
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.09;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 28);
      }

      Simulation { # 21
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.11;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 6.5);
      }

      Simulation { # 57
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 22);
      }

      Simulation { # 23
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.13;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 21);
      }

      Simulation { # 13
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 41);
      }

      Simulation { # 67
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.47;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 41);
      }

      Simulation { # 18
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.082;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 16);
      }

      Simulation { # 41
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 70);
      }

      Simulation { # 30
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.17;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 16);
      }

      Simulation { # 37
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
        Data(Cbgd_Css, 30);
      }


    }
	## End Minnesota Training

  Level { # Minnesota Test SET - has individual data with only the first concentrations
      Distrib (ln_Cbgd, Normal, 0, 1);
      Distrib (ln_C_0, Normal, 0, 1);
      Distrib (ln_DWI_BW_d, Normal, 0, 1);
      Distrib (ln_k, Normal, 0, 1);
      Distrib (ln_Vd, Normal, 0, 1);


## data/PFOS_INputs_11_1_19.xlsx
## data/individual/simfiles/PFOS_MDPH_indiv_test_in
      Simulation { # 1
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 3);
      }

      Simulation { # 3
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 8.7);
      }

      Simulation { # 4
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 9);
      }

      Simulation { # 5
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 11);
      }

      Simulation { # 7
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 15);
      }

      Simulation { # 8
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 16);
      }

      Simulation { # 12
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.035;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 40);
      }

      Simulation { # 15
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.043;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 26);
      }

      Simulation { # 16
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.07;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 18);
      }

      Simulation { # 19
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.082;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 20);
      }

      Simulation { # 24
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.13;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 35);
      }

      Simulation { # 25
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.13;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 41);
      }

      Simulation { # 31
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 12);
      }

      Simulation { # 32
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 15);
      }

      Simulation { # 33
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 18);
      }

      Simulation { # 34
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 20);
      }

      Simulation { # 35
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 25);
      }

      Simulation { # 38
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 38);
      }

      Simulation { # 44
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.18;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 160);
      }

      Simulation { # 47
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.19;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 32);
      }

      Simulation { # 51
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.24;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 7);
      }

      Simulation { # 52
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.24;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 28);
      }

      Simulation { # 53
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.25;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 40);
      }

      Simulation { # 56
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 12);
      }

      Simulation { # 58
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 80);
      }

      Simulation { # 59
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 90);
      }

      Simulation { # 60
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.4;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 22);
      }

      Simulation { # 61
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.4;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 50);
      }

      Simulation { # 63
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.45;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 21);
      }

      Simulation { # 65
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.45;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 60);
      }

      Simulation { # 68
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.5;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 61);
      }

      Simulation { # 70
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.51;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 120);
      }

      Simulation { # 71
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.52;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 18);
      }

      Simulation { # 72
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.55;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 35);
      }

      Simulation { # 73
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.55;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 68);
      }

      Simulation { # 74
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.6;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 35);
      }

      Simulation { # 78
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.6;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 53);
      }

      Simulation { # 79
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 35);
      }

      Simulation { # 82
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 57);
      }

      Simulation { # 83
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 58);
      }

      Simulation { # 85
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.65;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 71);
      }

      Simulation { # 86
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.7;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 65);
      }

      Simulation { # 88
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 0.8;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 18);
      }

      Simulation { # 89
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 40);
      }

      Simulation { # 92
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.3;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 26);
      }

      Simulation { # 94
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.8;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 90);
      }

      Simulation { # 95
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.8;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 91);
      }

      Simulation { # 96
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.8;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 180);
      }

      Simulation { # 98
        # Cbgd
        Cbgd_in_gm = 13.47;
        Cbgd_in_gsd = 2.21;
        # C_0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Constant drinking water concentration
        DWC = 1.25;


        # Individual data
        Print(Cbgd_Css, 1e-06);
         Data(Cbgd_Css, 130);
      }

}
 ## End Individual TEST SETS
  Level { # Paulsboro, NJPopulation data ;Graber et al. 2019 , -- TRAIN sample dates 01/01/16 - 12/31/2016; n=186; age range: 12 to >=60 years; median age=47 years; PFAS_DATA PFOS sheet
    # Intervention 2.2 years prior to serum data
    
    Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);
    
    Simulation { 
      # Initial estimate of Cbgd distribution
      Cbgd_in_gm = 4.72 ; #GET rom NHANES 2015 total PFOS data; all sex; ages 12+  
      Cbgd_in_gsd = 2.38 ; # # from NHANES 2015 total PFOS data; all sex; ages 12+  
      # Initial C_0 set to 0
      C_0_in_gm = 1e-30;
      C_0_in_gsd = 1.01;
      # Fixed drinking water concentration
      DWC = .01; # Earlier (2009-10) than serum concentrations;  from Post et al. 2013
      
      # Population mean data - background + steady state
      Print (M_Cbgd_Css, 2.2); 
      Data (M_Cbgd_Css, 7.69);   # serum arithmetic mean estimated from geomean and 95ci from PFOS sheet in PFAS_DATA.xlsx      
      
      
    }
  }
  
  Level { # Horsham PA UCMR3, Penn DOH 2019; -- TRAIN water concentration in ppt--may have been pp thousand instead of pptr. Looks low
    # Intervention 2.0 years prior to serum data
    
    Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);

    Simulation { 
      # Initial estimate of Cbgd distribution
      Cbgd_in_gm = 4.72 ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
      Cbgd_in_gsd = 2.38  ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
      # Initial C_0 set to 0
      C_0_in_gm = 1e-30;
      C_0_in_gsd = 1.01;
      # Fixed drinking water concentration
      DWC = 0.2996; #    drinking water mean from PFOS sheet in PFAS_DATA.xlsx; UCMR3 06/24/14 - 03/19/15
      
      
      # Population mean data - background + steady state
      Print (M_Cbgd_Css, 2.0); 
      Data (M_Cbgd_Css, 24.639); # serum arithmetic mean estimated from geomean and geosd PFOS sheet in PFAS_DATA.xlsx; Penn DOH 2019         
      
    }
  }
  
  Level { # Test. Warminster, PA Population data
    
    Simulation { 
      # Initial estimate of Cbgd distribution
      Cbgd_in_gm = 4.72 ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
      Cbgd_in_gsd = 2.38  ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
      # Initial C_0 set to 0
      C_0_in_gm = 1e-30;
      C_0_in_gsd = 1.01;
      # Fixed drinking water concentration
      DWC = 0.28; # UCMR3
      
      # Population mean data - background + steady state
      Print (M_Cbgd_Css, 2.0); 
      Data (M_Cbgd_Css, 21.378); # arithmetic mean estiamted from serum geometric mean and 95%CI
    }
  }
  
    
    Level { # Warrington, PA ;Penn DOH 2019; n=41 (children aged 3-17 included however reports states that majority of participants were adults)
  
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm = 4.72 ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
        Cbgd_in_gsd = 2.38  ; #GET rom NHANES 2015 total PFOS data; all sex;  ages 12+  
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.67; #    drinking water mean from PFOS sheet in PFAS_DATA.xlsx; 01/01/14 - 12/31/14 Warrington Township 2014
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 20.754); # serum arithmetic mean est from geomean and 95ci PFOS sheet in PFAS_DATA.xlsx; Penn DOH 2019         
     
      }
    }

   }
}
End.
