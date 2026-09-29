#-------------------------------------------------------------------------------
# Simulation file.
# Notes: 
#   SD of 1e-6 is used when a sampled parameter is "fixed"
#   For steady state calculations, t=1e-6 is used because MCSim requires at 
#     least one t > 0.  Additionally, GM of C_0 is set to 1e-30 and its GSD
#     set to 1.01 in order to avoid underflow/infinities.
#   
#-------------------------------------------------------------------------------
MCMC ("PFHxS_1cpt_v8.MCMC_TrainTest.out","",  # name of output and restart file
      "",                     # name of data file
      20000,0,                 # iterations, print predictions flag,
      10,20000,                 # printing frequency, iters to print
      10101010);              # random seed (default)

M_ln_DWI_BW_d = -4.3955;
SD_ln_DWI_BW_d = 0.888;
SD_ln_Cbgd_sc = 1;
SD_ln_C_0_sc = 1;

Level { # priors on population parameters
  
  # Population Mean Parameters
  Distrib (M_ln_k, Normal, -2.03422, 0.4055); # Elimination rate (1/yr) #  5.3 years
  Distrib (M_ln_Vd, Normal, -1.38629,  0.2624); # Distribution volume (L/kg) 
 
 
# Population SD or Variance Parameters
#  Distrib (V_ln_k, InvGamma, 9, 0.75); # Elimination rate (1/yr)
  Distrib (V_ln_k, LogNormal, 0.20, 1.275); # Elimination rate (1/yr) from PFOA posterior
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
      Distrib (DWC_belowMRL, Uniform, 0, 0.03);
      Level { # All same below MRL level
      Level { # Decatur Training 9 M 9 F individual data
        Distrib (ln_Cbgd, Normal, 0, 1);
        Distrib (ln_C_0, Normal, 0, 1);
        Distrib (ln_DWI_BW_d, Normal, 0, 1);
        Distrib (ln_k, Normal, 0, 1);
        Distrib (ln_Vd, Normal, 0, 1);
  	  
        Likelihood (Cserum, LogNormal, Prediction(Cserum), GSD_Cserum);
  
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFHxS_Decatur_indiv_M_train.in 
        Simulation { # 22
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 15.4;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 15.4,16.6);
        }
  
        Simulation { # 43
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 4.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 4.9,6.1);
        }
  
        Simulation { # 15
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 11.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 11.3,7.8);
        }
  
        Simulation { # 47
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 12.8;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 12.8,5.6);
        }
  
        Simulation { # 56
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 20.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 20.9,12.4);
        }
  
        Simulation { # 14
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 6.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 6.3,6.7);
        }
  
        Simulation { # 42
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 24.4;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 24.4,18.1);
        }
  
        Simulation { # 8
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 24.2;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 24.2,20.2);
        }
  
        Simulation { # 30
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 7.8;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.8,8.5);
        }
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFHxS_Decatur_indiv_F_train.in 
        Simulation { # 50
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 2.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.3,2.5);
        }
  
        Simulation { # 12
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 12.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 12.9,13.7);
        }
  
        Simulation { # 64
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 2.4;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.4,3.3);
        }
  
        Simulation { # 33
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 2.7;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 2.7,4);
        }
  
        Simulation { # 9
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 18.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 18.3,18.4);
        }
  
        Simulation { # 31
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 12.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 12.9,13.2);
        }
  
        Simulation { # 46
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 3.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.3,4.1);
        }
  
        Simulation { # 67
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 16.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 16.9,12.3);
        }
  
        Simulation { # 37
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 8.7;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 8.7,6.5);
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
  ## data/individual/simfiles/PFHxS_Decatur_indiv_M_test.in 
        Simulation { # 5
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 6.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 6.3,4.6);
        }
  
        Simulation { # 10
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 7.1;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.1,7.4);
        }
  
        Simulation { # 13
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 19.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 19.5,14);
        }
  
        Simulation { # 25
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 7.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.5,9);
        }
  
        Simulation { # 32
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 8.6;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 8.6,9.2);
        }
  
        Simulation { # 40
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 12.4;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 12.4,12.8);
        }
  
        Simulation { # 44
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 8.9;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 8.9,6.6);
        }
  
        Simulation { # 51
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 7.4;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.4,6.3);
        }
  
        Simulation { # 59
          # Cbgd
          Cbgd_in_gm = 1.61;
          Cbgd_in_gsd = 2.17;
          # C_0
          C_0_in_gm = 14.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 14.3,15.8);
        }
  
  ## data/individual/Decatur_PFAS_Indiv_WMEL_no3M.xlsx 
  ## data/individual/simfiles/PFHxS_Decatur_indiv_F_test.in 
        Simulation { # 6
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 3.8;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 3.8,4.2);
        }
  
        Simulation { # 24
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 22.1;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 22.1,26);
        }
  
        Simulation { # 29
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 6.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 6.5,5.8);
        }
  
        Simulation { # 39
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 7.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.5,7.9);
        }
  
        Simulation { # 41
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 7.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.5,6.8);
        }
  
        Simulation { # 45
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 7.5;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 7.5,2.4);
        }
  
        Simulation { # 48
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 6;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 6,6.8);
        }
  
        Simulation { # 55
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 18.2;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 18.2,13.2);
        }
  
        Simulation { # 57
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 5.3;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 5.3,3.9);
        }
  
        Simulation { # 61
          # Cbgd
          Cbgd_in_gm = 0.88;
          Cbgd_in_gsd = 2.47;
          # C_0
          C_0_in_gm = 5.6;
          C_0_in_gsd = 1.2;
          DWC = PerDose(DWC_belowMRL,1e+10,0,1e+10);
          # Individual data
          Print(Cserum, 0,5.802);
          Data(Cserum, 5.6,5.4);
        }
  
   
    } ## End Decatur test 
      } # All Decatur same below MRL level
    }	## End Decatur 
  
    Level { # Paulsboro, NJ Population data - TRAIN
      # Intervention 2.2 years prior to serum data
      
      Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);

      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm = 1.18;
        Cbgd_in_gsd = 2.45;
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.0047;#9/17/2013	treated water sample	Post et al. 2013 (support document)
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.2); 
        Data (M_Cbgd_Css, 2.593); # arithmetic mean estiamted from serum geometric mean and 95%CI
      }
    }
	
    Level { # Horsham, PA Population data - TRAIN
      # Intervention 2.0 years prior to serum data
      
      Likelihood (M_Cbgd_Css, LogNormal, Prediction(M_Cbgd_Css), GSD_M_Cbgd_Css);
      
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm =  1.18; # NHANES 2015-2016
        Cbgd_in_gsd =  2.45;# NHANES 2015-2016
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.17; # 06/24/14 - 03/19/15 arithmetic mean water concentration UCMR3 # Note EWG measurement 0.0383
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 27.340); # arithmetic mean estiamted from serum geometric mean and 95%CI
      }
    }		
    
    Level { # Test. Warminster, PA Population data
      
      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm = 1.18;
        Cbgd_in_gsd = 2.45;
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.127; #11/19/13 - 08/19/14 UCMR3 # Note EWG value 0.0262
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 23.157); # arithmetic mean estiamted from serum geometric mean and 95%CI
      }
      
	Level { # TEST Warrington, PA Population data

      Simulation { 
        # Initial estimate of Cbgd distribution
        Cbgd_in_gm = 1.18;
        Cbgd_in_gsd = 2.45;
        # Initial C_0 set to 0
        C_0_in_gm = 1e-30;
        C_0_in_gsd = 1.01;
        # Fixed drinking water concentration
        DWC = 0.0349; #11/01/14 - 11/30/14 EWG 2019
        
        # Population mean data - background + steady state
        Print (M_Cbgd_Css, 2.0); 
        Data (M_Cbgd_Css, 14.851); # arithmetic mean estiamted from serum geometric mean and 95%CI
      }
    }
	}
	
  }
}
End.
