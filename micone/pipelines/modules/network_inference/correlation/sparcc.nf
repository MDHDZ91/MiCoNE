process sparcc {
    label 'sparcc'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(bootstrap_files), file(obsmeta_file), file(samplemeta_file), file(children_file)
    output:
        tuple val(meta), file(otu_file), file('*_corr.tsv'), file('*_corr.boot'), file(obsmeta_file), file(samplemeta_file), file(children_file)
    when:
        "sparcc" in params.network_inference.correlation['selection']
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.network_inference.correlation['sparcc']['ncpus']
        iterations = params.network_inference.correlation['sparcc']['iterations']
        template 'network_inference/correlation/sparcc.sh'
}
