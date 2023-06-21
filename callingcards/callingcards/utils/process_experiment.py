from typing import Union
import logging
import os
import gzip
import io
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pandas as pd
from callingcards.users.models import User
from ..models import (CallingCardsSig,
                      CCExperiment, HopsSource,
                      BackgroundSource,
                      PromoterRegionsSource)
from .callingcards_with_metrics import callingcards_with_metrics

logger = logging.getLogger(__name__)


def process_experiment(experiment_id,
                       user_id,
                       **kwargs) -> Union[pd.DataFrame, None]:
    """
    Create the CallingCardsSig records for a given experiment.

    :param experiment_id: The ID of the experiment to process.
    :type experiment_id: int
    :param user_id: The ID of the user associated with the experiment.
    :type user_id: int
    :param kwargs: Additional keyword arguments for customization.
    :type kwargs: dict
    :return: The processed result dataframe if successful, None otherwise.
    :rtype: pandas.DataFrame or None
    :raises ValueError: If an error occurs during the processing.
    """

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.error('User with id %s does not exist', user_id)
        return None

    try:
        result_df = callingcards_with_metrics(
            {
                'experiment_id': experiment_id,
                'hops_source': kwargs.get('hops_source', None),
                'background_source': kwargs.get('background_source', None),
                'promoter_source': kwargs.get('promoter_source', None)
            }
        )
    except ValueError as err:
        # Log the error and continue with the next experiment
        logger.error('callingcards_with_metrics failed: %s', err)
        return None

    # Process the result as needed
    grouped = result_df.groupby(['experiment_id',
                                 'hops_source',
                                 'background_source',
                                 'promoter_source'])

    for name, group in grouped:
        logger.debug('processing group: {}'.format(name))
        (experiment_id_tmp, hops_source,
            background_source, promoter_source) = name

        # Compress the dataframe and write it to the buffer
        compressed_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_buffer,
                           mode='wb') as gz:
            group.to_csv(gz, index=False, encoding='utf-8')

        # Reset the buffer's position to the beginning
        compressed_buffer.seek(0)

        # Save the file to Django's default storage
        filepath = os.path.join(
            'analysis',
            CCExperiment.objects.get(pk=experiment_id).batch,
            f'ccexperiment_{experiment_id}',
            f'{hops_source}'
            f'_{background_source}'
            f'_{promoter_source}.csv.gz')

        logger.debug("filepath: %s", filepath)

        default_storage.save(
            filepath,
            ContentFile(compressed_buffer.read()))

        # Close the buffer
        compressed_buffer.close()

        # create the record in the database
        CallingCardsSig.objects.create(
            uploader=user,
            uploadDate=datetime.date.today(),
            modified=datetime.datetime.now(),
            modifiedBy=user,
            experiment=CCExperiment.objects.get(pk=experiment_id),
            hops_source=HopsSource.objects.get(pk=hops_source),
            background_source=BackgroundSource.objects.get(pk=background_source),  # noqa
            promoter_source=PromoterRegionsSource.objects.get(pk=promoter_source),  # noqa
            file=filepath)

    return result_df
