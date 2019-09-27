        with open('asrs_report.txt', 'w') as f:
            f.write('\nFrom : {}  To : {}\n'.format(formatted_date1, formatted_date2))
            f.write("-------------------------------------------------------------------------------------------\n")
            f.write("-------------------------------------------------------------------------------------------\n\n")
            for key, value in data.items():
                x = value.split(';')
                f.write('TID         : %s\nNAME        : %s\nDOB         : %s\nID          : %s\nCOMPANY     : %s\nVALIDITY    : %s\nSTORED DATE : %s  |  RETRIEVED DATE : %s \n\n' $
                f.write("-------------------------------------------------------------------------------------------\n\n")

        os.system('enscript -b "ASRS REPORT" -G -p output.ps asrs_report.txt')
        os.system('ps2pdf output.ps asrs_report.pdf')

