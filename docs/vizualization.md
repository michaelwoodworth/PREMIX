# Vizualization

Vizualizations in the PREMIX paper were produced in R using the RStudio interface and tidyverse packages. We will walk through a few of these plots as examples of different types of vizualizations.

## Overview
- Line plots
- Time to event plots
- Heatmaps

In the visualization page for my [practical metagenomics](https://github.com/michaelwoodworth/practicalmetagenomics/blob/main/pages/23.03.24.md) repository, we include R code for generating plotting functions, manual color schemes, and looping over IDs to create multiple plots from a data set.

## Line plots

```r
knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(ggtext)
library(glue)
library(readr)
library(lubridate)
library(patchwork)
```

```r
######## set paths
  # observation cycle inStrain profiles
	data_path <- "/PREMIX/Analyses/Data/"
	data_file <- "observation_data.txt"

######## import data
  # strain summary
  ss <- read_tsv(paste0(data_path, "/", data_file))
  ss$sample <- gsub("-", ".", ss$sample)


  days_file <- read_csv(paste0(data_path,"/","visit_day_counts.csv") %>% 
    select(-c(ICF:lastv_delta_C1D01))
  
  colnames(days_file) <- gsub("_rel_FMT1", "", colnames(days_file))
  
  days_file <- days_file %>%     
    pivot_longer(cols = -ID,
                 names_to = "Visit",
                 values_to = "Days from FMT1")
  
  # metadata
  md <- read_csv(paste0(data_path,"/",stable_metadata.csv")

  # merge dates and metadata
  md <- left_join(md, days_file, by=c("ID", "Visit"))
  
  
########## join data to plot
  ss_sub <- ss %>% select(sample:breadth)
  
  ss_md <- left_join(ss_sub,
                     md,
                     by=c("sample"="Sample"))

```

```r

observation_ids <- c("PM03",
                     "PM05",
                     "PM07",
                     "PM08",
                     "PM12")

label_colors    <- scale_color_manual(
                              breaks = c("PM03-K4",
                                         "PM05-E1",
                                         "PM12-E1",
                                         "PM08-E1",
                                         "PM07-E2",
                                         "PM07-E3"
                                         ),
                              values = c(
                                         "orange",
                                         "orange",
                                         "orange",
                                         "orange",
                                         "darkgrey",
                                         "orange")
                            )


# loop plots
  
    plotlist <- vector("list", length = 2*length(observation_ids))
    patchlist <- vector("list", length = length(observation_ids))
    j = 1

    for(i in observation_ids){
      
      print(glue("  - starting {i}"))
      
      breadth_plot <- ss_md %>% 
                        filter(ID == i) %>% 
                        ggplot(aes( x = `Days from FMT1`,
                                    y = breadth,
                                    # color = genome)) +
                                    color = label)) +
                        geom_line(size=1) +
                        geom_point(size=3) +
                        # geom_line() +
                        # geom_point() +
                        geom_hline(yintercept = 0.5,
                                   linetype = "dashed",
                                   color = "red") +
                        ylim(0, 1) +
                        labs(title = glue("{i}")) +
                        label_colors +
                        theme_classic() +
                      guides(color=guide_legend(ncol=1))
      
      plotlist[[j]] <- breadth_plot
      
      cov_plot <- ss_md %>% 
                      filter(ID == i) %>% 
                      ggplot(aes( x = `Days from FMT1`,
                                  y = coverage,
                                    # color = genome)) +
                                    color = label)) +
                        geom_line(size=1) +
                        geom_point(size=3) +
                        # geom_line() +
                        # geom_point() +
                      ylim(0, 45) +
                      labs(y = "depth") +
                      label_colors +
                      # theme(legend.position = "none") +
                      theme_classic() +
                      guides(color=guide_legend(ncol=1))
      
      patchlist[[i]] <- breadth_plot / cov_plot  + 
            plot_layout(guides = "collect") & theme(legend.position = "bottom",
                                                    legend.title = element_blank())

      j <- j+1

    }


    wrap_plots(patchlist[observation_ids])
    
```

## Time to event plots

We drew heavily on the [excellent tutorial by Emily Zabor](https://www.emilyzabor.com/tutorials/survival_analysis_in_r_tutorial.html) and the R packages survival and survminer.

```r
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

```r

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

```r

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

```r

  # Time to MDRO decolonization
  survdiff(Surv(tt_MDRO_negative, 
                MDRO_negative_status) ~ Randomization, 
           data = tte)

  # Time to MDRO infection
  survdiff(Surv(tt_MDRO_infection,
                MDRO_infection_status) ~ Group, 
           data = tte)  
  
```


## Heatmaps

```r
knitr::opts_chunk$set(echo = TRUE)

library(readr)
library(vegan)
library(tidyverse)
library(viridis)
library(ggpubr)
library(ggsci)
library(ggtext)
library(glue)
library(MEP)
library(wesanderson)
library(pheatmap)
library(stringr)
```

```r

# prep column annotation dataframe

c_annotation <- data.frame(md$Exposure,
                           as.factor(md$`MDRO Status`))
    rownames(c_annotation) <- md$Sample
    colnames(c_annotation) <- c("Exposure",
                                "MDRO Status")
    
# prep row annotation dataframe
r_annotation <- data.frame(quality$Completeness,
                           quality$Contamination,
                           quality$Quality,
                           quality$fastani_ani)
    rownames(r_annotation) <- species_list
    colnames(r_annotation) <- c("MAG Completeness",
                                "MAG Contamination",
                                "MAG Quality Score",
                                "ANI with Reference")
    
# define annotation colors
meta_colors <- list(
          Exposure=c(Donor="#B6854D",
                 FMT="#79402E",
                 None="#D9D0D3",
                 Prep="#9986A5"),
          `MDRO Status`=c(Negative="#46ACC8",
                  Positive="#E58601")
          )

```

```r
# define heatmap function
	
heater <- function(df, legend=TRUE, 
                   matrix_type="breadth",
                   ID=NULL) {
  
            # plotting parameters for relative abundance matrices
            if(legend==TRUE & matrix_type=="rela"){
              print(
               pheatmap(log(df + 1),          # log transform
               annotation_col=c_annotation,
               # annotation_col=glue("can_{ID}"),
               annotation_row=r_annotation,
               annotation_colors=meta_colors,
               cluster_cols = FALSE,
               # cluster_rows = FALSE,
               color=viridis(5),
               # color=magma(5),
               angle_col=45,
               # labels_row = as.expression(newnames),
               scale="row"
               ))
              }
            if(legend==FALSE & matrix_type=="rela"){
              print(
               pheatmap(log(df + 1),          # log transform
               annotation_col=c_annotation,
               # annotation_col=glue("can_{ID}"),
               # annotation_row=r_annotation,
               annotation_colors=meta_colors,
               cluster_cols = FALSE,
               # cluster_rows = FALSE,
               color=viridis(5),
               # color=magma(5),
               angle_col=45,
               # labels_row = as.expression(newnames),
               scale="row",
               annotation_legend=FALSE,
               # legend=FALSE
               ))
            }
              
            # separate plotting parameters for breadth matrices
            if(legend==TRUE & matrix_type=="breadth"){
              print(
               pheatmap(df,           # no log transform
               annotation_col=c_annotation,
               # annotation_col=glue("can_{ID}"),
               annotation_row=r_annotation,
               annotation_colors=meta_colors,
               cluster_cols = FALSE,
               color=viridis(5),
               angle_col=45,
               # labels_row = as.expression(newnames)
               ))
            }
            if(legend==FALSE & matrix_type=="breadth"){
              print(
               pheatmap(df,           # no log transform
               annotation_col=c_annotation,
               # annotation_col=glue("can_{ID}"),
               annotation_row=r_annotation,
               annotation_colors=meta_colors,
               cluster_cols = FALSE,
               color=viridis(5),
               angle_col=45,
               annotation_legend=FALSE,
               # labels_row = as.expression(newnames)
               # legend=FALSE
               ))                  
            }
        }

```
