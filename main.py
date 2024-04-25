#Pune importurile aici
#
#Dupa ce instalezi importurile baga in consola "pip freeze > requirements.txt
try:
    import pygame
except ImportError:
    print("Please run 'pip install -r requirements.txt in this folder's directory.")


#Pune codu aci
def main():
    print("It works!")


if __name__ == "__main__":
    main()
print("merge bine")