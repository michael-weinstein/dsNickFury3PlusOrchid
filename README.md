# Elevation-search (aka dsNickFury3)

To perform efficient genomic searches for potential off-targets, we developed
the program dsNickFury. This program can be used to locate every potential
CRISPR/Cas9 target in a genome for a given sgRNA sequence, which can then be
evaluated for on-target efficacy by our previously published model, Azimuth
(Doench et al., Nature Biotechnology 2016), and for off-target effects by
our new predictive model, Elevation (Listgarten et al., Nature Biomedical
Engineering 2018).

See our [**manuscript**](https://doi.org/10.1038/s41551-017-0178-6) or [**official project page**](https://www.microsoft.com/en-us/research/project/crispr/) for more detail.

## Setup

### Directory structure

When you first clone this repo, you will have the following folder structure:

```
dsnickfury/
    README.md
    dsNickFury3PlusOrchid/
    ...
```
### Download data dependencies

**All path names in the instructions assume the current working directory
is the "dsnickfury" directory, i.e. the repo root.**

To search the human (hg38) genome for potential off-target sites, you will also
need to download the indexed genome data, available at the following link:
http://download.microsoft.com/download/8/2/1/821D3094-7997-4B69-B221-573480A412E3/crispr_data.zip

**Warning: the human genome data is large (~22GB)**

Next, make a top-level directory for the data dependencies. Then you'll
need to download the Elevation repository from the GitHub page:

`git clone https://github.com/Microsoft/Elevation.git dependencies/elevation`

Next, use the scripts in the Elevation repo to generate the data dependencies.
The documentation for Elevation will walk you through this.

After generating the data dependencies, your directory structure should look
like this:

```
dsnickfury/
    README.md
    dependencies/
        elevation/
            CRISPR/
            ..
    dsNickFury3PlusOrchid/
        genomes/
        ...
```

### Installation of remaining code dependencies

The following dependencies are needed and should be put in the specified directories:
 * Azimuth 2.0.0 (from the public repo): `git clone https://github.com/MicrosoftResearch/Azimuth.git dependencies/azimuth`

### Installation of Python dependencies

The main Elevation-search program code `dsNickFury3.3.py` runs on Python 3.
Azimuth and Elevation (our on-target and off-target prediction models) run
on Python 2. They will be invoked as sub-processes from Python 3.

Therefore, we need both Python 2 and 3 interpreters available at runtime.

Steps to set this up:

1. Install anaconda2 into the `dsnickfury/dependencies` directory. You can
   do this directly on Linux by running the install script with the `-p`
   option, or on Windows using the graphical installer.

   **All subsequent instructions refer to the anaconda2 installation in the dependencies directory.**

2. Install all Azimuth and Elevation dependencies using pip from the anaconda2
   installation, e.g. `dependencies/anaconda2/bin/pip install X` or a similar command.

3. Create a Python 3 environment using
   `dependencies/anaconda2/bin/conda create -n dsNickFury python=3`
   and install all Python 3 dependencies (everything needed by
   `dsNickFury3.3.py`) using pip from the created environment,
   e.g. `dependencies/anaconda2/envs/dsNickFury/bin/pip install X`.

4. The anaconda2 installation should now contain all third-party Python
   dependencies, as well as Python 2 and Python 3 interpreters.

   You should end up with the following folder structure:

```
dsnickfury
    dependencies
    anaconda2
    elevation
    azimuth
    CRISPR
dsNickFury3PlusOrchid
    genomes
    ...
```

### Path Configuration

Modify the following line in `settings.py` to reflect the location of the
dsNickFury repo.

```
network_root = "/home/jake/repos/"
```

If you followed the directory structure suggested above, the rest of
the locations in `settings.py` should match your setup. At this point,
you should be able to test the installation by running the commands in
the section **Test Commands**.

### Database Dependencies

`ensemblGeneAnalyzer.py` originally depended on Azure, but you can pass the `-f`
flag to write results to stdout (or an output file, using the `-o` flag) instead.

To use Azure for storing the output:

* `pip install azure`

* write API key to `azureTable.apikey`. This is the file that will be accessed for the API key.

##  Test Commands

### Debugging Model (invoke using python 2.7)

    * `python predictionWrapper.py aggregation < test_aggregation.txt`
      (this tests the Elevation aggregation model)

    * `python predictionWrapper.py elevation < test_elevation.txt`
      (this tests the Elevation-score model)

### Debugging dsNickFury (invoke using python 3)

    * `python dsNickFury3.3.py -m search -s CCTCTTTGACATCGTGTCCC_GGG -g HG38 --noElevation`
    (this should return a perfectly matched site in TRPV4, and some other near-matches)

    * `python dsNickFury3.3.py -m search -s TGGGGTGATTATGAGCACCG_AGG -g HG38 -p NGG --endClip 3`
    (this should return a perfectly matched site in CD33, and give the
     Elevation-aggregate score for all of the listed mismatches. These are
     the same parameters that were used to populate the online database, so
     the score should match the score listed online for this guide)

    * `python ensemblGeneAnalyzer.py --ensg ENSG00000105383 -f`
    (this should find all guides that target protein-coding regions in CD33,
     and print a list of them to stdout, which can then be run through
     dsNickFury)

## Usage details

#### About dsNickFury3:

**Purpose**: dsNickFury is a Python3 program to help select guide RNA sequences
for use with any CRISPR/Cas system.  This program can work with any system having
activity sites defined by a guide RNA of some maximum length and some PAM sequence
of fixed length with or without a degenerate sequence.

**How it works**: This program works by identifying all potential activity sites
for any given guide length/PAM sequence combination during its *index* operation.
During *search* operations, a given guide sequence will be searched against the
indexed sites to determine if any are similar enough to be of concern in designing
a CRISPR targeting strategy.  During a *selection* operation, all potential targets
for a system are collected from a sequence (or a list of already-selected targets can
be supplied) and analyzed.  The potential targets will then be sorted by their
predicted specificity and efficiency (in that order).

#### Version history:

*Version 1 (All Shiny and Chrome)*: The original version of this program worked
by creating several small files, each containing several thousand potential CRISPR
targets from the chosen genome.  Sites were stored sequentially, relative to their
genomic locus and every site was matched against the site of interest following a
highly-parallelized map/reduce type of scheme.  This version was forked into a
server/stand-alone and cluster version, with one being optimized for use on a
single system with multiple cores and the other being optimized for use on a
cluster system running an SGE job scheduler.  These versions were later rejoined,
with cluster or stand-alone mode being specified as an argument.

*Version 2 (CRISPR Divided)*: This version's major change was the introduction of
a tree structure to better organize the potential targets.  The indexer now
separates targets into multiple bins depending upon their sequence immediately
prior to the PAM site.  This requires significantly more computational effort
than the previous method of saving them in the order they are found, and will
often result in *index* jobs requiring double or triple the amount of time
required in the previous version.  This organization of sites, however, makes site
*searches* significantly more efficient than the previous version.  Additionally,
this version will not list all potential off-targets during a *selection* run for
potential target sites with with over 100 potential mismatch sites per allowed
mismatch (i.e. with the default setting of 3 mismatches, any site with over 300
potential mismatch sites will show how many potential mismatches it has, but will
not list them specifically unless clobber mode is set).  The changes introduced
in this version have resulted in significantly faster searches and selections
(with some operations seeing a 30-fold improvement in time) and cleaner outputs.

*Version 3 (Orchid Edition)*: This version has multiple changes for massively
scaling-up and running with Microsoft's packages.  This version was designed to
be called iteratively as one "walks" a chromosome or genome to analyze regions of
genomic features.  This version also has built-in connectivity to azure data
storage resources.  This version can now use non-canonical PAM sites (such as NGA
and NAG, among others, for pyogenes cas-9).  To compensate for the potentially
massive increase in data to analyze, the data storage is now in a binary format
with site comparisons being handled in a bit-wise manner instead of standard string
comparison as before.

#### Data storage:

The data are now stored using a binary format.  For a site with a 3 base PAM
sequence, a 20 base guide, and storing up to 4 bases up and downstream, each site
can be stored in 20 bytes.  The final bytes will always be the guide sequence
stored in the 3'-5' orientation in a 2-bit DNA format (A = 00, C = 01, G = 10,
T = 11).  For site comparison, the site to be compared is converted to a 2-bit
format and a binary XOR is carried out between the two sites, with any mismatching
bases returning at least one bit true.
