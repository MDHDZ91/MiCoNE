process flashweave {
    label 'flashweave'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file(otu_file), file('*_network.gml'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'flashweave' in params.network_inference.correlation['selection']
    script:
        meta.network_inference = 'flashweave'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.network_inference.direct['flashweave']['ncpus']
        sensitive = params.network_inference.direct['flashweave']['sensitive']
        heterogeneous = params.network_inference.direct['flashweave']['heterogeneous']
        fdr_correction = params.network_inference.direct['flashweave']['fdr_correction']
        template 'network_inference/direct/flashweave.jl'
}