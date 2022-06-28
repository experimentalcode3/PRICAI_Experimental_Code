from abc import abstractmethod
from google.oauth2 import service_account
import pandas_gbq


class DataExtractor:
    def __init__(
            self,
            args
    ):
        self.args = args
        self.query_prefix = args.query_prefix

        self.ent_extract = args.ent_extract
        self.rel_extract = args.rel_extract
        self.feat_extract = args.feat_extract

        self.conn = None
        self.path = args.path

        self._setup_conn()

    def _setup_conn(self):
        if self.ent_extract or self.rel_extract or self.feat_extract:
            try:
                self.conn = self._get_gbq_conn()
            except Exception:
                exit(f"Connection to gqb could not be established, can\'t continue")
        else:
            print('All extraction arguments set to false, using local parquet files\n')

    def _get_gbq_conn(self):
        return service_account.Credentials.from_service_account_file(
            f'{self.path["config_fold"]}mimiciv_gbq.json'
        )

    def extract(self, func, *args):
        df = pandas_gbq.read_gbq(
            func(*args),
            project_id=self.args.project_id,
            credentials=self.conn)

        # save df as parquet file
        if df is not None:
            df.to_parquet(f'{self.path["output_fold"]}{func.__name__}.parquet')
            print(f'Read and wrote query: {func.__name__}')
        else:
            exit(f"No data extracted with function: {func.__name__}")

    @abstractmethod
    def run_queries(self):
        pass
