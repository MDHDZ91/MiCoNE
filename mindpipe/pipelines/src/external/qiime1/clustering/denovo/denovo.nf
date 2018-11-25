#!/usr/bin/env nextflow

// Initialize variables
def sequences = params.sequences
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters)
def ncpus = params.ncpus // "-a -O $ncpus"

// Channels
Channel
    .fromPath(sequences)
    .ifEmpty { exit 1, "16S sequences not found" }
    .set { sequence_data_chnl }


// Processes

// Step1: Pick de novo otus
process pick_de_novo_otus {
    tag "de_novo"
    publishDir "${output_dir}/denovo_picking"

    input:
    val sequence_files from sequence_data_chnl.collect()

    output:
    set file('otu_table.biom'),
        file('rep_set.tre'),
        file('rep_set/seqs_rep_set.{fasta,fna}'),
        file('log*.txt') into output_chnl

    script:
    sequence_list = sequence_files.join(',')
    {{ pick_de_novo_otus }}
}