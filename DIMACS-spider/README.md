# DIMACS data spider

This is a data spider for [9th DIMACS Implementation Challenge - Shortest Paths](http://www.diag.uniroma1.it//challenge9/download.shtml#benchmark)

The scripts are taken from the [benchmarks compressed archive file](http://www.diag.uniroma1.it//challenge9/code/ch9-1.1.tar.gz).
But there are several bugs in the script so that it cannot run anymore. So I fixed them and make this new version public.

## HOW TO RUN
``` bash
perl genUSA-road-d.gr.pl
perl genUSA-road-t.gr.pl
```

the data will be downloaded into the `dataset` directory.
The specification for the downloaded files are given on [the format page](http://www.diag.uniroma1.it//challenge9/format.shtml).
