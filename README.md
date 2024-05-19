
# CygnoUNet Project

## Setup Environment on Google Colab

To set up the CygnoNet project on Google Colab, follow these steps:

1. **Install Poetry and Clone the Repository:**

   ```python
   !pip install -q poetry
   !git clone https://github.com/Gui1402/cygunet.git
   %cd cygunet
   !git checkout feature/insert-properties
   ```

2. **Mount Google Drive (if needed):**

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **Unzip Data into the Project Directory:**

   Replace `<PATH_ER_NR.ZIP>` with the actual path to your ZIP file in Google Drive.

   ```python
   !unzip /content/drive/MyDrive/<PATH_ER_NR.ZIP> -d /content/cygunet/data/01_raw
   !mv /content/cygunet/data/01_raw/ER-NR/* /content/cygunet/data/01_raw/
   !rmdir /content/cygunet/data/01_raw/ER-NR
   ```

4. **Configure Poetry to Use the System Environment and Install Dependencies:**

   ```python
   !poetry config virtualenvs.create false
   !poetry install
   ```

## Setup Environment on CYGNO Cloud

*To be filled in with specific instructions for setting up the environment on CYGNO Cloud.*

## Accessing Catalogs to Use Events

After setting up the environment, you can access catalogs to use events as follows:

1. **Bootstrap the Kedro Project:**

   ```python
   from kedro.framework.startup import bootstrap_project
   from kedro.framework.project import pipelines, settings

   # Bootstrap the project to set up logging and configuration
   project_path = '/content/cygunet'
   bootstrap_project(project_path)
   ```

2. **Create a Kedro Session and Load the Catalog:**

   ```python
   from kedro.framework.session import KedroSession

   # Create and manage the session yourself
   with KedroSession.create(project_path) as session:
       context = session.load_context()

   catalog = context.catalog
   ```

3. **Load and Access Data from the Catalog:**

   For example, to access the `simulation.NR_30` catalog:

   ```python
   nr_30 = catalog.load("simulation.NR_30")
   ```

By following these steps, you will be able to set up your environment in Google Colab, configure Poetry, and use Kedro to access your data catalogs.