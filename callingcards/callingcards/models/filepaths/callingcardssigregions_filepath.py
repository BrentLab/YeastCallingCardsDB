def callingcardssigregions_filepath(instance, filename):
    ccid = instance.callingcards_id
    source = instance.promoterregions_source
    return f'callingcards/{source}/{ccid}.tsv.gz'
