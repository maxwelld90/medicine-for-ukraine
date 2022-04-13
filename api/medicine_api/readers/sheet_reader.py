import zlib
import redis
import pickle
import pygsheets
from django.conf import settings
from medicine_api.models import Sheet
from medicine_api.readers import exceptions
from pygsheets.exceptions import WorksheetNotFound


REDIS_WORKSHEET_SUFFIX = '-WORKSHEET'
REDIS_DATAFRAME_SUFFIX = '-DF'

class SheetReader(object):
    def __init__(self):
        self.__redis_conn = None
        self._worksheets = {}
        self._dataframes = {}
        self._language_data = settings.MEDICINE_LANGUAGE_DATA

        if not hasattr(self, '_data_key'):
            raise NotImplementedError('Missing the _data_key attribute.')
        
        self._data = self.__populate_data()

        if settings.REDIS_ENABLED:
            self.__redis_conn = self.__connect_to_cache()

            if self.__check_cache():
                return  # If we get here, the cache was populated, and the _worksheets object was populated.
        
        self._get_data()
    
    def __populate_data(self):
        """
        Populates the _data attribute based on the selected sheet for this instance of the SheetReader.
        """
        data = settings.MEDICINE_SHEETS_DATA

        if self._data_key not in data.keys():
            raise exceptions.UnknownSheetError(self._data_key)

        return settings.MEDICINE_SHEETS_DATA[self._data_key]
    
    def __connect_to_cache(self):
        """
        Attempts to connect to the Redis cache, and returns the object if successful.
        Raises an exception if this fails.
        """
        try:
            redis_conn = redis.StrictRedis(host=settings.REDIS_HOSTNAME,
                                           port=settings.REDIS_PORT,
                                           db=0)
            redis_conn.exists('test')  # Forces the connection to establish; failures are captured from here.
        except redis.exceptions.ConnectionError:
            raise exceptions.CacheConnectionError("Could not connect to the Redis host.")
        
        return redis_conn
    
    def __check_cache(self):
        """
        Checks to see if the Redis cache has the necessary keys to use.
        Returns True if all keys are present; False otherwise.
        Sets the self._dataframes instance variable.
        """
        present_worksheets = 0
        worksheets = self._data['worksheets']

        for worksheet_key, worksheet_data in worksheets.items():
            redis_worksheet_key = f"{worksheet_data['redis_key']}{REDIS_WORKSHEET_SUFFIX}"
            redis_dataframe_key = f"{worksheet_data['redis_key']}{REDIS_DATAFRAME_SUFFIX}"

            if self.__redis_conn.exists(redis_worksheet_key) and self.__redis_conn.exists(redis_dataframe_key):
                self._worksheets[worksheet_key] = pickle.loads(zlib.decompress(self.__redis_conn.get(redis_worksheet_key)))
                self._dataframes[worksheet_key] = pickle.loads(zlib.decompress(self.__redis_conn.get(redis_dataframe_key)))
                present_worksheets += 1
        
        if len(self._data['worksheets'].keys()) == present_worksheets:
            return True

        return False
    
    def __connect_to_google(self, document_key):
        """
        Returns a Spreadsheet object, representing the connection to the document denoted by document_key (string).
        """
        try:
            client = pygsheets.authorize(service_file=settings.GOOGLE_API_SECRET_PATH)
            connection = client.open_by_key(document_key)
        except Exception as e:
            raise exceptions.GoogleConnectionError(f"An exception occurred connecting to the Google Sheets API. {str(e)}")
        
        return connection
    
    def _get_data(self):
        """
        Sets the _worksheets and _dataframes attributes.
        For each of the required worksheets/dataframes, creates a Worksheet object.

        If a Worksheet cannot be found, an UnknownSheetError exception is raised.
        """
        worksheets = self._data['worksheets']

        for worksheet_key, worksheet_data in worksheets.items():
            try:
                Sheet.objects.get(name=worksheet_key)  # Do we recognise the sheet in the database?
            except Sheet.DoesNotExist:
                raise exceptions.UnknownSheetError(worksheet_key)
            
            # Prepare the data
            self.__prepare_worksheet(worksheet_key)
            self.__prepare_dataframe(worksheet_key)
    
    def __prepare_worksheet(self, worksheet_key):
        """
        Given a Worksheet key, creates the Worksheet object and caches it, if caching is enabled.
        The _worksheets instance attribute is also updated to include this object.
        """
        if worksheet_key not in self._data['worksheets'].keys():
            raise exceptions.UnknownSheetError(worksheet_key)
        
        connection = self.__connect_to_google(self._data['document_key'])
        worksheet_data = self._data['worksheets'][worksheet_key]

        try:
            self._worksheets[worksheet_key] = connection.worksheet('title', worksheet_data['sheet_name'])  # Is the sheet known in the Spreadsheet?
        except WorksheetNotFound:
            raise exceptions.UnknownSheetError(worksheet_data['sheet_name'])
        
        # Cache the Worksheet and DataFrame objects if Redis is being used.
        if settings.REDIS_ENABLED:
            redis_worksheet_key = f"{worksheet_data['redis_key']}{REDIS_WORKSHEET_SUFFIX}"

            self.__redis_conn.setex(redis_worksheet_key,
                                    settings.REDIS_EXPIRATION_TIME,
                                    zlib.compress(pickle.dumps(self._worksheets[worksheet_key])))
        

    def __prepare_dataframe(self, worksheet_key):
        """
        Given a Worksheet key, creates a DataFrame object from the stored Worksheet, and caches it if caching is enabled.
        The _dataframes instance attribute is also updated to include this object.
        """
        if worksheet_key not in self._data['worksheets'].keys():
            raise exceptions.UnknownSheetError(worksheet_key)

        worksheet_data = self._data['worksheets'][worksheet_key]

        # If start is specified, we start the DataFrame from row x.
        # This allows us to ignore, for example, instructions at the top of a worksheet.
        if 'start' in worksheet_data.keys():
            df = self._worksheets[worksheet_key].get_as_df(start=worksheet_data['start'])
        else:
            df = self._worksheets[worksheet_key].get_as_df()
        
        df = df.rename(columns=str.lower)
        df['row_number'] = df.index  # Make a copy of the row numbers to preserve them.

        # We can skip the first x rows with the skip attribute. Ignore if not provided.
        if 'skip' in worksheet_data.keys():
            try:
                skip_rows = int(worksheet_data['skip'])
                df = df.loc[skip_rows:]
            except ValueError:
                pass
        
        self._dataframes[worksheet_key] = df

        # Cache the DataFrame is Redis is being used.
        if settings.REDIS_ENABLED:
            redis_dataframe_key = f"{worksheet_data['redis_key']}{REDIS_DATAFRAME_SUFFIX}"

            self.__redis_conn.setex(redis_dataframe_key,
                                    settings.REDIS_EXPIRATION_TIME,
                                    zlib.compress(pickle.dumps(self._dataframes[worksheet_key])))
    
    def save_to_worksheet(self, worksheet_key, data):
        """
        Inserts data into the Worksheet, and synchronises the changes to the Worksheet on Google's servers.
        Refreshes the caches (if used).
        """
        if worksheet_key not in self._data['worksheets'].keys():
            raise exceptions.UnknownSheetError(worksheet_key)
        
        worksheet_data = self._data['worksheets'][worksheet_key]
        worksheet = self._worksheets[worksheet_key]
        worksheet.sync()

        data_list = self.__data_dict_to_list(worksheet_key, data)

        # If we don't have an insert attribute, we position the new row at the top.
        if 'insert' in worksheet_data.keys():
            worksheet.insert_rows(worksheet_data['insert'], values=data_list, inherit=True)
        else:
            worksheet.insert_rows(1, values=data_list, inherit=True)

        self.__prepare_worksheet(worksheet_key)
        self.__prepare_dataframe(worksheet_key)
    
    def __data_dict_to_list(self, worksheet_key, data):
        """
        Creates a list of items that should be appended to a new row in the specified worksheet.
        Data should be a dictionary, where keys are column names, and values are the values to be placed in the specified column.
        """
        return_list = []
        data_normalised = {k.lower(): v for k, v in data.items()}
        dataframe = self._dataframes[worksheet_key]

        for column_name in dataframe.columns:
            data_key_lower = column_name.lower()

            if data_key_lower in data_normalised.keys():
                return_list.append(data_normalised[data_key_lower])
                continue
            
            return_list.append('')

        return return_list
