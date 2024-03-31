import pathlib
import connexion


basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

