# Vizualization

Vizualizations in the PREMIX paper were produced in R using the RStudio interface and tidyverse packages. We will walk through a few of these plots as examples of different types of vizualizations.

## Overview
- Line plots
- Violin plots
- Time to event plots
- Heatmaps

## Line plots



## Violin plots



## Time to event plots

We drew heavily on the [excellent tutorial by Emily Zabor](https://www.emilyzabor.com/tutorials/survival_analysis_in_r_tutorial.html) and the R package Survival.

```{r format dates}

# Calculate follow up time / time to event
    tte <- tte %>% mutate(

    # - Time to MDRO_negative post first D01
      tt_MDRO_negative=
        case_when(MDRO_negative_status == 1 ~
                    (as.numeric(
                      difftime(MDRO_Negative,
                               First_D01_Date,
                               units = "days"))),
                  MDRO_negative_status == 0 ~
                    (as.numeric(
                      difftime(Last_Screen,
                               First_D01_Date,
                               units = "days")))
                  ),

    # - Time to first bacterial infection post first D01
      tt_Infection=
        case_when(Infection_status == 1 ~
                    (as.numeric(
                      difftime(Infection_Date,
                               First_D01_Date,
                               units = "days"))),
                  Infection_status == 0 ~
                    (as.numeric(
                      difftime(Last_FollowUp,
                               First_D01_Date,
                               units = "days")))
                  ),
    
    # - Recode for follow up time <= 180 days
      tt_MDRO_infection_lt180 =
        case_when(MDRO_infection_status_180 == 0 &
                    (as.numeric(difftime(Last_FollowUp,
                                         First_D01_Date,
                                         units = "days")) > 180) ~ 180,

                  MDRO_infection_status_180 == 0 &
                    (as.numeric(difftime(Last_FollowUp,
                                         First_D01_Date,
                                         units = "days")) <= 180) ~
                    (as.numeric(
                      difftime(Last_FollowUp,
                               First_D01_Date,
                               units = "days"))),

                  MDRO_infection_status_180 == 1 &
                    (as.numeric(difftime(Last_FollowUp,
                                         First_D01_Date,
                                         units = "days")) <= 180) ~
                    (as.numeric(
                      difftime(MDRO_Infection_Date,
                               First_D01_Date,
                               units = "days"))),

                  MDRO_infection_status_180 == 1 &
                    (as.numeric(difftime(Last_FollowUp,
                                         First_D01_Date,
                                         units = "days")) > 180) ~
                    (as.numeric(
                      difftime(MDRO_Infection_Date,
                               First_D01_Date,
                               units = "days")))
                  ),
    
    # - Code strata by any FMT
      FMT =
        case_when(Group == "Control" ~ "Control",
                  Group == "FMT"     ~ "FMT",
                  Group == "Observation" ~ "FMT"
                  ),
    
    # - Time to first MDR bacterial infection post first D01
      tt_MDRO_infection=
        case_when(MDRO_infection_status == 1 ~
                    (as.numeric(
                      difftime(MDRO_Infection_Date,
                               First_D01_Date,
                               units = "days"))),
                  MDRO_infection_status == 0 ~
                    (as.numeric(
                      difftime(Last_FollowUp,
                               First_D01_Date,
                               units = "days")))
                  )
    )
```

## Heatmaps
