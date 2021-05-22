process make_network {
    label 'micone'
    tag "$id"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), val(level), file(corr_file), file(pval_file), file(obsdata_file), file(childrenmap_file)
    output:
        tuple val(id), file('*_network.json')
    script:
        template 'network_inference/network/make_network.py'
}