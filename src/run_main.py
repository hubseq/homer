#
# run_main
#
# Template wrapper script that runs a command-line program within a Docker container.
#
import os, subprocess, sys
from datetime import datetime
sys.path.append('global_utils/src/')
# sys.path.append('../../global_utils/src/')
import module_utils


def runOtherPre( input_dir, output_dir, run_json ):
    """ This function is used to run any other commands BEFORE the main program has run.
    run_json has most of what you might need to run other commands, and has the following structure:

    run_json = {'module': module_name, 'local_input_dir': <LOCAL_INPUT_DIR>, 'local_output_dir': <LOCAL_OUT_DIR>, \
                'docker_entry_dir': DOCKER_DIR, \
		'remote_input_dir': remote_input_directory, 'remote_output_dir': remote_output_directory, \
                'program_arguments': program_arguments, 'run_arguments': run_arguments_json, \
                'module_instance_json': module_instance_json}

    LOCAL_INPUT_DIR has any downloaded files. LOCAL_OUT_DIR has any output data or log files that will be uploaded.

    If you are not running any other commands or post-processing, then leave this function blank.
    """
    # first need to move genome files to homer directory - hopefully this works
    # subprocess.call(['mv','{}/data'.format(run_json['local_input_dir'].rstrip('/')), '{}/'.format(run_json['docker_entry_dir'].rstrip('/'))])
    # first need to configure Homer
    subprocess.call(['perl','{}/homer/configureHomer.pl'.format(run_json['docker_entry_dir'].rstrip('/')),'-install'])
    # need to run makeTagDirectory - creates inputs for other homer commands
    print('First running makeTagDirectory...')
    print('RUN_JSON: '+str(run_json))
    pargs_full = run_json['program_arguments']
    rargs = run_json['module_instance_json']
    pargs_from_user = module_utils.getRunProgramArguments( rargs )
    if 'treatment' not in os.listdir(run_json['local_input_dir']):
        os.mkdir('{}/treatment'.format(run_json['local_input_dir'].rstrip('/')))
    if 'control' not in os.listdir(run_json['local_input_dir']):        
        os.mkdir('{}/control'.format(run_json['local_input_dir'].rstrip('/')))             
    runMakeTagDirectoryArgs_T = 'makeTagDirectory {}/treatment {} -genome {}'.format(run_json['local_input_dir'].rstrip('/'), \
                                                                             module_utils.getArgument(pargs_full, '-t'), \
                                                                             module_utils.getArgument(pargs_full, '-genome'))
    module_utils.runProgram( runMakeTagDirectoryArgs_T )
    runMakeTagDirectoryArgs_C = 'makeTagDirectory {}/control {} -genome {}'.format(run_json['local_input_dir'].rstrip('/'), \
                                                                           module_utils.getArgument(pargs_full, '-c'), \
                                                                           module_utils.getArgument(pargs_full, '-genome'))
    module_utils.runProgram( runMakeTagDirectoryArgs_C )
    # then create program arguments for running homer peak finding
    run_json['program_arguments'] = '{} {}/treatment -o {} -i {}/control {}'.format(module_utils.getSubprogram(rargs), \
                                                                                    run_json['local_input_dir'].rstrip('/'), \
                                                                                    run_json['local_output_file'], \
                                                                                    run_json['local_input_dir'].rstrip('/'), \
                                                                                    pargs_from_user)
    return run_json


def runOtherPost( input_dir, output_dir, run_json ):
    """ This function is used to run any other commands AFTER the main program has run.
    run_json has most of what you might need to run other commands, and has the structure shown above.

    If you are not running any other commands or pre-processing, then leave this function blank.
    """
    return run_json


def runMain():
    # time the duration of module container run
    run_start = datetime.now()
    print('Container running...')
    
    # initialize program run
    run_json = module_utils.initProgram()
    
    # do any pre-processing (specific to module)
    run_json = runOtherPre( run_json['local_input_dir'], run_json['local_output_dir'], run_json )
    
    # run main program
    module_utils.runProgram( run_json['program_arguments'], run_json['local_output_file'] )
    
    # do any post-processing
    run_json = runOtherPost( run_json['local_input_dir'], run_json['local_output_dir'], run_json )

    # create run log that includes program run duration
    run_end = datetime.now()
    run_json['module_run_duration'] = str(run_end - run_start)
    module_utils.logRun( run_json, run_json['local_output_dir'] )
    
    # upload output data files
    module_utils.uploadOutput( run_json['local_output_dir'], run_json['remote_output_dir'] )
    print('DONE!')
    
    return


if __name__ == '__main__':
    runMain()
