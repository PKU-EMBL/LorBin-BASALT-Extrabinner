# LorBin-BASALT-Extrabinner

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13864645.svg)](https://doi.org/10.5281/zenodo.13864645)

This is an in-house version of the LorBin implementation for BASALT Extrabinner.

GitHub repository for the manuscript "LorBin: Efficient binning of long-read metagenomes by multiscale adaptive clustering and evaluation".
The code is also citable by obtaining a DOI for the GitHub repository in order to provide a permanent reference to the version of the code used in this study and improve reproducibility (https://doi.org/10.5281/zenodo.13864645).

- [Overview](#overview)
- [System Requirements](#requirements)
- [Installation](#install)
- [A test dataset to demo LorBin](#demo)
- [Preprocessing](#preprocessing)
- [How to run LorBin](#runlorbin)
- [References](#references)
- [License](#license)

## <a name="overview"></a>Overview

LorBin is a deep learning-based binner suitable for contigs assembled from long reads. The framework of LorBin is mainly divided into the following steps: 1) VAE embedding: computes the k-mer frequencies and abundance and uses a self-supervised variational autoencoder to extract the embedded features; 2) first-stage clustering (clustering): uses the multiscale adaptive DBSCAN with a clustering bin quality model to generate bins and then uses a reclustering decision model to determine whether the bins are retained; 3) second-stage clustering (reclustering): generates bins in a similar way as the first-stage clustering by multiscale adaptive BIRCH using contigs failed to be clustered; and 4) bin pooling: pools the bins of the two stages as the final binning result.

## <a name="requirements"></a>System Requirements

In-house version LorBin is developed in Python 3.12 with modules and external tools.

### Hardware requirements

In-house version LorBin requires only a standard computer with enough RAM to support the in-memory operations.

### OS requirements

In-house version LorBin is supported and tested in Linux systems.

### Required dependencies

Python modules:

- biopython=1.85
- torch=2.5.1
- numpy=1.26.4
- pandas=2.2.2
- scikit-learn=1.5.2
- scipy=1.13.1
- joblib=1.4.2

Sequence processing tools:

- minimap2=2.24-r1122
- samtools=1.15.1
- hmmer=3.1b2
- prodigal=2.6.3
- bedtools=2.26.0

## <a name="install"></a>Installation

### Install In-house Version LorBin via pip from BASALT base environment

You can install LorBin from pip. After installing Anaconda (or miniconda), first obtain LorBin and install it based on the BASALT environment:

```bash
git clone https://github.com/PKU-EMBL/LorBin-BASALT-Extrabinner.git
cd LorBin-BASALT-Extrabinner
conda activate basalt_env
# install our in-house version lorbin-basalt-extrabinner
pip install .
```

### Install LorBin via pip from scratch

You can install LorBin from pip. After installing Anaconda (or miniconda), first obtain LorBin:

```bash
git clone https://github.com/PKU-EMBL/LorBin-BASALT-Extrabinner.git
```

Then create a Python 3.12 environment to run LorBin.

The old dependency pins in this repository (for example `biopython=1.78`, `numpy=1.23.3`, `scikit-learn=1.1.2`, and `pytorch=1.11.0`) do not provide Python 3.12 builds, which is why `LibMambaUnsatisfiableError` appears during installation. The environment file now installs the Python 3.12-compatible non-PyTorch dependencies first, and `torch` should be installed separately according to your platform.
For other CUDA versions, please choose the matching install command from the official PyTorch installation guide.

```bash
cd LorBin-BASALT-Extrabinner
conda env create -f lorbin_env.yaml
conda activate lorbin_env

# install torch separately
# Linux CPU only
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
# Linux + CUDA 12.1
# pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
# macOS
# pip install torch==2.5.1

# install our in-house version lorbin-basalt-extrabinner
pip install .
```

If installing the environment through the configuration file is too slow, or you need an environment that is more suitable for your hardware, you can install it step by step with Python 3.12.

```bash
conda create -n lorbin_env -c conda-forge -c bioconda -c defaults python=3.12 minimap2 hmmer prodigal samtools bedtools pip
conda activate lorbin_env

pip install biopython==1.85 numpy==1.26.4 pandas==2.2.2 scikit-learn==1.5.2 scipy==1.13.1 joblib==1.4.2

# CPU Only
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
# Linux + CUDA 12.1
# pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
# macOS
# pip install torch==2.5.1

pip install .
```

## <a name="demo"></a>A test dataset to demo LorBin

We provide a small dataset to demo and test the software. The contigs were assembled by hifiasm.
The inputs for LorBin include contigs and BAM files. You can get a test dataset at https://zenodo.org/records/13883404.

Run LorBin on the test dataset:

```bash
LorBin bin --fa test/test.fna -b test.sort.bam -o test_o
```

## <a name="preprocessing"></a>Preprocessing

The preprocessing steps aim to obtain a single FASTA file and generate bam files as input to our program.

### Concatenate the input contigs to a single FASTA file

If you have several FASTA files and want to bin them at once, you can use the `concat` subcommand to concatenate the input contigs to a single FASTA file.

```bash
LorBin concat -fa test1.fna test2.fna -o test.fna
```

Your contig headers must be unique. Then, `concat` will use '-' to connect the sample index and contigs header.

### Generate bam files

```bash
minimap2 -a test/test.fna test/test1_raw.fq | samtools view -h -b -S | samtools view -b -F 4 | samtools sort -@ 20 > test1.mapped.sorted.bam
minimap2 -a test/test.fna test/test2_raw.fq | samtools view -h -b -S | samtools view -b -F 4 | samtools sort -@ 20 > test2.mapped.sorted.bam
```

## <a name="runlorbin"></a>How to run LorBin

### Run LorBin

#### Activate the environment

```bash
conda activate lorbin_env
```

#### Binning

You can use subcommand 'bin' to bin the contigs.

```bash
LorBin bin -o outputdir -fa test.fna -b test1.mapped.sorted.bam test2.mapped.sorted.bam --multi
```

If you only want to use LorBin in single mode,

```bash
LorBin bin -o outputdir -fa test.fna -b test.mapped.sorted.bam
```

```text
usage: LorBin bin [-h] -o OUTPUT -fa FASTA [--bin_length BIN_LENGTH] -b BAM [BAM ...] [--num_process NUM_PROCESS] [--evaluation EVALUATION] [-a AKEEP] [--multi]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (will be created if non-existent)
  -fa FASTA, --fasta FASTA
                        Path to the input fasta file.
  --bin_length BIN_LENGTH
                        Minimum bin size in bps (Default: 80000)
  -b BAM [BAM ...], --bam BAM [BAM ...]
                        Path to the input BAM(.bam) file.
  --num_process NUM_PROCESS
                        Number of threads used (default: 10)
  --evaluation EVALUATION
                        Evaluation model used(no_markers, markers110, markers35, default: no_markers)
  -a AKEEP, --akeep AKEEP
                        The cut-off parameters of re-clustering decision model(0~1, default:0.6)
  --multi               Cluster uses more samples
```

### Only generate data

If you only need the kmer and abundance data, you can use subcommand 'generate_data'.

```bash
LorBin generate_data -o outputdir -fa path_to_all_contigs -b test1.mapped.sorted.bam test2.mapped.sorted.bam
```

```text
usage: LorBin generate_data [-h] -o OUTPUT -fa FASTA [--bin_length BIN_LENGTH] -b BAM [BAM ...] [--num_process NUM_PROCESS]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (will be created if non-existent)
  -fa FASTA, --fasta FASTA
                        Path to the input fasta file.
  --bin_length BIN_LENGTH
                        Minimum bin size in bps (Default: 80000)
  -b BAM [BAM ...], --bam BAM [BAM ...]
                        Path to the input BAM(.bam) file.
  --num_process NUM_PROCESS
                        Number of threads used (default: 10)
```

If you want to train your model more finely, you can use subcommand 'train'.

```bash
LorBin train --data test/data.csv -o outputdir
```

```text
usage: LorBin train [-h] --data DATA -o OUTPUT [--epoch EPOCH] [--lrate LRATE] [--batch_size BATCH_SIZE] [--batchsteps BATCHSTEPS [BATCHSTEPS ...]]

options:
  -h, --help            show this help message and exit
  --data DATA           The path of training data
  -o OUTPUT, --output OUTPUT
                        Output directory (will be created if non-existent)
  --epoch EPOCH, -n EPOCH
                        training epoch (default: 300)
  --lrate LRATE, -l LRATE
                        learning rate (default: 0.001)
  --batch_size BATCH_SIZE
                        batch size (default: 64)
  --batchsteps BATCHSTEPS [BATCHSTEPS ...]
                        batchsteps (default: 30, 60, 120)
```

### Only cluster used embedding.csv

If you have the embedded features of contigs and only want to use the two-stage clustering to bin, you can use subcommand 'cluster' to get the binning result. Note that the embedded features should be stored in .csv files and the index should be the contigs header.

```bash
LorBin cluster -o outputdir -fa path_to_all_contigs --embedding path/embedding.csv
```

```text
usage: LorBin cluster [-h] -o OUTPUT -fa FASTA [--bin_length BIN_LENGTH] [--evaluation EVALUATION] [-a AKEEP] [--multi] --embeddingdir EMBEDDINGDIR [--num_process NUM_PROCESS]

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (will be created if non-existent)
  -fa FASTA, --fasta FASTA
                        Path to the input fasta file.
  --bin_length BIN_LENGTH
                        Minimum bin size in bps (Default: 80000)
  --evaluation EVALUATION
                        Evaluation model used(no_markers, markers110, markers35, default: no_markers)
  -a AKEEP, --akeep AKEEP
                        The cut-off parameters of re-clustering decision model(0~1, default:0.6)
  --multi               Cluster uses more samples
  --embeddingdir EMBEDDINGDIR, -e EMBEDDINGDIR
                        The path of embedding csv file used in clustering
  --num_process NUM_PROCESS
                        Number of threads used (default: 10)
```

## <a name="references"></a>References

[1] Pan, S., Zhao, X.-M. & Coelho, L. P. SemiBin2: self-supervised contrastive learning leads to better MAGs for short- and long-read sequencing. Bioinformatics 39, i21–i29 (2023).

[2] Nissen, J. N. et al. Improved metagenome binning and assembly using deep variational autoencoders. Nat Biotechnol 39, 555–560 (2021).

[3] Wang, Z. et al. Effective binning of metagenomic contigs using contrastive multi-view representation learning. Nat Commun 15, 585 (2024).

[4] Qiu, Z. et al. BASALT refines binning from metagenomic data and increases resolution of genome-resolved metagenomic analysis. Nature Communications 15, 2179 (2024).

## <a name="license"></a>License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
