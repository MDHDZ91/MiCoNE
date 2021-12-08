include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process normalize {
    label 'micone'
    tag "${new_meta.id}:${processing}"
    publishDir "${params.output_dir}/${f[0]}/transform/${module_dir}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
        each rm_sparse_obs
    output:
        tuple val(new_meta), file("*_normalized.biom")
    script:
        new_meta = updateMeta(meta)
        new_meta.id = "${otu_file.baseName}"  // "meta.id_label"
        processing = rm_sparse_obs ? 'on' : 'off'
        new_meta.otu_processing = "normalize(${processing})"
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        module_dir = "${new_meta.otu_processing}"
        directory = "${new_meta.denoise_cluster}-${new_meta.chimera_checking}-${new_meta.tax_assignment}"
        axis = params.otu_processing.transform['normalize']['axis']
        count_thres = params.otu_processing.transform['normalize']['count_thres']
        prevalence_thres = params.otu_processing.transform['normalize']['prevalence_thres']
        abundance_thres = params.otu_processing.transform['normalize']['abundance_thres']
        rm_sparse_samples = params.otu_processing.transform['normalize']['rm_sparse_samples']
        template 'otu_processing/transform/normalize.py'
}
