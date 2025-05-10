# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = "mbsa.csv"  # Replace with the actual file name

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "gauravduttakiit/bitcoin-tweets-16m-tweets-with-sentiment-tagged",
  file_path,
  # Provide any additional arguments like
  # sql_query or pandas_kwargs. See the
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)
# Deja el DataFrame disponible para importar desde otros archivos
if __name__ == "__main__":
  # generate a csv file
  df.to_csv(file_path, index=False)
# Print the first 5 records
  print("First 5 records:", df.head())
