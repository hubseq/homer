import json
MODULE = 'homer'

mi_template_json = {'module_version': '00.00.00', 'program_name': 'homer', 'program_subname': 'findPeaks', 'program_version': '4.11', 'compute': {'environment': 'aws', 'language': 'Python', 'language_version': '3.7', 'vcpus': 2, 'memory': 6000}, 'program_arguments': '', 'program_input': [{'input_type': 'file', 'input_file_type': 'SAM', 'input_position': -1, 'input_prefix': '-t,-c'}], 'program_output': [{'output_type': 'file', 'output_file_type': 'TXT', 'output_position': -2, 'output_prefix': '-o'}], 'alternate_inputs': [{'input_type': 'file', 'input_file_type': 'FASTA', 'input_position': -3, 'input_prefix': '-genome'}], 'alternate_outputs': [], 'defaults': {'alternate_inputs': 's3://npipublicinternal/test/genomes/mm10/mm10.fasta', 'output_file': '<SAMPLE_ID>.homer.txt'}}
with open(MODULE+'.template.json','w') as fout:
    json.dump(mi_template_json, fout)

io_json = {'input': ['s3://npipublicinternal/test/chipseq/run_test1/bowtie2/mouse_heart_H3K4me3_rep1.bowtie2.sam', 's3://npipublicinternal/test/chipseq/run_test1/bowtie2/mouse_control_chipseq_rep1.bowtie2.sam'], 'output': ['s3://npipublicinternal/test/chipseq/run_test1/homer/mouse_heart_H3K4me3_rep1.homer.txt'], 'alternate_inputs': ['s3://npipublicinternal/test/genomes/mm10/mm10.fasta'], 'alternate_outputs': [], 'program_arguments': '-style histone', 'sample_id': MODULE+'_test'}
with open(MODULE+'.test.io.json','w') as fout:
    json.dump(io_json, fout)

io_dryrun_json = io_json
io_dryrun_json['dryrun'] = ''
with open(MODULE+'.dryrun_test.io.json','w') as fout:
    json.dump(io_dryrun_json, fout)

io_dryrun_local_json = {'input': ['/Users/jerry/icloud/Documents/hubseq/homer/test/mouse_heart_H3K4me3_rep1.bowtie2.sam', '/Users/jerry/icloud/Documents/hubseq/homer/test/mouse_control_chipseq_rep1.bowtie2.sam'], 'output': ['/Users/jerry/icloud/Documents/hubseq/homer/test/mouse_heart_H3K4me3_rep1.homer.txt'], 'alternate_inputs': ['/Users/jerry/icloud/Documents/hubseq/genomes/mm10/mm10.fasta'], 'alternate_outputs': [], 'program_arguments': '', 'sample_id': MODULE+'_test', 'dryrun': ''}

with open(MODULE+'.dryrun_local_test.io.json','w') as fout:
    json.dump(io_dryrun_local_json, fout)

# job info test JSONs
job_json = {"container_overrides": {"command": ["--module_name", MODULE, "--run_arguments", "s3://npipublicinternal/test/modules/"+MODULE+"/job/"+MODULE+".test.job.json", "--working_dir", "/home/"]}, "jobqueue": "batch_scratch_queue", "jobname": "job_"+MODULE+"_test"}
with open(MODULE+'.test.job.json','w') as fout:
    json.dump(io_json, fout)

