# coding: utf-8
import gpxpy
import geopy
import os
import sys


def find_cities(fichier: str) -> tuple:
    """
    Trouve le nom du point de départ et du point d'arrivée

    Args:
        fichier (str): le fichier gpx
    Returns
        Tuple(str,str): un tuple de chaîne de caractères
    """
    with open(fichier) as f:
        gpx = gpxpy.parse(f)

    finder = geopy.Nominatim(user_agent="test")
    """
    zoom = 14 pour le quartier
    zoom = 16 pour la rue
    """
    start_city = finder.reverse(
        (
            gpx.tracks[0].segments[0].points[0].latitude,
            gpx.tracks[0].segments[0].points[0].longitude,
        ),
        zoom=14,
    ).address.split(",")[0]
    end_city = finder.reverse(
        (
            gpx.tracks[-1].segments[-1].points[-1].latitude,
            gpx.tracks[-1].segments[-1].points[-1].longitude,
        ),
        zoom=14,
    ).address.split(",")[0]
    return start_city, end_city


def rename(fichier: str)-> None:
    """
    Renomme le fichier avec le point de départ et d'arrivée

    Args:
        fichier (str): le nom du fichier à renommer
    Returns:
        None
    """
    start_city, end_city = find_cities(fichier)
    os.rename(fichier, f"{fichier[:-4]} {start_city} - {end_city}.gpx")


if __name__ == '__main__':
    assert len(sys.argv) > 0
    rename(sys.argv[1])
