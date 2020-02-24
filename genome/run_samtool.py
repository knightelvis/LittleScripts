import subprocess

sam_cmd = 'samtools view -h {ftp_file} chrX: > {output}.bam'
with open('output_test.txt', 'r') as f:
    for line in f:
        # print(f, end='')
        ftp_file = line.strip()
        output = ftp_file.split('/')[-1]
        ready_to_run = sam_cmd.format(ftp_file=ftp_file, output=output)
        print(ready_to_run)
        out = subprocess.run(['ls > test.log'], shell=True,)