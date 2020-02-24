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

    with open('output_low.txt', 'w') as f_low, open('output_exo.txt', 'w') as f_exo, open('output_high.txt', 'w') as f_hig:
        for r in race_files:
            second_level_path = os.path.join(base_path,r)
            ftp.cwd(second_level_path)  # currently in 'data/ACB/'
            individual_files = ftp.nlst()  # ['HG01879'...]

            for i in individual_files:
                third_level_path = os.path.join(second_level_path, i)
                ftp.cwd(third_level_path)
                alignments = ftp.nlst()
                for a in alignments:
                    print(a)
                    if a == 'alignment':
                        fourth_level_path = os.path.join(third_level_path, a)
                        target_files = ftp.nlst(fourth_level_path)  # *.bas, *.cram ...

                        for t in target_files:
                            if t.endswith('.cram'):
                                output_file = os.path.join(fourth_level_path, t)
                                line = prefix + output_file + '\n'
                                f_low.write(line)
                                print(line)

                    elif a == 'exome_alignment':
                        fourth_level_path = os.path.join(third_level_path, a)
                        target_files = ftp.nlst(fourth_level_path)  # *.bas, *.cram ...

                        for t in target_files:
                            if t.endswith('.cram'):
                                output_file = os.path.join(fourth_level_path, t)
                                line = prefix + output_file + '\n'
                                f_exo.write(line)
                                print(line)

                    elif a == 'high_cov_alignment':
                        fourth_level_path = os.path.join(third_level_path, a)
                        target_files = ftp.nlst(fourth_level_path)  # *.bas, *.cram ...

                        for t in target_files:
                            if t.endswith('.cram'):
                                output_file = os.path.join(fourth_level_path, t)
                                line = prefix + output_file + '\n'
                                f_hig.write(line)
                                print(line)
                    else:
                        print("###" + a)
