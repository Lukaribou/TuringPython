from src.Turing import Turing

if __name__ == '__main__':
    from sys import argv

    if len(argv) < 3:
        print("Utilisation:\n> main.py chemin_fichier.xxx valeur_entree")
    else:
        turing = Turing.from_file(argv[1], argv[2])
        print(turing.run())
