import zlib
import redis
import pickle
import pygsheets
from django.conf import settings
from medicine_api.readers import exceptions
from pygsheets.exceptions import WorksheetNotFound


class SheetReader(object):
    def __init__(self, document_id, required_sheets, using_cache=True):
        redis_conn = None
        self._dataframes = {}
        self._document_id = document_id
        self._required_dataframes = self.__read_sheets_data(required_sheets)
        self._language_data = settings.MEDICINE_LANGUAGE_DATA

        if using_cache:
            redis_conn = self.__connect_to_cache()

            if self.__check_cache(redis_conn):
                return  # If we get here, the cache was populated and loaded.
        
        # If we get here, data needs to be loaded from the Sheets API.
        self.__get_sheets(using_cache, redis_conn=redis_conn)
    
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
    
    def __check_cache(self, redis_conn):
        """
        Checks to see if the Redis cache has the necessary keys to use.
        Returns True if all keys are present; False otherwise.
        Sets the self._dataframes instance variable.
        """
        present_dataframes = 0

        for df_sheet, df_values in self._required_dataframes.items():
            if redis_conn.exists(df_values['redis_key']):
                self._dataframes[df_sheet] = pickle.loads(zlib.decompress(redis_conn.get(df_values['redis_key'])))
                present_dataframes += 1
        
        if len(self._required_dataframes.keys()) == present_dataframes:
            return True
        
        return False
    
    def __get_sheets(self, use_cache, redis_conn=None):
        """
        Connects to the Google Sheets API to extract the necessary data.
        Populates the cache if required; sets the object's instance variables.
        """
        try:
            client = pygsheets.authorize(service_file=settings.GOOGLE_API_SECRET_PATH)
            table = client.open_by_key(self._document_id)
        except Exception as e:
            raise exceptions.GoogleConnectionError(f"An exception occurred connecting to the Google Sheets API. {str(e)}")
        
        for df_sheet, df_values in self._required_dataframes.items():
            try:
                worksheet = table.worksheet('title', df_values['sheet_name'])
            except WorksheetNotFound:
                raise exceptions.UnknownSheetError()

            if 'start' in df_values:
                df = worksheet.get_as_df(start=df_values['start'])
            else:
                df = worksheet.get_as_df()
            
            df = df.rename(columns=str.lower)
            df['row_number'] = df.index  # Copy row numbers, preserving them

            self._dataframes[df_sheet] = df

            if use_cache:
                redis_conn.setex(df_values['redis_key'],
                                 settings.REDIS_EXPIRATION_TIME,
                                 zlib.compress(pickle.dumps(df)))
    
    def __read_sheets_data(self, required_sheets):
        """
        Returns information on the requested sheets.
        This data is pulled from SHEETS.json in the root of the repository.
        """
        return_object = {}
        data = settings.MEDICINE_SHEETS_DATA

        if self._document_id not in data.keys():
            raise exceptions.UnknownDocumentError(self._document_id)
        
        for sheet_name in required_sheets:
            if sheet_name in data[self._document_id].keys():
                return_object[sheet_name] = data[self._document_id][sheet_name]
                continue
            
            raise exceptions.UnknownSheetError(sheet_name)
        
        return return_object