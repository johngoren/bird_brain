import os
import files
import config
import click
import helpers
import pdb


# Does this file exist in expansion pack asset loading directory?
def roll_call():
	path_expansion_assets = config.PATH_OBB_SOURCE
	path_songs = config.PATH_SONGS

	path_family_images = config.PATH_FAMILY
	path_species_images = config.PATH_SPECIES_IMAGES_FULL
	path_thumbs = config.PATH_SPECIES_IMAGES_THUMBNAIL

	species_images = os.listdir(path_species_images)
	desired_num_species_images = config.NUM_SPECIES_IMAGES

	plumage_images = os.listdir(f'{path_expansion_assets}/images/plumages')
	map_images = os.listdir(f'{path_expansion_assets}/images/maps')
	family_images = os.listdir(f'{path_family_images}')
	songs = os.listdir(path_songs)
	thumbs = os.listdir(path_thumbs)

	click.echo(f'Found {len(family_images)} family image files')    
	click.echo(f'Found {len(species_images)} species image files (expected {desired_num_species_images})')
	click.echo(f'Found {len(plumage_images)} plumage image files')
	click.echo(f'Found {len(songs)} songs')
	click.echo(f'Found {len(thumbs)} thumbs')

	if len(species_images) != desired_num_species_images:
		missing = desired_num_species_images - len(species_images)
		click.echo(f'{missing} species images may be missing out of a hoped-for {desired_num_species_images}.')


def songs(strix):
	not_found = 0
	
	songs_list = files.get_songs()
	species_id_list = strix.get_species_id_list()
	for id in species_id_list:
		# pdb.set_trace()
		songs_for_this_species = strix.get_song_refs_for_species(id)
		android_filenames = helpers.androidize_song_refs(songs_for_this_species)
		missing = check_my_songs_are_found(android_filenames, songs_list)
		if missing > 0:
			not_found = not_found + missing

	click.echo(f'Missing {not_found} songs')


def check_my_songs_are_found(songs_for_this_species, master_song_list):
	not_found = 0

	for song in songs_for_this_species:
		if song not in master_song_list:
			click.echo(f'{song} not found')
			not_found = not_found + 1

	return not_found
