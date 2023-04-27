"""part of an unimplemented openai suggestion on streaming"""
import pandas as pd
import io
import gzip
from django.http import StreamingHttpResponse
# note -- address the Gzipping. this had a mixin that is deprecated, 
# needs checking

class DataFrameIterator(object):
    """
    An iterator that yields the contents of a pandas dataframe as chunks of bytes.
    """
    def __init__(self, df):
        self.buffer = io.StringIO()
        self.df = df
    
    def __iter__(self):
        for row in self.df.itertuples(index=False):
            self.buffer.write('\t'.join([str(val) for val in row]) + '\n')
            data = self.buffer.getvalue().encode('utf-8')
            self.buffer.truncate(0)
            self.buffer.seek(0)
            yield data


class GzipCsvResponse(StreamingHttpResponse):
    """
    A compressed CSV response object that streams the contents of a pandas dataframe.
    """
    def __init__(self, df, filename, *args, **kwargs):
        content_type = 'text/csv'
        content_disposition = f'attachment; filename="{filename}.csv.gz"'
        iterator = DataFrameIterator(df)
        super().__init__(iterator, content_type=content_type,
                         content_disposition=content_disposition,
                         *args, **kwargs)


def serve_compressed_dataframe(request, df, filename):
    # Concatenate dataframes
    df_concatenated = pd.concat(df, ignore_index=True)
    # Compress the dataframe
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb') as gz:
        df_concatenated.to_csv(gz, index=False, encoding='utf-8')
    # Return the response
    return GzipCsvResponse(df=df_concatenated, filename=filename)