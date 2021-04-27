from typing import Dict

from flask import Flask, request

from Turing import Turing

app = Flask(__name__)


@app.route('/exec', methods=['GET', 'POST'])
def exec_route():
    r_data: Dict[str, str] = request.get_json()
    m_turing = Turing(r_data['program'], r_data['bride'])

    data = {}
    try:
        m_turing.run(record_mvt=True)
        data['record'] = m_turing.record
    except (ValueError, KeyError) as err:
        data['error'] = err

    return data  # va automatiquement appeler jsonify


if __name__ == '__main__':
    """
    from sys import argv

    if len(argv) < 3:
        print("Utilisation:\n> main.py chemin_fichier.xxx valeur_entree")
    else:
        turing = Turing.from_file(argv[1], argv[2])
        print(turing.run())
    """

    app.run()
