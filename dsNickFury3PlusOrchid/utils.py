import pandas as pd

import azure.storage.table
import azure.storage.blob


def get_table_service(azure_account):
    try:
        accountkey_file = open('azureTable.apikey', 'r')
    except FileNotFoundError:
        raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
    accountkey = accountkey_file.read().strip()
    accountkey_file.close()
    return azure.storage.table.TableService(account_name=azure_account, account_key=accountkey)


def get_blob_service(azure_account):
    try:
        accountkey_file = open('azureTable.apikey', 'r')
    except FileNotFoundError:
        raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
    accountkey = accountkey_file.read().strip()
    accountkey_file.close()
    return azure.storage.blob.BlockBlobService(account_name=azure_account, account_key=accountkey)


def read_dsnf(filename):
    # columns = ['chromosome', 'start', 'end', 'gene', 'ontarget', 'offtarget', 'strand', 'mismatches']
    columns = ['ontarget', 'mismatches', 'chromosome', 'start', 'end', 'gene', 'offtarget', 'strand']
    data = {col: [] for col in columns}
    with open(filename, "r") as f:
        for line in f:
            if line.startswith('Too many mismatches'):
                continue
            if '\t' not in line:
                ontarget = line.replace('_', '').replace('\n', '')
            if line.startswith('\tMismatches'):
                mismatches = int(line.split(" ")[1])
            if line.startswith("\t\t"):
                data['ontarget'].append(ontarget)
                data['mismatches'].append(mismatches)

                items = line.strip("\n").replace(',', ';').split("\t")
                assert len(items) == 11

                data['chromosome'].append(items[2])
                data['start'].append(int(items[3]))
                data['end'].append(int(items[4]))

                gene_offtarget = items[5].split('/')
                data['gene'].append(gene_offtarget[0].replace(' ', ''))
                data['offtarget'].append(gene_offtarget[1].replace('_', ''))

                # data['score'].append(float(items[6]))
                data['strand'].append(items[7])
                # data['rgb'].append(items[10])

    return pd.DataFrame(data, columns=columns).sort_values(by=['ontarget', 'mismatches', 'chromosome', 'start'])

