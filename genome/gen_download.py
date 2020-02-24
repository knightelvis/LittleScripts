from ftplib import FTP
import os
import sys

prefix = 'ftp://ftp.1000genomes.ebi.ac.uk'

with FTP('ftp.1000genomes.ebi.ac.uk') as ftp:
    msg = ftp.login()
    print(msg)
    if not 'success' in msg:
        sys.exit("login unsuccessfully")

    base_path = '/vol1/ftp/data_collections/1000_genomes_project/data'
    ftp.cwd(base_path)
    race_files = ftp.nlst() # files is ['ACB', 'ASW', 'BEB', 'CDX', 'CEU', 'CHB', 'CHS', 'CLM', 'ESN', 'FIN', 'GBR', 'GIH', 'GWD', 'IBS', 'ITU', 'JPT', 'KHV', 'LWK', 'MSL', 'MXL', 'PEL', 'PJL', 'PUR', 'STU', 'TSI', 'YRI']
    print("Total races:" + ",".join(race_files))

    with open('output.txt', 'w') as f:
        for r in race_files:
            # TODO remove
            if r == 'ACB':
                continue

            second_level_path = os.path.join(base_path,r)
            ftp.cwd(second_level_path) # currently in 'data/ACB/'
            individual_files = ftp.nlst() # ['HG01879'...]

            for i in individual_files:
                third_level_path = os.path.join(second_level_path, i)
                ftp.cwd(third_level_path)
                alignments = ftp.nlst()
                if not 'alignment' in alignments:
                    continue
                third_level_path = os.path.join(third_level_path,'alignment')
                target_files = ftp.nlst(third_level_path) # *.bas, *.cram ...

                for t in target_files:
                    if t.endswith('.cram'):
                        output_file = os.path.join(third_level_path,t)
                        line = prefix + output_file + '\n'
                        f.write(line)
                        print(line)

