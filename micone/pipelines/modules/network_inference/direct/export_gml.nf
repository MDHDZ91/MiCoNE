process export_gml {
    label 'flashweave'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(network_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'network_inference/direct/export_gml.py'
}
