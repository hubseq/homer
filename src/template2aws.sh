BASEDIR='s3://npipublicinternal/test'
aws s3 cp $1.test.io.json $BASEDIR/modules/$1/io/
aws s3 cp $1.dryrun_test.io.json $BASEDIR/modules/$1/io/
aws s3 cp $1.dryrun_local_test.io.json $BASEDIR/modules/$1/io/
aws s3 cp $1.test.job.json $BASEDIR/modules/$1/job/
aws s3 cp $1.template.json $BASEDIR/templates/
