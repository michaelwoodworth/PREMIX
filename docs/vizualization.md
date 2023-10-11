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

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(readr)
library(survival)
library(survminer)
library(cowplot)

path      <-"/PREMIX/Analyses/Data"
date_file <- "TimetoEvent.csv"

tte <- read_csv(paste0(path,"/",date_file),
                col_types = cols(First_D01_Date = col_date(format = "%m/%d/%y"),
                                 Last_FollowUp = col_date(format = "%m/%d/%y"),
                                 Last_Screen = col_date(format = "%m/%d/%y"),
                                 MDRO_Negative = col_date(format = "%m/%d/%y"),
                                 Infection_Date = col_date(format = "%m/%d/%y"),
                                 MDRO_Infection_Date = col_date(format = "%m/%d/%y")))
```

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
    )
```

```{r survival function analyses}

  # - Create / inspect survival objects

   MDRO_status_surv <- Surv(tte$tt_MDRO_negative, tte$MDRO_negative_status)
   MDRO_infx_surv   <- Surv(tte$tt_Infection, tte$Infection_status)

   
  # Estimate curves with Kaplan-Meier method
   
   MDRO_status_curve <- survfit(Surv(tt_MDRO_negative, MDRO_negative_status) ~ 1,
                                data = tte)

  # - Time to MDRO decolonization post first D01  [stratify by randomization]
    MDRO_decol_plot <- ggsurvplot(
     fit = survfit(Surv(tt_MDRO_negative, 
                        MDRO_negative_status) ~ Group,
                                data = tte),
     xlab = "Days",
     ylab = "Overall decolonization probability",
     palette = "uchicago"
    )

  # - Time to MDR bacterial infection post first D01  [stratify by randomization]
          # censored at 180 days
    MDRO_infection180_plot <- ggsurvplot(
     fit = survfit(Surv(tt_MDRO_infection_lt180, 
                        # MDRO_infection_status) ~ Randomization,
                        MDRO_infection_status) ~ Group,
                                data = tte),
     xlab = "Days",
     ylab = "Free from MDRO infection",
     title = "Time to MDRO infection by group",
     palette = "uchicago"
   )        

  # View plots
    MDRO_decol_plot
    MDRO_infection180_plot

```

## Heatmaps
