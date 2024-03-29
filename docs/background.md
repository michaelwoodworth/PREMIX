# Background

Fecal microbiota transplantation (FMT) has become an important approach to understand the functions of host-associated microbial communities. In many cases, the taxa in these communities are challenging to culture with routine microbiology methods. FMT allows investigation of phenotypic effects of transfer of whole (or at least plurality of members of) microbial communities. Next-generation sequencing approaches have greatly enhanced our ability to then identify taxa and their gene-predicted functions associated with responses to treatment with FMT. PREMIX was a randomized, controlled trial of FMT for treatment of multi-drug resistant organism (MDRO) colonization in renal transplant recipients.

This page outlines the naming convention and details of how participants flowed through the PREMIX trial for clarity and analytic context.

---

### 1 - Naming convention

In the PREMIX study, **consented participants** were assigned sequential unique identifiers as **PM--**. Participants were found to not have an MDRO on screening stool culture after consent or were unable to complete a visit cycle as specified in the protocol were not included in analyses or in the publicly available datasets. **Consented stool donors** were similarly assigned sequential unique identifiers as **SD--**, however a single donor was used for all treatments in PREMIX.

**Visits** were conducted in 36-day blocks in one of three visit cycles (i.e. 0, 1, 2). Cycle 0 was an observation visit cycle without administration of FMT. Cycles 1 and 2 were FMT visit cycles. Visits were in person on Days 1, 15, and 36, with an additional stool specimen collected on Day 2. Visits were coded by cycle and day as C-D-- (e.g. C1D36, C0D15).

### 2 - Trial Schema

Participants in the PREMIX study were renal transplant recipients with a history of one of four target multi-drug resistant organism (MDRO) infections. These included: ESBL (extended-spectrum beta-lactamase-producing *Enterobacterales*, defined as any *Enterobacterales* isolate with a Ceftriaxone MIC greater than or equal to 8), CRE (carbapenem-resistant *Enterobacterales*, defined as any *Enterobacterales* isolate that was non-susceptible to any carbapenem, including ertapenem), VRE (vancomycin-resistant *Enterococcus*, defined as any *Enterococcus* isolate that was not susceptible to vancomycin), and MDRP (multi-drug resistant *Pseudomonas*, defined as an isolate resistant to two or more antibiotic classes).

![Schema for PREMIX trial](../assets/21.12.01-PREMIX-schema.png)

### 3 - Linux Command Line Tools and High-Performance Cluster Computing

Almost all of the tools used in these analyses can be installed with conda. We typically create a new conda environment for each tool, named as the tool (occasionally including the tool version in the conda environment name if there are frequent/conflicting updates), and install the tool with conda.

For shorter wall times, we use a high-performance computing cluster to complete these steps in parallel. For the most part, this was done on the PACE computing cluster at Georgia Tech. Most tools had an associated [launcher bash script](../assets/Launch_template.sh) and [pbs script](../assets/pbs_template.sh), which submitted these jobs as an array. For simplicity, this repository just documents the tools, commands, arguments/parameters, and input/output files used within each tool pbs script.
