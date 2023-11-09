def chipexo_filepath(instance, filename):
    tf = instance.tf
    chipexo_id = instance.chipexo_id
    return f'chipexo/{tf.locus_tag}_{chipexo_id}.tsv.gz'