import os
import strix
import files
import click


# Does this file exist in expansion pack asset loading directory?
def roll_call():
	path_app_assets = config.PATH_APP_ASSETS
	path_expansion_assets = config.PATH_EXPANSION_ASSETS
	path_songs = config.PATH_SONGS

	path_family_images = os.listdir(f'{path_app_assets}/images/family')
	path_species_images = f'{path_expansion_assets}/images/species'

	species_images = os.listdir(species_path) 
	click.echo(species_path)

	plumage_images = os.listdir(f'{path_expansion_assets}/images/plumages')
	map_images = os.listdir(f'{path_expansion_assets}/images/maps')
	songs = os.listdir(path_songs)

	click.echo(f'Found {len(family_images)} family image files')    
	click.echo(f'Found {len(species_images)} species image files')
	click.echo(f'Found {len(plumage_images)} plumage image files')
	click.echo(f'Found {len(songs)} songs')

	if len(species_images) != NUM_SPECIES_IMAGES:
		missing = NUM_SPECIES_IMAGES - len(species_images)
		click.echo(f'{missing} species images may be missing out of a hoped-for {NUM_SPECIES_IMAGES}.')


def songs():
	songs_list = files.get_songs()
	species_id_list = strix.get_species_id_list()
	for id in species_id_list:
		songs_for_this_species = strix.get_songs_for_species(id)
		check_songs_are_found(songs_for_this_species, songs)
		
def check_songs_are_found(songs_for_this_species, master_song_list):
	for song in songs_for_this_species:
		if song not in master_song_list:
			click.echo(f'{song} not found')

def get_song_file_list():
	pass

def get_species_id_list():
	pass

def get_species_ref_list():
	pass

