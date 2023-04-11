# La fonction  utilise la  fonction "pygame.transform.scale" pour redimensionner
# l'image  en multipliant sa largeur et sa   hauteur  par le  facteur  donné. La
# fonction  "memoize" est appliquée  à   la fonction "resize", ce  qui permet de
# conserver en  cache les résultats de la fonction et d'éviter de recalculer les
# mêmes résultats plusieurs fois.


from src.tools.memoize import memoize
import pygame


@memoize
def resize(img, factor):
    return pygame.transform.scale(
        img, (int(img.get_width() * factor), int(img.get_height() * factor))
    )
